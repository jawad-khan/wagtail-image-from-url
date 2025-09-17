
# Wagtail Image From URL

Add images to your Wagtail site directly from a URL without downloading them manually.
This plugin provides a simple interface in the Wagtail admin to paste an image URL and add it to your images library.

---

## Features

- Add images to Wagtail via URL
- Handles common image formats (JPEG, PNG, GIF)
- Shows success/error messages in the Wagtail admin
- Includes breadcrumbs for easy navigation

---

## Installation

Install directly from GitHub using pip:

```
bash
pip install git+https://github.com/awais786/wagtail-image-from-url.git@main
```

---
## Add to Installed Apps (Required!)

```
bash
INSTALLED_APPS = [
    ...
    "image_url_upload",  # <-- Add this line
]
```

<img width="1249" height="462" alt="Screenshot 2025-09-17 at 3 43 44 PM" src="https://github.com/user-attachments/assets/639dd436-bde7-4bf4-bac0-dd710a63e728" />

