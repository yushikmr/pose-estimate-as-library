import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pose-estimate-as-library", 
    version="0.0.1",
    install_requires=[
        "mmcv-full==1.5.3",
        "mmdet==2.25.0",
        "mmpose==0.27.0",
        "torch==1.13.0",
        "torchvision==0.14.0",
        "torchaudio==0.14.0"
    ],

    author="yushikmr",
    author_email="yushi.ds@gmail.com",
    description="the wrapper libraries for pose estimate based on mmpose",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yushikmr/pose-estimate-as-library",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache License 2.0",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)