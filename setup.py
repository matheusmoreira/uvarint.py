import setuptools

def README() -> str:
    with open('README.md', 'r') as file:
        return file.read()

setuptools.setup(
    name='uvarint',
    version='0.1.1',
    author='Matheus Afonso Martins Moreira',
    author_email='matheus.a.m.moreira@gmail.com',
    description='Unsigned variable-length integers',
    long_description=README(),
    long_description_content_type='text/markdown',
    url='https://github.com/matheusmoreira/uvarint.py',
    py_modules=['uvarint'],
    python_requires='>=3',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
