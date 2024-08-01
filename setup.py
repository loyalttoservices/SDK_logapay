from setuptools import setup, find_packages

setup(
    name="logapay",
    version="1.0.0",
    description="LogapayAPI SDK is designed for interacting with the LogApay.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="bogosla",
    author_email="loyalttoservices@gmail.com",
    url="https://github.com/loyalttoservices/SDK_logapay",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here, e.g.,
        # 'requests>=2.25.1',
    ],
    tests_require=[
        "pytest",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        # Add more classifiers as needed
    ],
    python_requires=">=3.6",
    include_package_data=True,
    zip_safe=False,
)
