# 🖼️ Wagtail Image From URL

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/)
[![Django Version](https://img.shields.io/badge/django-4.2%2B-green.svg)](https://www.djangoproject.com/)
[![Wagtail Version](https://img.shields.io/badge/wagtail-5.0%2B-teal.svg)](https://wagtail.org/)

A powerful and user-friendly Wagtail plugin that enables you to import images directly from URLs into your Wagtail image library without the need to manually download them first. Perfect for content editors who need to quickly add images from external sources.

---

## ✨ Features

### 🚀 Core Functionality
- **Bulk URL Import**: Add multiple images simultaneously by providing multiple URLs
- **Direct Integration**: Seamlessly integrates into the Wagtail admin interface
- **Real-time Feedback**: Inline status indicators show success/failure for each URL
- **Beautiful UI**: Modern, responsive design with smooth animations and transitions
- **Smart Validation**: Client-side and server-side URL validation

### 🔒 Security & Performance
- **SSRF Protection**: Built-in protection against Server-Side Request Forgery attacks
- **Private IP Blocking**: Prevents requests to private, loopback, and reserved IP addresses
- **File Size Limits**: Configurable maximum file size (default: 10MB)
- **Format Validation**: Supports AVIF, GIF, JPEG, JPG, PNG, and WEBP formats
- **Image Verification**: Uses Pillow to verify image integrity before saving
- **Timeout Protection**: Request timeouts to prevent hanging operations

### 🎨 User Experience
- **Intuitive Interface**: Clean, modern UI that follows Wagtail design patterns
- **Batch Processing**: Submit multiple URLs with a single click
- **Dynamic Field Management**: Add or remove URL fields on the fly
- **Visual Feedback**: Success/error messages with icons
- **Responsive Design**: Works perfectly on desktop and mobile devices
- **No Page Reload**: AJAX-based submission for smooth user experience

---

## 📋 Requirements

- **Python**: 3.10 or higher
- **Django**: 4.2 or higher
- **Wagtail**: 5.0 or higher
- **Additional Dependencies**:
  - `requests` - For HTTP operations
  - `Pillow` - For image validation and processing

---

## 📦 Installation

### Step 1: Install the Package

Install directly from GitHub using pip:

```bash
pip install git+https://github.com/awais786/wagtail-image-from-url.git@main
```

### Step 2: Add to Installed Apps

Add `image_url_upload` to your Django `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    # ... other apps
    'wagtail.contrib.forms',
    'wagtail.contrib.redirects',
    'wagtail.embeds',
    'wagtail.sites',
    'wagtail.users',
    'wagtail.snippets',
    'wagtail.documents',
    'wagtail.images',
    'wagtail.search',
    'wagtail.admin',
    'wagtail',
    
    'image_url_upload',  # ← Add this line
    
    # ... other apps
]
```

### Step 3: Run Migrations (if needed)

```bash
python manage.py migrate
```

### Step 4: Collect Static Files

```bash
python manage.py collectstatic --noinput
```

---

## 🎯 Usage

### Quick Start

1. **Navigate to Images**: Go to the Wagtail admin and click on "Images" in the sidebar

2. **Click "Add an Image from URL"**: You'll see a new button in the images index page header

   ![Add Image Button](https://github.com/user-attachments/assets/f7b76caa-c349-4b9e-8205-1c6cedff71a9)

3. **Enter Image URLs**: 
   - Enter one or more image URLs
   - Click "Add Another URL" to add more fields
   - Remove unwanted fields using the trash icon

4. **Fetch Images**: Click the "Fetch All Images" button to import all images at once

   ![Add Images Form](https://github.com/user-attachments/assets/639dd436-bde7-4bf4-bac0-dd710a63e728)

5. **View Results**: See real-time status updates next to each URL field

### Supported URL Examples

```
✅ https://example.com/image.jpg
✅ https://cdn.example.com/photos/2024/picture.png
✅ https://images.example.com/photo.webp
✅ https://example.com/assets/image.avif
```

### Supported Image Formats

- **AVIF** (.avif)
- **GIF** (.gif)
- **JPEG** (.jpg, .jpeg)
- **PNG** (.png)
- **WEBP** (.webp)

---

## ⚙️ Configuration

### Optional Settings

You can customize the behavior by adding these settings to your Django `settings.py`:

```python
# Maximum file size in bytes (default: 10MB)
IMAGE_URL_UPLOAD_MAX_SIZE = 10 * 1024 * 1024

# Request timeout in seconds (connect, read)
IMAGE_URL_UPLOAD_TIMEOUT = (5, 15)

# Allowed image formats
IMAGE_URL_UPLOAD_FORMATS = {'avif', 'gif', 'jpeg', 'jpg', 'png', 'webp'}
```

---

## 🔧 Advanced Usage

### Custom Image Collection

Images are added to the default collection. To specify a different collection, you can extend the view:

```python
# In your app's views.py
from image_url_upload.views import AddFromURLView

class CustomAddFromURLView(AddFromURLView):
    def post(self, request):
        # Your custom logic here
        return super().post(request)
```

### Image Metadata

The plugin automatically:
- Sets the image title from the URL filename
- Records the uploading user (if authenticated)
- Generates a unique filename using UUID

---

## 🛡️ Security Features

### SSRF Protection

The plugin includes comprehensive Server-Side Request Forgery (SSRF) protection:

- ✅ Blocks requests to private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- ✅ Blocks loopback addresses (127.0.0.0/8, ::1)
- ✅ Blocks reserved IP ranges
- ✅ Blocks multicast addresses
- ✅ Validates DNS resolution to prevent DNS rebinding attacks

### Content Validation

- ✅ Verifies Content-Type headers
- ✅ Validates image format using Pillow
- ✅ Enforces file size limits
- ✅ Prevents malformed image uploads

### Request Safety

- ✅ Configurable connection and read timeouts
- ✅ Streaming downloads to manage memory
- ✅ Error handling for network failures

---

## 🧪 Testing

The project includes comprehensive tests. To run them:

```bash
# Install development dependencies
pip install pytest pytest-django coverage

# Run tests
pytest

# Run with coverage
pytest --cov=image_url_upload --cov-report=html
```

### Test Coverage

The plugin includes tests for:
- ✅ Form validation
- ✅ URL validation and SSRF protection
- ✅ Image download and processing
- ✅ View functionality
- ✅ Wagtail hooks integration

---

## 🐛 Troubleshooting

### Common Issues

#### Issue: "Blocked for security reasons"
**Cause**: The URL points to a private or reserved IP address.
**Solution**: Only use public URLs. This is a security feature to prevent SSRF attacks.

#### Issue: "Image too large"
**Cause**: The image exceeds the maximum file size limit (default: 10MB).
**Solution**: Use a smaller image or increase `IMAGE_URL_UPLOAD_MAX_SIZE` in settings.

#### Issue: "Invalid Content-Type"
**Cause**: The URL doesn't return an image content type.
**Solution**: Ensure the URL points directly to an image file, not an HTML page.

#### Issue: "Unsupported format"
**Cause**: The image format is not in the allowed list.
**Solution**: Convert the image to a supported format (AVIF, GIF, JPEG, PNG, WEBP).

#### Issue: "Could not fetch image headers"
**Cause**: Network error, timeout, or invalid URL.
**Solution**: Check your internet connection and verify the URL is accessible.

---

## 📚 API Reference

### Views

#### `AddFromURLView`
Handles the bulk image import from URLs.

**Endpoint**: `/admin/images/add-from-url/`
**Method**: POST
**Parameters**:
- `url` (string): The image URL to fetch
- `collection` (int, optional): Collection ID (default: 1)

**Response**: JSON
```json
{
    "success": true,
    "image": {
        "id": 123,
        "title": "image.jpg",
        "url": "/media/images/image.jpg"
    }
}
```

### Forms

#### `ImageURLForm`
Validates image URLs before processing.

**Fields**:
- `image_url` (URLField): The URL of the image to import

### Utilities

#### `get_image_from_url(url, user=None)`
Downloads and creates a Wagtail image from a URL.

**Parameters**:
- `url` (str): The image URL
- `user` (User, optional): The user uploading the image

**Returns**: `Image` object

**Raises**:
- `ValidationError`: If the URL is invalid or blocked
- `RequestException`: If the download fails

#### `validate_image_url(url)`
Performs lightweight validation before downloading.

**Parameters**:
- `url` (str): The URL to validate

**Raises**: `ValidationError` if validation fails

---

## 🤝 Contributing

Contributions are welcome! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**: Follow the existing code style
4. **Run tests**: Ensure all tests pass
5. **Commit your changes**: `git commit -m 'Add amazing feature'`
6. **Push to the branch**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Development Setup

```bash
# Clone the repository
git clone https://github.com/awais786/wagtail-image-from-url.git
cd wagtail-image-from-url

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

### Code Style

- Follow PEP 8 guidelines
- Use Black for code formatting (line length: 120)
- Write docstrings for public functions
- Add tests for new features

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors & Contributors

- **Awais Qureshi** - *Initial work* - [@awais786](https://github.com/awais786)

See also the list of [contributors](https://github.com/awais786/wagtail-image-from-url/contributors) who participated in this project.

---

## 🙏 Acknowledgments

- Built for the [Wagtail CMS](https://wagtail.org/) community
- Inspired by the need for faster content management workflows
- Special thanks to all contributors and users

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/awais786/wagtail-image-from-url/issues)
- **Discussions**: [GitHub Discussions](https://github.com/awais786/wagtail-image-from-url/discussions)
- **Wagtail Slack**: Find us in the [#packages channel](https://wagtail.org/slack/)

---

## 🗺️ Roadmap

### Planned Features

- [ ] Support for custom image collections selection
- [ ] Bulk upload progress indicator
- [ ] Image preview before import
- [ ] Import from CSV file containing multiple URLs
- [ ] Support for authenticated image sources
- [ ] Image metadata extraction from EXIF data
- [ ] Duplicate detection by image hash
- [ ] Integration with cloud storage providers

---

## 📊 Changelog

### Version 0.1.0 (Current)
- ✨ Initial release
- ✅ Bulk URL import functionality
- ✅ SSRF protection
- ✅ Modern UI with Tailwind CSS
- ✅ Real-time status feedback
- ✅ Support for multiple image formats

---

## 🔗 Related Projects

- [Wagtail](https://github.com/wagtail/wagtail) - The CMS this plugin extends
- [Django](https://github.com/django/django) - The web framework
- [Pillow](https://github.com/python-pillow/Pillow) - Image processing library

---

<div align="center">

**Made with ❤️ for the Wagtail community**

[⭐ Star on GitHub](https://github.com/awais786/wagtail-image-from-url) | [🐛 Report Bug](https://github.com/awais786/wagtail-image-from-url/issues) | [💡 Request Feature](https://github.com/awais786/wagtail-image-from-url/issues)

</div>
