import setuptools

with open('requirements.txt') as req_fp:
    
    setuptools.setup(
        name="EquiBot",
        version="0.0.1-dev",
        author="Abhijeet Soni",
        author_email="abhijeet.nkt@gmail.com",
        url="https://github.com/abijeet-nkt/EquiBot",
        packages=setuptools.find_packages(),
        python_requires=">=3.8",
        install_requires=list(req_fp.read().splitlines())
    )