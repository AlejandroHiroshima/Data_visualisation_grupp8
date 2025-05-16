
from setuptools import setup, find_packages


setup(
    name= "yh-dashboard",
    version= "0.0.1",
    description="""
    This page is used for creating YH dashboard in taipy""",
    author= "Marcus Alexander Efrem",
    author_email= "team_8@gamil.com",
    install_requires = ["pandas", "taipy", "duckdb", "openpyxl"],
    packages= find_packages(exclude=("test*", "exploration", "assets", "data"))
) 