"""Initialize exact renderer text slots without replacing later human edits.

The original editorial draft arrays are a guard: this migration only replaces
an untouched draft list or an already synchronized renderer list. It never
rewrites a title, caption, or source section.
"""
from __future__ import annotations
import json
import re
from render import ROOT, TEXT, entries
from episodes_first import SCREEN_TEXT as FIRST
from episodes_second import SCREEN_TEXT as SECOND

NUMERICAL_LABELS = {
    1: 'Clock t and calculated elapsed times. The same equal-mass elastic-disk collision is transformed in both panels; ball radius and collision separation use the same spatial scale.',
    2: 'Vertex labels A, B, C. Action selector e, r, r², s, rs, r²s. Intermediate rotation and reflection frames show the motion between discrete group actions.',
    3: 'R = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]; S = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]. The displayed state starts at (1, 3, 5), follows three cyclic permutations, then two reflections. Colors follow the values.',
    4: '(1, 3, 5) = (3, 3, 3) + (−2, 0, 2). The component axes are x₁, x₂, x₃. The common part lies on the equal-components axis; the zero-sum part turns in its perpendicular plane.',
    5: 'Axes x and y; live θ in degrees; actual current values of r² and u. The reference values are 1.000 and +0.707. Cubic u varies during intermediate angles and returns at the allowed 120° endpoints.',
    6: 'The translation parameter a is displayed numerically as the marked line moves. The circle has a tracked radial direction.',
    7: 'J = [[0, −1], [1, 0]]. Vector labels v and Jv, and axes x and y. State and tangent arrows use the same scale.',
    8: 'Axes x and y. The dots and marked quadrilateral undergo the same rotation; vector-field arrow lengths use one common display scale.',
}


def main():
    current = entries()
    inventories = FIRST | SECOND
    drafts = {}
    for name in ('captions-01-08.draft.json', 'captions-09-16.draft.json'):
        for item in json.loads((TEXT.parent/name).read_text(encoding='utf8')):
            drafts[item['number']] = item['screen_text']
    for number, entry in current.items():
        if entry['screen_text'] not in (drafts[number], inventories[number]):
            raise ValueError(f'Reel {number}: on-screen text differs from its draft and renderer inventory; preserve and reconcile the human edit.')
    document = TEXT.read_text(encoding='utf8')
    blocks = re.split(r'(^## Reel\s+\d+\s*$)', document, flags=re.M)
    for index in range(1,len(blocks),2):
        number = int(re.search(r'\d+',blocks[index]).group())
        section = blocks[index+1]
        replacement = '### On-screen text\n\n'+'\n'.join('- '+label for label in inventories[number])+'\n\n'
        section, count = re.subn(r'^### On-screen text\n.*?(?=^### |\Z)',replacement.replace('\\','\\\\'),section,flags=re.M|re.S)
        if count != 1:
            raise ValueError(f'Reel {number}: expected one on-screen block')
        if number in NUMERICAL_LABELS and '### Numerical labels' not in section:
            section = section.replace('### Source\n','### Numerical labels\n\n'+NUMERICAL_LABELS[number]+'\n\n### Source\n',1)
        blocks[index+1] = section
    updated=''.join(blocks)
    note=('The on-screen lists use stable ordered slots. Edit their wording in place; preserve the order and number of entries. '
          'Equation entries use raw TeX and are rendered as mathematics. Numerical labels below describe calculated readings and fixed symbols.\n\n')
    if 'The on-screen lists use stable ordered slots.' not in updated:
        updated=updated.replace('---\n\n## Reel 01',note+'---\n\n## Reel 01',1)
    TEXT.write_text(updated,encoding='utf8')
    print('Synchronized all 16 screen inventories; titles, captions and source sections preserved.')


if __name__=='__main__':
    main()
