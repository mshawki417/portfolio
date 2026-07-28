import re

html_path = "index.html"
with open(html_path, "r", encoding="utf-8") as f:
    html = f.read()

def replace_image_for_cert(html, cert_title, new_filename):
    # Find the cert-name
    search = f'<h3 class="cert-name">{cert_title}</h3>'
    idx = html.find(search)
    if idx == -1:
        print(f"Not found: {cert_title}")
        return html
    
    card_start = html.rfind('<div class="cert-card', 0, idx)
    img_slot_idx = html.find('<div class="cert-image-slot"', card_start, idx)
    
    img_tag = (
        f'<div class="cert-image-slot">\n'
        f'          <img src="assets/certs/{new_filename}" alt="{cert_title}" '
        f'onerror="this.parentElement.classList.add(\'no-img\')">\n'
        f'          <div class="cert-img-placeholder"><span>🎓</span></div>\n'
        f'        </div>'
    )
    
    if img_slot_idx != -1:
        slot_end = html.find('</div>', img_slot_idx)
        slot_end = html.find('</div>', slot_end + 1)
        slot_end = html.find('</div>', slot_end + 1)
        html = html[:img_slot_idx] + img_tag + html[slot_end + 6:]
        print(f"Updated {cert_title}")
    else:
        html = html[:idx] + "  " + img_tag + "\n        " + html[idx:]
        print(f"Inserted {cert_title}")
    
    return html

def remove_image_from_cert(html, cert_title):
    search = f'<h3 class="cert-name">{cert_title}</h3>'
    idx = html.find(search)
    if idx == -1:
        print(f"Not found: {cert_title}")
        return html
    
    card_start = html.rfind('<div class="cert-card', 0, idx)
    img_slot_idx = html.find('<div class="cert-image-slot"', card_start, idx)
    if img_slot_idx != -1:
        slot_end = html.find('</div>', img_slot_idx)
        slot_end = html.find('</div>', slot_end + 1)
        slot_end = html.find('</div>', slot_end + 1)
        # Replace with empty placeholder
        empty_slot = (
            f'<div class="cert-image-slot">\n'
            f'          <div class="cert-img-placeholder"><span>🎓</span></div>\n'
            f'        </div>'
        )
        html = html[:img_slot_idx] + empty_slot + html[slot_end + 6:]
        print(f"Removed image from {cert_title}")
    return html

html = replace_image_for_cert(html, "DATA ANALYST L1", "Screenshot 2026-07-28 105222.png")
html = replace_image_for_cert(html, "DATA ANALYST L2", "Screenshot 2026-07-28 105204.png")
html = replace_image_for_cert(html, "Process Data from Dirty to Clean", "Screenshot 2026-02-01 131009.png")
html = remove_image_from_cert(html, "Accelerate Your Job Search with AI")

with open(html_path, "w", encoding="utf-8") as f:
    f.write(html)
