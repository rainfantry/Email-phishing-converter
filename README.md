# Email-phishing-converter
.eml to .html converter with LinkedIn anti-image scraping defeating capability

🔒 All techniques shown are for authorised testing and security awareness only. 

Video demonstration

https://youtu.be/FJntEY91Arg?si=p9Z9AyiYMzACSlYU

while I share this my family is starving and old man is dying from 5x bypass surgery as I try to get a helpdesk traineeship but dont have 2 years IT experience. yet i continue to spread awareness where others dont. You learn this so you understand the criminal mindset so you can protect your company

https://buymeacoffee.com/rainfantry

https://22div.com.au

If you are a Sydney based IT/CSEC company that can train me or give an internship, anything so I can help my father - contact me at contact@22div.com.au or gwu0738@gmail.com


# eml2html

Convert .eml email files to clean, self-contained HTML for phishing.

## Features

- Extracts HTML from .eml files
- **Inlines all images as base64** (no external requests)
- Removes tracking pixels
- Strips UTM parameters
- Adds `{{PLACEHOLDERS}}` for customization
- Single file output - just copy/paste

## Usage

```bash
# Basic - outputs email_clean.html
python3 eml2html.py email.eml

# Custom output
python3 eml2html.py email.eml output.html

# Keep image URLs (don't inline)
NO_INLINE=1 python3 eml2html.py email.eml

# No placeholders
NO_PLACEHOLDERS=1 python3 eml2html.py email.eml
```

## Output

Single HTML file with:
- All images embedded as base64 data URIs
- Tracking pixels removed
- Links replaced with `{{MAIN_URL}}`, `{{UNSUBSCRIBE}}`
- Ready to copy into email sender

## Example

```bash
$ python3 eml2html.py "Secure your wallet.eml"
[+] From: Exodus Newsletter <newsletter@exodus.com>
[+] Subject: Tip 1 of 3: Secure your wallet
[+] Found HTML: 72381 bytes
[+] Cleaning...
  [*] Inlining: https://...logo.png
  [*] Inlining: https://...header.jpg
[+] Saved: Secure your wallet_clean.html (401808 bytes)
```

## Why Base64 Inline?

- **Self-contained** - one file, no dependencies
- **Copy/paste ready** - works in any email sender
- **No hosting needed** - images are in the HTML
- **Offline** - works without internet after conversion

# LICENCE
MIT
i dont GAF 
