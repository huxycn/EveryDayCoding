from setuptools import setup, find_packages

setup(
    name='arxiv_tool',
    version='0.0.1',
    author='huxiaoyang',
    author_email='545960442@qq.com',

    install_requires=[
        'fire',
        'loguru',
        'requests',
        'tenacity',
        'feedparser',
        'Unidecode',
        'BeautifulSoup4',

    ],

    entry_points={
      'console_scripts': [
          'arxiv_tool = arxiv_tool.main:main'
      ]
    },

    packages=find_packages()
)
