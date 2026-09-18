"""Verify timing, frame counts/order, and sampled visual fidelity to the backup."""
from __future__ import annotations
import struct
from retime import BACKUP
from render import *

def atoms(data,start=0,end=None):
    end=len(data) if end is None else end
    while start<end:
        size,kind=struct.unpack_from('>I4s',data,start)
        header=8
        if size==1:size=struct.unpack_from('>Q',data,start+8)[0];header=16
        if size==0:size=end-start
        assert size>=header and start+size<=end
        yield kind,start+header,start+size
        start+=size

def metadata(path):
    data=path.read_bytes(); found={}; top=list(atoms(data))
    found['faststart']=next(i for i,x in enumerate(top) if x[0]==b'moov')<next(i for i,x in enumerate(top) if x[0]==b'mdat')
    def visit(start,end):
        for kind,a,b in atoms(data,start,end):
            if kind in (b'moov',b'trak',b'mdia',b'minf',b'stbl'):visit(a,b)
            elif kind==b'mdhd':
                assert data[a]==0
                found['timescale'],found['duration_ticks']=struct.unpack_from('>II',data,a+12)
            elif kind==b'stsz':found['frames']=struct.unpack_from('>I',data,a+8)[0]
            elif kind==b'stts':
                count=struct.unpack_from('>I',data,a+4)[0]
                found['timing_runs']=[struct.unpack_from('>II',data,a+8+8*i) for i in range(count)]
    visit(0,len(data))
    found['duration']=found['duration_ticks']/found['timescale']
    return found

def sample_frames(path,indices):
    select='+'.join(f'eq(n\\,{n})' for n in indices)
    raw=subprocess.check_output([imageio_ffmpeg.get_ffmpeg_exe(),'-v','error','-i',str(path),
        '-vf',f'select={select},scale=270:480','-fps_mode','passthrough',
        '-an','-f','rawvideo','-pix_fmt','rgb24','-threads','2','-'])
    return np.frombuffer(raw,dtype=np.uint8).reshape((len(indices),480,270,3))

def main():
    rows=[]; media=[];entries=episodes();review=OUT/'review';review.mkdir(exist_ok=True)
    original=json.loads((BACKUP/'manifest.json').read_text(encoding='utf8'))
    manifest=json.loads((OUT/'manifest.json').read_text(encoding='utf8'))
    for number,e in entries.items():
        src=BACKUP/f'{slug(number)}.mp4';dst=OUT/f'{slug(number)}.mp4'
        before=metadata(src);after=metadata(dst)
        assert before['frames']==after['frames']==round(e['source_duration']*SOURCE_FPS)
        assert abs(after['duration']-before['duration']/PLAYBACK_SPEED)<1/after['timescale']
        assert all(abs(delta/after['timescale']-1/FPS)<1e-9 for count,delta in after['timing_runs'])
        assert after['faststart']
        probe=subprocess.run([imageio_ffmpeg.get_ffmpeg_exe(),'-hide_banner','-i',str(dst)],
            stdout=subprocess.DEVNULL,stderr=subprocess.PIPE).stderr.decode('utf8',errors='replace')
        assert 'Audio:' not in probe and 'h264' in probe and 'yuv420p' in probe
        assert '1080x1920' in probe and '42 fps' in probe
        n=after['frames'];indices=[0,n//4,n//2,3*n//4,n-1]
        old=sample_frames(src,indices);new=sample_frames(dst,indices)
        errors=np.sqrt(np.mean((old.astype(float)-new.astype(float))**2,axis=(1,2,3)))/255
        assert float(max(errors))<.02,(number,errors)
        sheet=Image.new('RGB',(270*len(indices),520),BG);d=ImageDraw.Draw(sheet)
        for i,(frame,index) in enumerate(zip(new,indices)):
            sheet.paste(Image.fromarray(frame),(270*i,0))
            d.text((270*i+10,488),f'{index/FPS:.2f}s',font=font(20),fill=INK)
        sheet.save(review/f'{slug(number)}-retimed-contact-sheet.jpg',quality=93)
        old_caption=original['episodes'][number-1]['caption']
        expected=old_caption.replace('Full chapter: wadelamble.github.io/constrained-improvisation/symmetry/',
            'Website: https://wadelamble.github.io/constrained-improvisation/\nFull chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/')
        assert manifest['episodes'][number-1]['caption']==expected
        assert manifest['episodes'][number-1]['status']=='staged'
        assert Image.open(OUT/f'{slug(number)}-cover.jpg').size==(W,H)
        media.append(dict(episode=number,seconds=after['duration'],fps=FPS,
            bytes=dst.stat().st_size,caption_characters=len(expected),
            full_decode='pass (sample selection traverses all frames)',audio_tracks=0))
        rows.append(dict(episode=number,source_seconds=before['duration'],seconds=after['duration'],
            frames=n,fps=FPS,faststart=True,frame_count_and_sample_order='pass',
            sampled_frame_rmse=[float(x) for x in errors],caption_changes='URLs only'))
        print(f'Verified retime {number:02d}: {n} frames / {after["duration"]:.6f}s',flush=True)
    (OUT/'retiming-validation.json').write_text(json.dumps(dict(speed=PLAYBACK_SPEED,
        immutable_backup=str(BACKUP.relative_to(ROOT)),episodes=rows),indent=2),encoding='utf8')
    report=json.loads((BACKUP/'validation.json').read_text(encoding='utf8'))
    report['media']=media
    report.pop('package',None)
    report['retiming']='All frames retained at 1.75x; numerical content unchanged from original validated package.'
    (OUT/'validation.json').write_text(json.dumps(report,indent=2),encoding='utf8')

if __name__=='__main__':main()
