# Build and Publish Instructions

## Problem Solved

The package was failing to publish to PyPI with the error:
```
InvalidDistribution: Metadata is missing required fields: Name, Version.
```

This was caused by using `setuptools>=68.0` which generated `Metadata-Version: 2.4`, which is not yet fully supported by PyPI's validation tools.

## Solution

1. **Constrained setuptools version**: Changed from `setuptools>=68.0` to `setuptools>=61.0,<70.0`
   - This ensures Metadata-Version 2.1 is used instead of 2.4
   - Version 2.1 is fully compatible with PyPI

2. **Added proper dependencies**: Added `requests` and `Pillow` to dependencies
   - These are required by the application but were missing

3. **Updated GitHub Actions workflow**:
   - Added `twine check` step to validate packages before publishing
   - Pinned setuptools version to match pyproject.toml
   - Added debugging output to inspect package contents

## Building Locally

To build the package locally:

```bash
# Clean previous builds
rm -rf dist/ build/ *.egg-info/

# Install build tools with correct versions
pip install build "setuptools>=61.0,<70.0" wheel

# Build the package
python -m build

# Verify the package
pip install twine
twine check dist/*
```

## Expected Output

After building, you should see:
- `dist/wagtail_image_from_url-1.0.0-py3-none-any.whl`
- `dist/wagtail_image_from_url-1.0.0.tar.gz`

The PKG-INFO should show:
- `Metadata-Version: 2.1` (not 2.4)
- `Name: wagtail-image-from-url`
- `Version: 1.0.0`

## Publishing to PyPI

The package is automatically published when you create a new GitHub release:

1. Go to GitHub repository
2. Create a new release with a tag (e.g., `v1.0.0`)
3. Publish the release
4. GitHub Actions will automatically build and publish to PyPI

## Manual Publishing (if needed)

```bash
# Build the package first
python -m build

# Check the package
twine check dist/*

# Upload to TestPyPI first (recommended)
twine upload --repository testpypi dist/*

# If successful, upload to PyPI
twine upload dist/*
```

## Verification

After publishing, verify the package is available:

```bash
pip install wagtail-image-from-url
```

Or from a specific index:

```bash
pip install --index-url https://test.pypi.org/simple/ wagtail-image-from-url
```

