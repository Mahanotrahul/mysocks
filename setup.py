from setuptools import setup

def _get_requirements():
    with open('requirements.txt') as f:
        requirements = f.read().splitlines()
    return requirements

setup(
      name = 'mysocks',
      version = '1.0',
      description = 'Testing installation of sockets package',
      packages = ['mysocks'],
      license='MIT',
      url='https://github.com/Mahanotrahul/mysocks',
      author = 'Rahul Mahanot',
      install_requires=_get_requirements(),
      author_email = 'thecodeboxed@gmail.com',
      download_url = 'https://github.com/Mahanotrahul/mysocks/archive/1.0.tar.gz')
