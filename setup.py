from setuptools import setup, find_packages

setup(
    name='edc',
    version='0.0.1',
    author='huxiaoyang',
    author_email='545960442@qq.com',

    install_requires=['numpy', 'opencv-python', 'loguru', 'tenacity'],

    entry_points={
      'console_scripts': [
          'arxiv = edc.arxiv.main:main'
      ]
    },

    packages=find_packages()
)
