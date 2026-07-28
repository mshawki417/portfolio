#!/usr/bin/env python3
import re
with open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

certs = re.findall(r'<h3 class="cert-name">(.*?)</h3>', html)
for i, c in enumerate(certs):
    print(f"{i+1}: {c}")

print("Check Accelerate comment:")
idx = html.find('Accelerate Job Search with AI')
if idx != -1:
    print(html[idx-50:idx+200])
