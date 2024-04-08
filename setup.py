from setuptools import find_packages, setup

setup(
    name = "MedKGC",
    version = "0.1.0",
    author = "Mou YongLi, Hanbin Chen, Stefan Decker",
    author_email = "mou@dbis.rwth-aachen.de",
    description = ("Biomedical and Medical Knowledge Graph Construction"),
    license = "MIT",
    url = "https://github.com/MouYongli/MedKGC.git",
    package_dir={"": "src"},
    packages=find_packages("src"),
    classifiers=[
        "Development Status :: 1 - Alpha",
        "Topic :: Named Entity Recognition, Named Entity Normalization, Relation Extraction",
        "License :: OSI Approved :: MIT License",
    ],
)