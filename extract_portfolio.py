import re

print("Reading local bundle.js...")
try:
    with open("bundle.js", "r", encoding="utf-8") as f:
        content = f.read()
    print("Read completed. Parsing content...")
except Exception as e:
    print(f"Error reading file: {e}")
    content = ""

if content:
    # Find all strings in double quotes, single quotes, or backticks
    # We want text strings, specifically those with letters and spaces
    strings = re.findall(r'"([^"\\]*(?:\\.[^"\\]*)*)"|\'([^\'\\]*(?:\\.[^\'\\]*)*)\'', content)
    
    extracted_text = []
    for s1, s2 in strings:
        text = s1 or s2
        # Clean up escapes
        text = text.replace('\\"', '"').replace("\\'", "'").replace('\\n', ' ').strip()
        # Filter for readable English strings (longer than 10 chars, containing spaces)
        if len(text) > 8 and ' ' in text and not text.startswith('http') and not text.startswith('svg') and not text.startswith('path'):
            # Basic validation to avoid pure code/selectors
            if re.search(r'[a-zA-Z]{3,}', text) and not re.search(r'[{}\[\]();=,]', text):
                extracted_text.append(text)
                
    # Remove duplicates
    unique_text = []
    seen = set()
    for text in extracted_text:
        if text.lower() not in seen:
            seen.add(text.lower())
            unique_text.append(text)
            
    print(f"Extracted {len(unique_text)} unique text strings:")
    print("=" * 60)
    for t in unique_text:
        print(f"- {t}")
    print("=" * 60)
    
    # Save results
    with open("extracted_strings.txt", "w", encoding="utf-8") as f:
        f.write("\n".join(unique_text))
    print("Saved extracted strings to C:\\Users\\Admin\\.gemini\\antigravity\\scratch\\portfolio\\extracted_strings.txt")
else:
    print("No content to parse.")
