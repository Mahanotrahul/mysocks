from setuptools import setup

def _get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
      name = 'mysocks',
      version = '1.0.1',
      description = 'Testing installation of sockets package',
      packages = ['mysocks'],
      license='MIT',
      url='https://github.com/Mahanotrahul/mysocks',
      author = 'Rahul Mahanot',
      install_requires=_get_requirements(),
      author_email = 'thecodeboxed@gmail.com',
      download_url = 'https://github.com/Mahanotrahul/mysocks/archive/1.0.tar.gz',
      long_description = long_description,
      long_description_content_type="text/markdown")
