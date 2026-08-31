#!/usr/bin/env python3
"""
EML to Phishing HTML Converter by github.com/rainfantry
- Handles quoted-printable encoding (LinkedIn, etc)
- src="" (images) → base64 inline
- href="" (links) → {{LINK}} placeholder
"""

import email
from email import policy
import re
import base64
import urllib.request
import sys
import os
import html as html_module

def download_b64(url):
    """Download image → base64 data URI"""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
            'Referer': 'https://mail.google.com/',
        }
        if 'licdn.com' in url:
            headers['Referer'] = 'https://www.linkedin.com/'
            headers['Accept'] = 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8'
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=15) as r:
            data = r.read()
            ct = r.headers.get('Content-Type', 'image/png')
            return f"data:{ct};base64,{base64.b64encode(data).decode()}"
    except Exception as e:
        print(f"  [!] Failed: {url[:60]}... ({e})")
        return None

def process_html(html):
    """Process HTML: images→base64, links→placeholder"""
    
    # Fix quoted-printable artifacts that might remain
    # =3D is actually =
    html = html.replace('=3D', '=')
    # Remove soft line breaks (=\n or = at end of line)
    html = re.sub(r'=\r?\n', '', html)
    
    cache = {}
    def get_b64(url):
        # Clean URL - decode HTML entities (&amp; → &) and strip whitespace
        url = html_module.unescape(url.strip().replace('\n', '').replace('\r', ''))
        if url in cache:
            return cache[url]
        print(f"  [img] {url[:60]}...")
        cache[url] = download_b64(url)
        return cache[url]
    
    # 1. <img src="..."> → base64
    def fix_img_src(m):
        tag = m.group(0)
        src = re.search(r'src="([^"]+)"', tag)
        if src and src.group(1).startswith('http'):
            b64 = get_b64(src.group(1))
            if b64:
                return tag.replace(src.group(1), b64)
            else:
                # Failed to download - remove the broken img
                return ''
        return tag
    
    html = re.sub(r'<img[^>]+>', fix_img_src, html, flags=re.I)
    
    # 2. CSS url(...) → base64
    def fix_css_url(m):
        url = m.group(1).strip('"\'').strip()
        if url.startswith('http'):
            b64 = get_b64(url)
            if b64:
                return f'url({b64})'
        return m.group(0)
    
    html = re.sub(r'url\(([^)]+)\)', fix_css_url, html)
    
    # 3. href="..." → {{LINK}}
    html = re.sub(r'href="https?://[^"]+"', 'href="{{LINK}}"', html)
    
    # 4. Remove any remaining external image URLs
    html = re.sub(r'<img[^>]*src="https?://[^"]*"[^>]*/?\s*>', '', html, flags=re.I)
    
    return html

def eml_to_html(eml_path, output_path=None):
    print(f"[+] Reading: {eml_path}")
    
    with open(eml_path, "rb") as f:
        msg = email.message_from_binary_file(f, policy=policy.default)
    
    print(f"[+] From: {msg['from']}")
    print(f"[+] Subject: {msg['subject']}")
    
    html = None
    for part in msg.walk():
        if part.get_content_type() == "text/html":
            html = part.get_content()
            break
    
    if not html:
        print("[-] No HTML found")
        return None
    
    print(f"[+] Processing {len(html)} bytes...")
    html = process_html(html)
    
    if not output_path:
        output_path = os.path.splitext(eml_path)[0] + "_phish.html"
    
    with open(output_path, "w") as f:
        f.write(html)
    
    # Stats
    ext_urls = len(re.findall(r'https?://', html))
    placeholders = len(re.findall(r'{{LINK}}', html))
    b64_imgs = len(re.findall(r'src="data:', html))
    
    print(f"\n[+] Saved: {output_path}")
    print(f"    Base64 images: {b64_imgs}")
    print(f"    Placeholder links: {placeholders}")
    print(f"    External URLs: {ext_urls}" + (" ⚠" if ext_urls > 0 else " ✓"))
    
    return output_path

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 eml2html.py <email.eml> [output.html]")
        sys.exit(1)
    
    eml_to_html(sys.argv[1], sys.argv[2] if len(sys.argv) > 2 else None)
