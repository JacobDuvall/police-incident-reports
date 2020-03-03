from setuptools import setup, find_packages

setup(
	name='project0',
	version='1.0',
	author='Jacob Duvall',
	authour_email='jdaleduvall@ou.edu',
	packages=find_packages(exclude=('tests', 'docs')),
	setup_requires=['pytest-runner'],
	tests_require=['pytest']	
)
