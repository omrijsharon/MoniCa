from setuptools import setup, find_packages

setup(
    name='MoniCa',
    version='0.1',
    url='https://github.com/omrijsharon/MoniCa',
    author='Omri J. Sharon',
    author_email='omrijsharon+github@gmail.com',
    description='MoniCa is a high-speed, user-friendly library for live Monitor Capturing. It harnesses the power of mss, pypiwin32, and multiprocessing to offer seamless and efficient screen capture capabilities.',
    packages=find_packages(),
    install_requires=[
       'pypiwin32',
        'mss',
        'numpy',
       ],
)