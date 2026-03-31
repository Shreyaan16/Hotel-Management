from setuptools import setup, find_packages

def get_requirements(file_path: str):
    """
    Reads requirements.txt and returns list of dependencies
    """
    requirements = []
    with open(file_path) as f:
        requirements = f.readlines()
        requirements = [req.replace("\n", "") for req in requirements]
        requirements = [req for req in requirements if req != "-e ."]
    return requirements


setup(
    name="hotel-reservation",
    version="0.0.1",
    author="Shreyaan16",
    author_email="16shreyaan09@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements("requirements.txt"),
)