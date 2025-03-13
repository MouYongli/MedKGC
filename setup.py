from setuptools import setup, find_packages

setup(
    name="medkgc",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        # 在这里添加项目依赖
    ],
    author="hbchen",
    description="Medical Knowledge Graph Construction Tools",
    python_requires=">=3.6",
)