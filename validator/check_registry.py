#!/usr/bin/env python3
"""Re-check every service in registry.json and publish docs/status.html."""
import json, datetime, urllib.request, os, re

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, 'registry.json')
OUT = os.path.join(ROOT, 'docs', 'status.html')


def fetch(url):
    if not url.endswith('.txt'):
        url = url.rstrip('/') + '/.well-known/honesty.txt'
    req = urllib.request.Request(url, headers={'User-Agent': 'honestshield-registry/1.0'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.read().decode('utf-8', 'replace')


def parse(text):
    header, sections, cur = {}, {}, None
    for raw in text.split('\n'):
        line = raw.strip()
        if line.startswith('## '):
            cur = line[3:].strip().upper()
            sections[cur] = []
            continue
        if not line or line.startswith('#'):
            continue
        if cur is None:
            m = re.match(r'^([A-Za-z-]+):\s*(.*)$', line)
            if m:
                header[m.group(1)] = m.group(2)
        else:
            sections[cur].append(line)
    return header, sections


def validate(text):
    header, sections = parse(text)
    fails, warns = 0, 0
    for k in ('App', 'Host', 'Contact', 'Updated', 'Expires'):
        if k not in header:
            fails += 1
    if header.get('Expires'):
        try:
            if datetime.date.fromisoformat(header['Expires']) <= datetime.date.today():
                warns += 1
        except ValueError:
            pass
    data = sections.get('DATA', [])
    if not data:
        fails += 1
    for l in data:
        if 'purpose=' not in l:
            fails += 1
        if 'retain=' not in l:
            warns += 1
        if 'shared=' not in l:
            warns += 1
    if 'TRACKERS' not in sections:
        fails += 1
    pr = '\n'.join(sections.get('PROMISES', []))
    if not re.search(r'sell-data:\s*no', pr):
        fails += 1
    if 'delete-on-request' not in pr:
        warns += 1
    if fails:
        return 'failed'
    return 'verified' if warns == 0 else 'warnings'


def main():
    with open(REG, encoding='utf-8') as f:
        reg = json.load(f)
    now = datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M UTC')
    rows = []
    for svc in reg.get('services', []):
        name = svc.get('name', '?')
        url = svc.get('url', '')
        try:
            state = validate(fetch(url))
        except Exception:
            state = 'unreachable'
        rows.append((name, url, state))
    colors = {'verified': '#238636', 'warnings': '#9e6a03',
              'failed': '#da3633', 'unreachable': '#6e7681'}
    tr = '\n'.join(
        '<tr><td>{}</td><td><a href="{}">{}</a></td>'
        '<td><span style="background:{};padding:2px 8px;border-radius:4px">'
        '{}</span></td></tr>'.format(n, u, u, colors[s], s)
        for n, u, s in rows)
    html = '''<!DOCTYPE html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>honesty.txt — registry status</title>
<style>body{font-family:system-ui,sans-serif;background:#0d1117;color:#e6edf3;margin:0 auto;padding:24px;max-width:760px}
a{color:#58a6ff}table{width:100%;border-collapse:collapse;margin-top:12px}
td{padding:8px;border-bottom:1px solid #21262d;font-size:14px;word-break:break-all}</style>
</head><body>
<h1>honesty.txt — registry status</h1>
<p>Automated re-check of registered services. Last run: ''' + now + '''. Re-checked daily by GitHub Actions.</p>
<p>Reference: <a href="https://github.com/Julia7856/honestshield">github.com/Julia7856/honestshield</a></p>
<table><tr><td>Service</td><td>Declaration</td><td>State today</td></tr>
''' + tr + '''
</table>
</body></html>'''
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    with open(OUT, 'w', encoding='utf-8') as f:
        f.write(html)
    print('status.html written,', len(rows), 'services')


if __name__ == '__main__':
    main()
