import re

html_path = 'index.html'
with open(html_path, 'r', encoding='utf-8') as f:
    html = f.read()

mapping = {
  "Foundations: Data, Data, Everywhere": "Screenshot 2026-01-25 201830.png",
  "Ask Questions to Make Data-Driven Decisions": "Screenshot 2026-01-26 202539.png",
  "Prepare Data for Exploration": "Screenshot 2026-01-28 120654.png",
  "Process Data from Dirty to Clean": "Screenshot 2026-02-01 131009.png",
  "Analyze Data to Answer Questions": "Screenshot 2026-02-15 165858.png",
  "Share Data Through the Art of Visualization": "Screenshot 2026-03-01 165456.png",
  "Data Analysis with R Programming": "Screenshot 2026-03-10 142340.png",
  "Google Data Analytics Capstone: Complete a Case Study": "Screenshot 2026-03-10 142454.png",
  "Google Data Analytics": "Screenshot 2026-03-15 152803.png",
  "Foundations of Data Science": "Screenshot 2026-03-29 092533.png",
  "Go Beyond the Numbers: Translate Data into Insights": "Screenshot 2026-03-29 094312.png",
  "The Power of Statistics": "Screenshot 2026-03-29 103524.png",
  "Regression Analysis: Simplify Complex Data Relationships": "Screenshot 2026-06-01 123210.png",
  "The Nuts and Bolts of Machine Learning": "Screenshot 2026-06-01 135238.png",
  "Google Advanced Data Analytics": "Screenshot 2026-06-06 183827.png",
  "Microsoft Certified: Power BI Data Analyst Associate": "Screenshot 2026-06-08 194407.png",
  "DATA ANALYST L2": "Screenshot 2026-06-08 194926.png",
  "DATA ANALYST L1": "Screenshot 2026-07-22 102620.png",
  "Delivering Quality Work with Agility": "Screenshot 2026-07-27 195917.png"
}

# The regex to find each card
card_pattern = r'(<div class="cert-card.*?)(</div>\s*</div>\s*(?:<!--|</div>|$))'
# Wait, parsing HTML with regex is tricky. 
# It's better to split by `<div class="cert-card` and process each block.
blocks = html.split('<div class="cert-card')
new_blocks = [blocks[0]]

for block in blocks[1:]:
    # Find cert name
    name_match = re.search(r'<h3 class="cert-name">(.*?)</h3>', block)
    if name_match:
        cert_name = name_match.group(1).strip()
        # Find img tag
        if cert_name in mapping:
            new_src = f"assets/certs/{mapping[cert_name]}"
            block = re.sub(r'<img src="assets/certs/[^"]+"', f'<img src="{new_src}"', block)
        else:
            # Leave existing or set placeholder if no mapping (e.g. FCC or missing)
            pass
    new_blocks.append(block)

new_html = '<div class="cert-card'.join(new_blocks)

with open(html_path, 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Mapping applied successfully.")
