
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
