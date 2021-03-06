from setuptools import setup
import glob

setup(name='map-submission',
      version='0.0.1',
      packages=['ms'],
      description='Skeleton commandline python project',
      url='https://github.com/danielecook/python-cli-skeleton',
      author='Daniel Cook',
      author_email='danielecook@gmail.com',
      license='MIT',
      entry_points="""
      [console_scripts]
      ms = ms.ms:main
      """,
      install_requires=["docopt", "clint", "slugify"],
      zip_safe=False)
