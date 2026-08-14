"""
Setup configuration for card camera capture project
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="card-camera-capture",
    version="1.0.0",
    author="Card Vision Team",
    description="Automatic credit/debit card detection and image capture",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7+",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Graphics",
        "Topic :: Scientific/Engineering :: Image Recognition",
    ],
    python_requires=">=3.7",
    install_requires=[
        "opencv-python>=4.8.0",
        "numpy",
        "imutils",
        "pillow>=10.0.0",
    ],
    entry_points={
        "console_scripts": [
            "card-capture=src.camera_capture:main",
        ],
    },
)
