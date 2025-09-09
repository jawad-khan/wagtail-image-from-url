from setuptools import setup, find_packages

setup(
    name="wagtail-image-url-upload",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "Django>=4.2",
        "Wagtail>=5.0",
        "requests",  # if your utils use requests to fetch images
    ],
    entry_points={},
    url="https://github.com/awais786/wagtail-image-from-url",
    license="MIT",
    author="Your Name",
    description="Add images to Wagtail via URL",
    classifiers=[
        "Framework :: Django",
        "Framework :: Wagtail",
    ],
)
