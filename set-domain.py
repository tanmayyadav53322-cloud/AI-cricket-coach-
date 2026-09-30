#!/usr/bin/env python3
"""Replace the placeholder domain everywhere. Usage: python3 scripts/set-domain.py https://your-domain.com"""
import os, sys
old = 'https://aicricketcoach.app'
new = sys.argv[1].rstrip('/')
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
n = 0
for dp, dns, fns in os.walk(root):
    dns[:] = [d for d in dns if not d.startswith('.')]
    for fn in fns:
        if fn.endswith(('.html', '.txt', '.xml', '.md')):
            p = os.path.join(dp, fn)
            t = open(p, encoding='utf-8').read()
            if old in t:
                open(p, 'w', encoding='utf-8').write(t.replace(old, new)); n += 1
print(f'Updated {n} files to {new}')
