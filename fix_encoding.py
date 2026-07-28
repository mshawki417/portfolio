#!/usr/bin/env python3
"""Fix broken emoji sequences in index.html - run and save without printing emojis."""

import re, sys

# Force stdout to handle all Unicode
sys.stdout.reconfigure(encoding='utf-8', errors='replace')

def fix():
    with open('index.html', 'r', encoding='utf-8') as f:
        text = f.read()
    
    cp1252_map = {
        0x20AC: 0x80, 0x201A: 0x82, 0x0192: 0x83, 0x201E: 0x84,
        0x2026: 0x85, 0x2020: 0x86, 0x2021: 0x87, 0x02C6: 0x88,
        0x2030: 0x89, 0x0160: 0x8A, 0x2039: 0x8B, 0x0152: 0x8C,
        0x017D: 0x8E, 0x2018: 0x91, 0x2019: 0x92, 0x201C: 0x93,
        0x201D: 0x94, 0x2022: 0x95, 0x2013: 0x96, 0x2014: 0x97,
        0x02DC: 0x98, 0x2122: 0x99, 0x0161: 0x9A, 0x203A: 0x9B,
        0x0153: 0x9C, 0x017E: 0x9E, 0x0178: 0x9F,
    }
    
    def char_to_byte(c):
        code = ord(c)
        if code < 0x80:
            return code
        if code <= 0xFF and code not in range(0x80, 0xA0):
            return code
        if code in cp1252_map:
            return cp1252_map[code]
        return None
    
    result = []
    i = 0
    fixes = 0
    
    while i < len(text):
        c = text[i]
        byte_val = char_to_byte(c)
        
        if byte_val is not None and byte_val >= 0xC0:
            if byte_val >= 0xF0:
                expected_len = 4
            elif byte_val >= 0xE0:
                expected_len = 3
            elif byte_val >= 0xC0:
                expected_len = 2
            else:
                result.append(c)
                i += 1
                continue
            
            if i + expected_len <= len(text):
                byte_seq = bytearray()
                valid = True
                for k in range(expected_len):
                    bv = char_to_byte(text[i + k])
                    if bv is None:
                        valid = False
                        break
                    byte_seq.append(bv)
                
                if valid:
                    try:
                        decoded = bytes(byte_seq).decode('utf-8')
                        result.append(decoded)
                        fixes += 1
                        i += expected_len
                        continue
                    except UnicodeDecodeError:
                        pass
        
        result.append(c)
        i += 1
    
    fixed = ''.join(result)
    print(f"Applied {fixes} encoding fixes")
    
    # Verify beyond-icon content
    for m in re.finditer(r'beyond-icon">(.*?)</div>', fixed):
        content = m.group(1)
        hex_repr = ' '.join(f'U+{ord(c):04X}' for c in content)
        print(f"  icon: {hex_repr}")
    
    # Check title
    for m in re.finditer(r'<title>(.*?)</title>', fixed):
        print(f"  title chars: {' '.join(f'U+{ord(c):04X}' for c in m.group(1))}")
    
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(fixed)
    print("Saved fixed index.html!")

if __name__ == '__main__':
    fix()
