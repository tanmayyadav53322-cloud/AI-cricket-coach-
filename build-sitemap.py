#!/usr/bin/env python3
"""Regenerate sitemap.xml from the public .html files in this repo.
Usage: python3 scripts/build-sitemap.py https://your-domain.com
Run it after adding or editing pages (or as a build step on your host)."""
import os, sys, datetime
domain = (sys.argv[1] if len(sys.argv) > 1 else 'https://aicricketcoach.app').rstrip('/')
root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PRIVATE = {'admin', 'dashboard', 'profile', 'auth', 'login', 'api', 'supabase', 'scripts', 'assets'}
urls = []
for dp, dns, fns in os.walk(root):
    dns[:] = [d for d in dns if d not in PRIVATE and not d.startswith('.')]
    for fn in fns:
        if not fn.endswith('.html'):
            continue
        rel = os.path.relpath(os.path.join(dp, fn), root).replace(os.sep, '/')
        loc = '/' + rel[:-len('index.html')] if rel.endswith('index.html') else '/' + rel
        mtime = datetime.date.fromtimestamp(os.path.getmtime(os.path.join(dp, fn))).isoformat()
        urls.append((loc, mtime))
urls.sort(key=lambda u: (u[0] != '/', u[0]))
out = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">']
for loc, lm in urls:
    out.append(f'  <url><loc>{domain}{loc}</loc><lastmod>{lm}</lastmod></url>')
out.append('</urlset>')
open(os.path.join(root, 'sitemap.xml'), 'w').write('\n'.join(out) + '\n')
print(f'Wrote sitemap.xml with {len(urls)} URLs')
