from setuptools import setup, find_packages

setup(
    name='comfortSIM',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
        # Add other dependencies here
    ],
    python_requires='>=3.6',
    author='Your Name',
    author_email='your@email.com',
    description='A Python library for thermal comfort analysis.',
    url='https://github.com/your_username/thermal_comfort_analysis',
    license='MIT',
)
