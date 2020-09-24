from setuptools import setup, find_packages

requires = [
    'flask',
    'flask-sqlalchemy',
    'psycopg2',
]

setup(
    name='orcServer',
    version='0.0',
    description='A OCR program running on server a built withFlask',
    author='Mir Wartel',
    author_email='hanneswartel@gmail.com',
    keywords='web flask',
    packages=find_packages(),
    include_package_data=True,
    install_requires=requires
)