import re
import os

html_path = 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

# The list of 19 images
images = [
    "Screenshot 2026-01-25 201830.png",
    "Screenshot 2026-01-26 202539.png",
    "Screenshot 2026-01-28 120654.png",
    "Screenshot 2026-02-01 131009.png",
    "Screenshot 2026-02-15 165858.png",
    "Screenshot 2026-03-01 165456.png",
    "Screenshot 2026-03-10 142340.png",
    "Screenshot 2026-03-10 142454.png",
    "Screenshot 2026-03-15 152803.png",
    "Screenshot 2026-03-29 092533.png",
    "Screenshot 2026-03-29 094312.png",
    "Screenshot 2026-03-29 103524.png",
    "Screenshot 2026-06-01 123210.png",
    "Screenshot 2026-06-01 135238.png",
    "Screenshot 2026-06-06 183827.png",
    "Screenshot 2026-06-08 194407.png",
    "Screenshot 2026-06-08 194926.png",
    "Screenshot 2026-07-22 102620.png",
    "Screenshot 2026-07-27 195917.png"
]

# Find all img src in the certs grid
# The pattern is `<img src="assets/certs/..."`
pattern = r'(<img src=")assets/certs/[^"]+(" alt="[^"]+" onerror="this.parentElement.classList.add\(\'no-img\'\)">)'

matches = re.finditer(pattern, html)
new_html = html
offset = 0

for i, match in enumerate(matches):
    if i < len(images):
        new_src = f"assets/certs/{images[i]}"
        replacement = match.group(1) + new_src + match.group(2)
        
        start = match.start() + offset
        end = match.end() + offset
        
        new_html = new_html[:start] + replacement + new_html[end:]
        offset += len(replacement) - (match.end() - match.start())

# Add FreeCodeCamp Certification HTML
fcc_html = """
      <!-- ========== FREECODECAMP ========== -->
      <div class="cert-card reveal" data-issuer="freecodecamp">
        <div class="cert-badge">
          <div class="cert-issuer-logo" style="background:#0a0a23;color:#fff;font-size:10px;">FCC</div>
        </div>
        <div class="cert-image-slot" data-cert="fcc-rwd">
          <img src="assets/certs/fcc-rwd.png" alt="Responsive Web Design" onerror="this.parentElement.classList.add('no-img')">
          <div class="cert-img-placeholder">📜<span>RWD</span></div>
        </div>
        <h3 class="cert-name">Responsive Web Design</h3>
        <div class="cert-issuer">FreeCodeCamp</div>
        <div class="cert-meta">
          <span class="cert-date">Issued -</span>
        </div>
        <div class="cert-skills">
          <span class="cert-skill-tag">HTML</span>
          <span class="cert-skill-tag">CSS</span>
          <span class="cert-skill-tag">Web Design</span>
        </div>
        <a href="https://www.freecodecamp.org/certification/mshawki/responsive-web-design" target="_blank" class="cert-link">
          Show Credential
          <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 13v6a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h6"/><polyline points="15,3 21,3 21,9"/><line x1="10" y1="14" x2="21" y2="3"/></svg>
        </a>
      </div>
"""

# Insert the FCC card right before the closing </div> of certs-grid
grid_end = new_html.find('    </div>\n\n    <!-- ===================== REVIEWS ===================== -->')
if grid_end != -1:
    new_html = new_html[:grid_end] + fcc_html + new_html[grid_end:]
else:
    # fallback insertion point
    grid_end = new_html.find('</section>', new_html.find('id="certifications"'))
    new_html = new_html[:grid_end-10] + fcc_html + new_html[grid_end-10:]


# Also add a filter for freecodecamp
filter_html = '      <button class="cert-filter" data-filter="freecodecamp">FreeCodeCamp</button>\n    </div>\n\n    <div class="certs-grid">'
new_html = new_html.replace('    </div>\n\n    <div class="certs-grid">', filter_html)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)
print("Updated HTML with images and FreeCodeCamp cert!")
