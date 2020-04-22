from setuptools import setup

setup(
    name='AutenticacionContinua',
    version='1.0',
    packages=['logic_code', 'logic_code.keyboard'],
    url='',
    python_requires='~=3.6',
    install_requires=['notify2','psutil','pynput','PyUserInput', 'requests'],
    license='UMU',
    author='Pedro Miguel Sanchez',
    author_email='pedromiguel.sanchez@um.es',
    description='Continuous authentication client'
)
