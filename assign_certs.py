import re

# Verified mapping from visual inspection
# filename -> certificate title shown in image
IMAGE_MAP = {
    "Foundations: Data, Data, Everywhere": "Screenshot 2026-01-25 201830.png",
    "Delivering Quality Work with Agility": "Screenshot 2026-01-26 202539.png",
    "Ask Questions to Make Data-Driven Decisions": "Screenshot 2026-01-28 120654.png",
    "Accelerate Your Job Search with AI": "Screenshot 2026-02-01 131009.png",
    "Prepare Data for Exploration": "Screenshot 2026-02-15 165858.png",
    "Analyze Data to Answer Questions": "Screenshot 2026-03-01 165456.png",
    "Share Data Through the Art of Visualization": "Screenshot 2026-03-10 142454.png",   # cleaner version
    "Data Analysis with R Programming": "Screenshot 2026-03-15 152803.png",
    "Introduction to Data Analysis Using Python": "Screenshot 2026-03-29 092533.png",
    "Google Data Analytics Capstone: Complete a Case Study": "Screenshot 2026-03-29 094312.png",
    "Google Data Analytics": "Screenshot 2026-03-29 103524.png",
    "Foundations of Data Science": "Screenshot 2026-06-01 123210.png",
    "The Power of Statistics": "Screenshot 2026-06-01 135238.png",
    "Regression Analysis: Simplify Complex Data Relationships": "Screenshot 2026-06-06 183827.png",
    "The Nuts and Bolts of Machine Learning": "Screenshot 2026-06-08 194407.png",
    "Google Advanced Data Analytics": "Screenshot 2026-06-08 194926.png",
    "Microsoft Certified: Power BI Data Analyst Associate": "Screenshot 2026-07-22 102620.png",
    "Responsive Web Design": "Screenshot 2026-07-27 195917.png",
    # DATA ANALYST L2 - no separate screenshot found, the Google Advanced DA cert is Screenshot 2026-06-08 194926
    # But the user mentioned this was Coursera DATA ANALYST L2 - we have no image for it currently
}

with open("index.html", "r", encoding="utf-8") as f:
    html = f.read()

def add_image_to_card(html, cert_title, filename):
    """Add or replace cert-image-slot for a card with given cert title."""
    # Find the cert-name for this cert
    search = f'<h3 class="cert-name">{cert_title}</h3>'
    idx = html.find(search)
    if idx == -1:
        print(f"[NOT FOUND] {cert_title}")
        return html
    
    # Look for cert-image-slot before the cert-name
    # Find the start of the cert-card containing this cert-name
    card_start_search = '<div class="cert-card'
    card_start = html.rfind(card_start_search, 0, idx)
    
    # Check if there's already an image slot between card_start and cert_name
    img_slot_idx = html.find('<div class="cert-image-slot"', card_start, idx)
    cert_badge_end = html.find('</div>', card_start, idx)
    # Find where cert-badge ends (after the logo div)
    badge_block_end = html.find('</div>\n        </div>', card_start, idx)
    
    img_tag = (
        f'\n        <div class="cert-image-slot">\n'
        f'          <img src="assets/certs/{filename}" alt="{cert_title}" '
        f'onerror="this.parentElement.classList.add(\'no-img\')">\n'
        f'          <div class="cert-img-placeholder"><span>🎓</span></div>\n'
        f'        </div>'
    )
    
    if img_slot_idx != -1:
        # Replace existing slot
        slot_end = html.find('</div>', img_slot_idx)
        slot_end = html.find('</div>', slot_end + 1)  # inner placeholder div
        slot_end = html.find('</div>', slot_end + 1)  # outer slot div
        old_slot = html[img_slot_idx:slot_end + 6]
        new_slot = (
            f'<div class="cert-image-slot">\n'
            f'          <img src="assets/certs/{filename}" alt="{cert_title}" '
            f'onerror="this.parentElement.classList.add(\'no-img\')">\n'
            f'          <div class="cert-img-placeholder"><span>🎓</span></div>\n'
            f'        </div>'
        )
        html = html[:img_slot_idx] + new_slot + html[slot_end + 6:]
        print(f"[UPDATED] {cert_title} -> {filename}")
    else:
        # Insert before the h3
        insert_pos = idx
        html = html[:insert_pos] + img_tag + "\n        " + html[insert_pos:]
        print(f"[INSERTED] {cert_title} -> {filename}")
    
    return html

for cert_title, filename in IMAGE_MAP.items():
    html = add_image_to_card(html, cert_title, filename)

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("\nDone! All images assigned.")
