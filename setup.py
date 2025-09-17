from setuptools import find_packages, setup

setup(
    name="image-url-upload",
    version="0.1.0",
    description="Add images to Wagtail via URL",
    author="Awais Qureshi",
    packages=find_packages(include=["image_url_upload", "image_url_upload.*"]),
    include_package_data=True,  # ✅ includes templates and static files
    install_requires=[
        "Django>=4.2",
        "Wagtail>=5.0",
        "requests",
    ],
    classifiers=[
        "Framework :: Django",
        "Framework :: Wagtail",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10",
)
