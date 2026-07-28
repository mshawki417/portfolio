#!/usr/bin/env python3
"""Fix the swapped images: 
- Process Data from Dirty to Clean -> Screenshot 2026-02-22 142401.png
- Accelerate Your Job Search with AI -> Screenshot 2026-02-01 131009.png
"""
import sys
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()
    
    # Fix: Process Data from Dirty to Clean currently points to 131009 (which is "Accelerate")
    # Should point to 142401
    old_dirty = 'src="assets/certs/Screenshot 2026-02-01 131009.png" alt="Process Data from Dirty to Clean"'
    new_dirty = 'src="assets/certs/Screenshot 2026-02-22 142401.png" alt="Process Data from Dirty to Clean"'
    
    if old_dirty in html:
        html = html.replace(old_dirty, new_dirty)
        print("Fixed: Process Data from Dirty to Clean -> 142401")
    else:
        print("Warning: could not find old Dirty to Clean reference")
        # Try alternate pattern
        idx = html.find('Process Data from Dirty to Clean')
        if idx > 0:
            # Find the img tag before this heading
            card_start = html.rfind('<div class="cert-card', 0, idx)
            img_idx = html.find('src="assets/certs/', card_start, idx)
            if img_idx > 0:
                img_end = html.find('"', img_idx + 19)
                old_src = html[img_idx:img_end+1]
                new_src = 'src="assets/certs/Screenshot 2026-02-22 142401.png"'
                html = html[:img_idx] + new_src + html[img_end+1:]
                print(f"Fixed via search: replaced {old_src}")
    
    # Fix: Accelerate Your Job Search with AI should point to 131009
    # Check if it currently has an image
    acc_idx = html.find('Accelerate Your Job Search with AI')
    if acc_idx > 0:
        card_start = html.rfind('<div class="cert-card', 0, acc_idx)
        img_check = html.find('src="assets/certs/', card_start, acc_idx)
        if img_check > 0:
            print(f"Accelerate already has an image")
        else:
            # Need to add image slot
            slot_idx = html.find('<div class="cert-image-slot"', card_start, acc_idx)
            if slot_idx > 0:
                # Replace the empty slot with one containing the image
                slot_end = html.find('</div>', slot_idx)
                new_slot = '<div class="cert-image-slot">\n          <img src="assets/certs/Screenshot 2026-02-01 131009.png" alt="Accelerate Your Job Search with AI" onerror="this.parentElement.classList.add(\'no-img\')">\n          <div class="cert-img-placeholder"><span>🎓</span></div>'
                html = html[:slot_idx] + new_slot + html[slot_end:]
                print("Added image to Accelerate Your Job Search with AI")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("Saved!")

if __name__ == '__main__':
    fix()
