from setuptools import setup, find_packages


setup(
    name='rankingTool',
    version='2.0',
    license='MIT',
    author="Haoqiang Kang",
    author_email='haoqik@cs.washington.edu',
    packages=find_packages('rankingTool'),
    package_dir={'': 'rankingTool'},
    url='https://github.com/lexilxu/Rankings-UI',
    keywords='GUI',
    install_requires=[
          'toml',
          'pandas',
          'numpy'
      ],

)
