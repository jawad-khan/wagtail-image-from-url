from setuptools import setup, find_packages

setup(
    name="image-url-upload",  # PyPI/package name
    version="0.1.0",
    packages=find_packages(include=["image_url_upload", "image_url_upload.*"]),
    include_package_data=True,  # include templates, static files
    install_requires=[
        "Django>=4.2",
        "Wagtail>=5.0",
        "requests",
    ],
    url="https://github.com/awais786/wagtail-image-from-url",
    license="MIT",
    author="Awais Qureshi",
    description="Add images to Wagtail via URL",
)
