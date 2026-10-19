"""Add the locally supplied soundtrack to the staged reels, without reencoding video.

The recording and reversible silent backups stay in the ignored .tools directory.
Run after stage.py, or independently to update only the soundtrack.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import shutil
import subprocess
import wave
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from core import ROOT
import numpy as np
import imageio_ffmpeg

OUT = ROOT / 'content/reels/symmetry-series-stage'
CACHE = ROOT / '.tools/reel-audio'
FFMPEG = imageio_ffmpeg.get_ffmpeg_exe()


def sha(path):
    h = hashlib.sha256()
    with Path(path).open('rb') as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b''):
            h.update(chunk)
    return h.hexdigest()


def save(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n', encoding='utf8')


def ff(*args):
    p = subprocess.run([FFMPEG, '-nostdin', '-hide_banner', *map(str, args)], capture_output=True)
    if p.returncode:
        raise RuntimeError(p.stderr.decode('utf8', errors='replace'))
    return p


def video_hash(path):
    return ff('-v', 'error', '-i', path, '-map', '0:v:0', '-c:v', 'copy',
              '-f', 'hash', '-hash', 'sha256', '-').stdout.decode().strip()


def metadata(path):
    frames = imageio_ffmpeg.read_frames(str(path))
    try:
        return next(frames)
    finally:
        frames.close()


def prepare_bed(source, total, music):
    source_hash = sha(source)
    measurements = CACHE / 'source-loudness.json'
    previous = json.loads(measurements.read_text()) if measurements.exists() else {}
    if previous.get('source_sha256') == source_hash:
        stats = previous['measurements']
    else:
        result = ff('-i', source, '-map', '0:a:0', '-af',
                    'loudnorm=I=-28:TP=-3:LRA=11:print_format=json', '-f', 'null', '-')
        log = result.stderr.decode('utf8', errors='replace')
        stats = json.loads(log[log.rfind('{'):log.rfind('}')+1])
        save(measurements, dict(source_sha256=source_hash, measurements=stats))
    # Use one constant gain. Preserve the recording's dynamics instead of compressing it.
    target = float(music.get('target_lufs', -28))
    gain = min(target-float(stats['input_i']), -3-float(stats['input_tp']))
    decoded = CACHE / 'source-pcm.wav'
    decode_record = CACHE / 'source-pcm.json'
    prior = json.loads(decode_record.read_text()) if decode_record.exists() else {}
    if not decoded.exists() or prior.get('source_sha256') != source_hash:
        ff('-v', 'error', '-y', '-i', source, '-map', '0:a:0', '-ar', '48000',
           '-ac', '2', '-c:a', 'pcm_s16le', '-map_metadata', '-1', decoded)
        save(decode_record, dict(source_sha256=source_hash))
    with wave.open(str(decoded)) as wav:
        duration = wav.getnframes()/wav.getframerate()
    crossfade = float(music.get('loop_crossfade_seconds', 2))
    assert duration > crossfade > 0
    copies = max(1, math.ceil((total-crossfade)/(duration-crossfade)))
    key = dict(source_sha256=source_hash, duration_seconds=total, gain_db=gain,
               crossfade_seconds=crossfade, sample_rate=48000, version=2)
    record = CACHE / 'music-bed.json'
    old = json.loads(record.read_text()) if record.exists() else {}
    bed = CACHE / 'music-bed.wav'
    if not bed.exists() or old.get('key') != key:
        if copies == 1:
            filters = f'[0:a]volume={gain}dB[a]'
        else:
            filters = ';'.join(f'[{i}:a]asetpts=PTS-STARTPTS[a{i}]' for i in range(copies))
            last = 'a0'
            for i in range(1, copies):
                filters += f';[{last}][a{i}]acrossfade=d={crossfade}:c1=tri:c2=tri[b{i}]'
                last = f'b{i}'
            filters += f';[{last}]volume={gain}dB[a]'
        inputs = [item for _ in range(copies) for item in ('-i', decoded)]
        ff('-v', 'error', '-y', *inputs, '-filter_complex', filters,
           '-map', '[a]', '-t', total, '-ar', '48000', '-ac', '2',
           '-c:a', 'pcm_s16le', '-map_metadata', '-1', bed)
        save(record, dict(key=key, source_duration_seconds=duration, copies=copies))
    with wave.open(str(bed)) as wav:
        assert abs(wav.getnframes()/wav.getframerate()-total) < .001
    music.update(local_source=source.relative_to(ROOT).as_posix(), source_sha256=source_hash,
                 source_duration_seconds=duration, target_lufs=target, gain_db=gain,
                 source_lufs=float(stats['input_i']), source_true_peak_dbfs=float(stats['input_tp']),
                 loop_crossfade_seconds=crossfade, fade_in_seconds=1.5, fade_out_seconds=2,
                 excerpt_policy='Consecutive passages with 2-second crossfades at recording loops and gentle fades on each reel',
                 audio_codec='AAC', audio_bitrate_kbps=192, sample_rate=48000)
    return bed, key


def add_one(e, bed, bed_key, music):
    video = OUT / e['video']
    record_path = OUT / 'records' / f'reel-{e["order"]:02d}.json'
    record = json.loads(record_path.read_text(encoding='utf8'))
    before = video_hash(video)
    duration = e['duration_seconds']
    key = dict(bed=bed_key, video_stream=before, start=e['music_start_seconds'], duration=duration,
               fade_in=music['fade_in_seconds'], fade_out=music['fade_out_seconds'], codec='aac-192k-v1')
    if record.get('audio_render_key') != key or record.get('audio_video_sha256') != sha(video):
        if metadata(video).get('audio_codec') is None:
            backup = CACHE / 'silent-stage' / video.name
            backup.parent.mkdir(parents=True, exist_ok=True)
            if not backup.exists():
                shutil.copy2(video, backup)
        temp = video.with_name(video.stem+'.audio-rendering.mp4')
        filters = (f'afade=t=in:st=0:d={key["fade_in"]},'
                   f'afade=t=out:st={duration-key["fade_out"]}:d={key["fade_out"]}')
        ff('-v', 'error', '-y', '-i', video, '-ss', e['music_start_seconds'], '-i', bed,
           '-map', '0:v:0', '-map', '1:a:0', '-c:v', 'copy', '-c:a', 'aac', '-b:a', '192k',
           '-ar', '48000', '-ac', '2', '-af', filters, '-t', duration,
           '-map_metadata', '-1', '-movflags', '+faststart', temp)
        assert video_hash(temp) == before, 'Video bitstream changed'
        info = metadata(temp)
        assert info.get('audio_codec') == 'aac' and info['size'] == (1080,1920) and info['fps'] == 30, info
        assert abs(info['duration']-duration) < .05
        temp.replace(video)
    else:
        info = metadata(video)
    audio = np.frombuffer(ff('-v', 'error', '-i', video, '-map', '0:a:0',
                             '-f', 'f32le', '-acodec', 'pcm_f32le', '-').stdout, dtype='<f4')
    assert np.isfinite(audio).all() and np.max(np.abs(audio)) < .95
    assert abs(len(audio)/(48000*2)-duration) < .05
    # Confirm signal exists beyond fades, and inspect levels without claiming to hear it.
    rms = float(np.sqrt(np.mean(audio.astype(np.float64)**2)))
    assert rms > 1e-5
    peak = float(np.max(np.abs(audio)))
    audit = dict(video_stream_unchanged=True, audio_codec='aac', sample_rate=48000, channels=2,
                 decoded_duration_seconds=len(audio)/(48000*2),
                 peak_dbfs=20*math.log10(peak), rms_dbfs=20*math.log10(rms))
    record.update(metadata=info, audio_render_key=key, audio_video_sha256=sha(video), audio_validation=audit)
    save(record_path, record)
    e.update(audio='embedded AAC soundtrack', video_sha256=sha(video), music_gain_db=music['gain_db'])
    print(f'{e["order"]:02d}/27 soundtrack included; video bitstream unchanged', flush=True)
    return e, audit


def mix_stage(workers=3):
    manifest = json.loads((OUT/'manifest.json').read_text(encoding='utf8'))
    music = json.loads((OUT/'source/music.json').read_text(encoding='utf8'))
    source = ROOT / music['local_source']
    assert source.is_file(), f'Local soundtrack source required: {source}'
    CACHE.mkdir(parents=True, exist_ok=True)
    episodes = manifest['episodes']
    # Do not start the former external preview while some videos already have audio.
    pending = dict(manifest)
    pending['music'] = dict(music, status='pending', baked_into_exports=False)
    save(OUT/'manifest.json', pending)
    cursor = 0.
    for e in episodes:
        e['music_start_seconds'] = cursor
        cursor += e['duration_seconds']
    bed, bed_key = prepare_bed(source, cursor, music)
    with ThreadPoolExecutor(max_workers=workers) as pool:
        results = list(pool.map(lambda e: add_one(e, bed, bed_key, music), episodes))
    music.update(status='mixed', mode='embedded soundtrack', baked_into_exports=True)
    manifest.update(music=music, episodes=[e for e,_ in results], audio_updated_at=datetime.now(timezone.utc).isoformat())
    save(OUT/'source/music.json', music)
    save(OUT/'manifest.json', manifest)
    validation = json.loads((OUT/'validation.json').read_text(encoding='utf8'))
    validation.update(audio='AAC soundtrack embedded in all 27 exports',
                      audio_validation={str(e['order']): audit for e,audit in results})
    for test in ('all video bitstreams unchanged by audio mux',
                 'AAC stereo 48 kHz audio decoded for every export; finite, non-silent, unclipped, correct duration'):
        if test not in validation['tests']:
            validation['tests'].append(test)
    save(OUT/'validation.json', validation)
    readme = OUT/'README.md'
    text = readme.read_text(encoding='utf8')
    start = text.index('## Music\n')
    end = text.index('## Rebuild', start)
    text = text[:start] + f'''## Music

All {len(episodes)} MP4s include {music['title']} ({music['artist']}). Consecutive excerpts play at a soft background level, with gentle fades on each reel and {music['loop_crossfade_seconds']:g}-second crossfades when the recording loops. Video streams are copied without reencoding. The preview plays the embedded audio, without an external music player.

The supplied recording and silent backups remain under the ignored `.tools/reel-audio/` directory. Nothing has been uploaded or scheduled.

''' + text[end:]
    text += '' if 'stage_audio.py' in text else '\nTo change only the audio mix, run `scripts/symmetry_reels_v2/stage_audio.py`. The local source is configured in `source/music.json`.\n'
    readme.write_text(text, encoding='utf8')
    print('All 27 staged reels now include music. No publishing performed.', flush=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--workers', type=int, default=3)
    mix_stage(parser.parse_args().workers)
