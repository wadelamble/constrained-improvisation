"""Verify the finalized asset/caption pairings and portable ZIP."""
from render import *

def main():
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf8'))
    items=manifest['episodes']
    assert [e['order'] for e in items]==list(range(1,14))
    report=json.loads((OUT/'validation.json').read_text(encoding='utf8'))
    total=0
    for item in items:
        for key in ('video','preview','cover','caption_file'):
            assert (OUT/item[key]).is_file(),item[key]
        caption=(OUT/item['caption_file']).read_text(encoding='utf8')
        assert caption==item['caption'] and len(caption)<=2200
        assert caption.count('Waves to Quanta ·')==1
        assert caption.count('Next:')==(item['order']<13)
        assert 'Website: https://wadelamble.github.io/constrained-improvisation/\n' in caption
        assert 'Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/' in caption
        assert item['fps']==FPS and item['playback_speed']==PLAYBACK_SPEED
        with (OUT/item['video']).open('rb') as handle:
            assert hashlib.file_digest(handle,'sha256').hexdigest()==item['video_sha256']
        stream=imageio_ffmpeg.read_frames(str(OUT/item['preview']))
        info=next(stream);stream.close()
        assert tuple(info['size'])==(720,1280) and abs(info['duration']-item['duration_seconds'])<.1
        for row in report['media']:
            if row['episode']==item['order']:
                row['caption_characters']=len(caption)
                row['webm_preview']='720x1280, matching duration'
        total+=item['duration_seconds']
    report['package']=dict(episodes=len(items),total_seconds=total,
        manifest_pairings='pass',video_hashes='pass',caption_limit='pass',
        browser_playback='WebM encoding and duration checked; interactive playback is a separate manual check.',
        source_manuscript='unchanged')
    (OUT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')
    bundle()
    with zipfile.ZipFile(OUT.parent/'ccr2-series-package.zip') as archive:
        assert archive.testzip() is None
        assert len([n for n in archive.namelist() if n.endswith('.mp4')])==13
        assert len([n for n in archive.namelist() if n.endswith('-caption.txt')])==13
    print(json.dumps(report['package'],indent=2),flush=True)

if __name__=='__main__':main()
