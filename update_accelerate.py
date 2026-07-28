#!/usr/bin/env python3
"""Update Accelerate Your Job Search with AI image."""

def update_cert():
    with open('index.html', 'r', encoding='utf-8') as f:
        html = f.read()

    # Find the comment marking the certificate
    marker = '<!-- ========== GOOGLE: Accelerate Job Search with AI ========== -->'
    idx = html.find(marker)
    
    if idx != -1:
        # Find the next cert-image-slot
        slot_idx = html.find('<div class="cert-image-slot">', idx)
        if slot_idx != -1:
            slot_end = html.find('</div>', slot_idx)
            # Find the closing tag of the placeholder div if it exists
            next_div = html.find('</div>', slot_end + 1)
            
            # The current content might have placeholder or an empty slot
            # Let's replace the whole cert-image-slot block
            
            # Look for the start of the next element after the slot (usually h3 cert-name)
            h3_idx = html.find('<h3 class="cert-name">', slot_idx)
            
            if h3_idx != -1:
                # Replace everything between the start of the slot and the h3 tag
                new_slot = '<div class="cert-image-slot">\n          <img src="assets/certs/Screenshot 2026-07-28 121659.png" alt="Accelerate Your Job Search with AI" onerror="this.parentElement.classList.add(\'no-img\')">\n        </div>\n        '
                html = html[:slot_idx] + new_slot + html[h3_idx:]
                print("Replaced cert-image-slot for Accelerate.")
            else:
                print("Could not find h3 after slot")
        else:
            print("Could not find cert-image-slot after marker")
    else:
        print("Could not find marker")

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print("HTML updated.")

if __name__ == '__main__':
    update_cert()
