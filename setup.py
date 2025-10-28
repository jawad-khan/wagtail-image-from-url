"""
Wagtail Image From URL - A plugin to import images from URLs into Wagtail CMS.
"""

from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wagtail-image-from-url",
    version="0.1.0",
    description="Add images to Wagtail via URL - A production-ready plugin for importing images from external URLs",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Awais Qureshi",
    author_email="",
    url="https://github.com/awais786/wagtail-image-from-url",
    project_urls={
        "Bug Reports": "https://github.com/awais786/wagtail-image-from-url/issues",
        "Source": "https://github.com/awais786/wagtail-image-from-url",
        "Documentation": "https://github.com/awais786/wagtail-image-from-url#readme",
    },
    packages=find_packages(include=["image_url_upload", "image_url_upload.*"]),
    include_package_data=True,
    install_requires=[
        "Django>=4.2",
        "Wagtail>=5.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "isort>=5.12.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-django>=4.5.0",
            "pytest-cov>=4.0.0",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Web Environment",
        "Framework :: Django",
        "Framework :: Django :: 4.2",
        "Framework :: Django :: 5.0",
        "Framework :: Wagtail",
        "Framework :: Wagtail :: 5",
        "Framework :: Wagtail :: 6",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.10",
    keywords="wagtail django cms image upload url import",
    license="MIT",
    zip_safe=False,
)
