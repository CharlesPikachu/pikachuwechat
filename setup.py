'''
Function:
    setup the pikachuwechat
Author:
    Charles
微信公众号:
    Charles的皮卡丘
GitHub:
    https://github.com/CharlesPikachu
'''
import pikachuwechat
from setuptools import setup, find_packages


'''readme'''
with open('README.md', 'r', encoding='utf-8') as f:
    long_description = f.read()


'''setup'''
setup(
    name=pikachuwechat.__title__,
    version=pikachuwechat.__version__,
    description=pikachuwechat.__description__,
    long_description=long_description,
    long_description_content_type='text/markdown',
    classifiers=[
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Intended Audience :: Developers',
        'Operating System :: OS Independent'
    ],
    author=pikachuwechat.__author__,
    url=pikachuwechat.__url__,
    author_email=pikachuwechat.__email__,
    license=pikachuwechat.__license__,
    include_package_data=True,
    install_requires=[lab.strip('\n') for lab in list(open('requirements.txt', 'r').readlines())],
    zip_safe=True,
    packages=find_packages()
)