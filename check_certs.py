#!/usr/bin/env python3
"""Add Process Data from Dirty to Clean image and fix L1/L2 assignments."""
import re, sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def fix_certs():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Check current state of all cert cards
    cert_cards = re.findall(r'<h3 class="cert-name">(.*?)</h3>', html)
    print(f"Found {len(cert_cards)} cert cards:")
    for c in cert_cards:
        print(f"  - {c}")
    
    # Check which cards have images
    print("\nCards with images:")
    for m in re.finditer(r'<img src="(assets/certs/[^"]+)" alt="([^"]*)"', html):
        print(f"  {m.group(2)} -> {m.group(1)}")
    
    # Check L1 and L2 specifically
    print("\n--- L1/L2 status ---")
    l1_idx = html.find('DATA ANALYST L1')
    l2_idx = html.find('DATA ANALYST L2')
    if l1_idx > 0:
        # Get surrounding 300 chars
        start = max(0, l1_idx - 300)
        print(f"L1 context: ...{html[start:l1_idx+50]}...")
    if l2_idx > 0:
        start = max(0, l2_idx - 300)
        print(f"L2 context: ...{html[start:l2_idx+50]}...")
    
    # Check Process Data from Dirty to Clean
    pdc_idx = html.find('Process Data from Dirty to Clean')
    if pdc_idx > 0:
        start = max(0, pdc_idx - 300)
        print(f"\nDirty to Clean context: ...{html[start:pdc_idx+50]}...")
    else:
        print("\nProcess Data from Dirty to Clean NOT FOUND in HTML!")

if __name__ == '__main__':
    fix_certs()
