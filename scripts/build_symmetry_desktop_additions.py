"""Build a local review gallery for the six reel-to-desktop adaptations.

Optional --render resumes the batch by skipping complete, hash-verified movies
whose generator and helper hashes still match. An interrupted movie is rendered
again, while completed movies are retained. This script does not edit the chapter
or publish anything. Run with the animation Python environment for --render.
"""
from __future__ import annotations
import argparse
import hashlib
from html import escape
from html.parser import HTMLParser
import json
import os
from pathlib import Path
import subprocess
import sys
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / 'content/drafts/animations'
OUT = ROOT / 'content/review/symmetry-desktop-additions'
ENTRIES = [
    dict(id='matrices', stem='symmetry-d3-transformation-matrices',
         title='Representing Symmetry with Matrices', reel='Symmetry to Waves · 5',
         description='The same values move between component slots as the rotation and reflection matrices act.',
         placement='Representations, after the worked matrix multiplication.',
         script='generate_symmetry_d3_matrices_desktop.py', helper='symmetry_desktop_d3.py'),
    dict(id='invariants', stem='symmetry-d3-invariants',
         title='What the Triangle’s Symmetries Preserve', reel='Symmetry to Waves · 8',
         description='Squared length stays fixed throughout. The cubic invariant returns to its original value at each allowed rotation.',
         placement='Invariants, after the squared-length and cubic-invariant equations.',
         script='generate_symmetry_d3_invariants_desktop.py', helper='symmetry_desktop_d3.py'),
    dict(id='commutator', stem='symmetry-commutator-sphere',
         title='The Commutator Encodes Group Structure Locally', reel='Symmetry to Waves · 16',
         description='Opposite rotation orders leave different endpoints. Shrinking the rotations reveals the third generator in the magnified mismatch.',
         placement='Commutators and Lie Algebra, alongside the infinitesimal rotation relationships.',
         script='generate_symmetry_commutator_sphere_desktop.py'),
    dict(id='eigenfunctions', stem='symmetry-translation-eigenfunctions',
         title='Translation Eigenfunctions Are Exponentials', reel='Symmetry to Waves · 23 · authoring label 24',
         description='Differentiation and translation reproduce the exponential function multiplied by a number.',
         placement='Eigenfunctions of Translational Symmetry, after the derivative equation.',
         script='generate_symmetry_translation_eigenfunctions_desktop.py', helper='symmetry_exponential_desktop_common.py'),
    dict(id='unitarity', stem='symmetry-translation-unitarity',
         title='Translation of Complex Exponentials Preserves the Inner Product', reel='Symmetry to Waves · 24 · authoring label 24a',
         description='Compare two coefficients of one exponential mode. Real scaling changes their inner product, while a common complex rotation preserves it.',
         placement='Unitarity, after the real-versus-complex exponential comparison.',
         script='generate_symmetry_translation_unitarity_desktop.py', helper='symmetry_exponential_desktop_common.py'),
    dict(id='momentum', stem='symmetry-momentum-uncertainty',
         title='Wave Number Becomes Momentum', reel='Waves to Quanta · 13',
         description='The same translation is written using wave number and momentum, followed by the Gaussian width tradeoff in physical units.',
         placement='Quantum Mechanics, after the position–momentum uncertainty relation.',
         script='generate_symmetry_momentum_uncertainty_desktop.py', helper='generate_symmetry_casimir_desktop.py', helper_key='renderer_sha256'),
]


def digest(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()


def verified(entry):
    stem = entry['stem']
    required = [ASSETS/f'{stem}{suffix}' for suffix in ('.mp4','-poster.png','-contact-sheet.png','-validation.json','-encoded-validation.json')]
    if not all(p.is_file() for p in required): return False
    maths = json.loads(required[3].read_text(encoding='utf8'))
    encoded = json.loads(required[4].read_text(encoding='utf8'))
    if encoded.get('decode')!='passed' or encoded.get('video_sha256')!=digest(required[0]): return False
    if maths.get('source_sha256')!=digest(ROOT/'scripts'/entry['script']): return False
    if entry.get('helper') and maths.get(entry.get('helper_key','helper_sha256'))!=digest(ROOT/'scripts'/entry['helper']): return False
    return True


def href(path):
    return Path(os.path.relpath(path,OUT)).as_posix()


def receipt(entry):
    return {'video_sha256':digest(ASSETS/f"{entry['stem']}.mp4"),
            'sources':{p:digest(ROOT/'scripts'/p) for p in (entry['script'],entry.get('helper')) if p}}


def cached(entry):
    path=OUT/'render-receipts.json'
    if not path.is_file() or not verified(entry): return False
    return json.loads(path.read_text(encoding='utf8')).get(entry['stem'])==receipt(entry)


def record_completed(entry):
    OUT.mkdir(parents=True,exist_ok=True)
    path=OUT/'render-receipts.json'
    records=json.loads(path.read_text(encoding='utf8')) if path.is_file() else {}
    records[entry['stem']]=receipt(entry)
    temporary=OUT/'render-receipts.pending.json'
    temporary.write_text(json.dumps(records,indent=2)+'\n',encoding='utf8')
    temporary.replace(path)


class Links(HTMLParser):
    def __init__(self): super().__init__(); self.urls=[]
    def handle_starttag(self,tag,attrs):
        for key,value in attrs:
            if key in ('href','src','poster') and value: self.urls.append(value)


def build():
    OUT.mkdir(parents=True,exist_ok=True)
    cards=[]
    records=[]
    for e in ENTRIES:
        if not verified(e): raise RuntimeError(f"Incomplete or stale animation: {e['stem']}. Run with --render to finish it.")
        stem=e['stem']
        report=json.loads((ASSETS/f'{stem}-encoded-validation.json').read_text(encoding='utf8'))
        version=report['video_sha256'][:12]
        video=href(ASSETS/f'{stem}.mp4')+'?v='+version
        poster=href(ASSETS/f'{stem}-poster.png')+'?v='+version
        frames=href(ASSETS/f'{stem}-contact-sheet.png')+'?v='+version
        maths=href(ASSETS/f'{stem}-validation.json')
        source=href(ROOT/'scripts'/e['script'])
        records.append({**e,**report,'sources':{p:digest(ROOT/'scripts'/p) for p in (e['script'],e.get('helper')) if p}})
        cards.append(f'''<section id="{e['id']}">
<p class="eyebrow">{escape(e['reel'])} · {report['duration_seconds']:g} seconds</p>
<h2>{escape(e['title'])}</h2>
<video controls playsinline preload="none" poster="{poster}"><source src="{video}" type="video/mp4"></video>
<p class="description">{escape(e['description'])}</p>
<div class="links"><a href="{video}">Open video</a><a href="{frames}">View decoded frames</a></div>
<details><summary>Placement and source</summary><p>{escape(e['placement'])}</p>
<a href="{source}">Generator</a> · <a href="{maths}">Mathematical checks</a></details>
</section>''')
    nav=''.join(f'<a href="#{e["id"]}">{i}. {escape(label)}</a>' for i,(e,label) in enumerate(zip(ENTRIES,['Matrices','Invariants','Commutator','Eigenfunctions','Unitarity','Momentum']),1))
    page='''<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Desktop Animation Additions</title><style>
:root{color-scheme:light;--bg:#fffcf6;--ink:#232426;--muted:#6b675f;--line:#ded8cc;--gold:#926014}
*{box-sizing:border-box}html{scroll-behavior:smooth;scroll-padding-top:90px}body{margin:0;background:var(--bg);color:var(--ink);font:17px/1.55 system-ui,Segoe UI,sans-serif}main{max-width:1240px;margin:auto;padding:44px 26px 80px}h1{font-size:clamp(30px,4vw,48px);line-height:1.12;margin:10px 0 18px;letter-spacing:-.03em}h2{font-size:clamp(23px,2.5vw,31px);font-weight:600;line-height:1.25;margin:7px 0 22px}.intro{max-width:770px;color:var(--muted);margin-bottom:28px}.eyebrow{color:var(--gold);font-size:14px;letter-spacing:.015em;margin:0}nav{position:sticky;top:0;background:#fffcf6f5;border-bottom:1px solid var(--line);display:flex;gap:9px;flex-wrap:wrap;padding:15px 0;z-index:3}a{color:#315f91;text-underline-offset:3px}nav a{padding:5px 11px;border:1px solid var(--line);border-radius:4px;text-decoration:none;font-size:14px;color:var(--ink)}nav a:hover{border-color:var(--gold);color:var(--gold)}section{padding-top:42px;margin-top:14px;padding-bottom:36px;border-bottom:1px solid var(--line)}video{display:block;width:100%;aspect-ratio:16/9;background:var(--bg);border:1px solid var(--line);border-radius:5px}.description{max-width:900px;margin:18px 0 10px}.links{display:flex;gap:25px;font-size:15px}details{font-size:14px;color:var(--muted);margin-top:19px}summary{cursor:pointer}footer{font-size:14px;margin-top:35px;color:var(--muted)}
</style><main><p class="eyebrow">LOCAL REVIEW</p><h1>Desktop Animation Additions</h1><p class="intro">Six landscape adaptations from the reel series. Play each demonstration below. Opening another video pauses the one already playing.</p><nav>'''+nav+'</nav>'+''.join(cards)+'''<footer>1600 × 900 · 24 fps · silent MP4s. Each movie has been decoded and checked against its generator.<br>The existing <a href="../../drafts/animations/symmetry-casimir-operator.mp4">Casimir animation</a> is available separately.</footer></main>
<script>for(const video of document.querySelectorAll('video'))video.addEventListener('play',()=>{for(const other of document.querySelectorAll('video'))if(other!==video)other.pause();});</script></html>'''
    parser=Links();parser.feed(page)
    for url in parser.urls:
        parsed=urlsplit(url)
        if parsed.scheme or not parsed.path: continue
        path=(OUT/unquote(parsed.path)).resolve()
        if not path.is_file(): raise RuntimeError(f'Missing gallery link: {url}')
    (OUT/'manifest.json').write_text(json.dumps({'schema_version':1,'animations':records},indent=2)+'\n',encoding='utf8')
    (OUT/'index.html').write_text(page,encoding='utf8')
    for e in ENTRIES: record_completed(e)
    print(f'Validated {len(records)} movies and {len(parser.urls)} gallery links. Gallery: {OUT / "index.html"}')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--render',action='store_true',help='Resume the batch, re-rendering only incomplete or changed animations.')
    args=parser.parse_args()
    if args.render:
        for e in ENTRIES:
            if cached(e):
                print(f"Keeping completed movie: {e['stem']}",flush=True)
                continue
            subprocess.run([sys.executable,str(ROOT/'scripts'/e['script']),'--render','--check'],cwd=ROOT,check=True)
            if not verified(e): raise RuntimeError(f"Validation failed: {e['stem']}")
            record_completed(e)
    build()


if __name__=='__main__': main()
