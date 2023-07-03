#through this setup.py file we can create our whole machine learning application as a package
#can deploy it on pypi
# and can install it anywhere
HYPEN_E_DOT='-e .'
from setuptools import find_packages,setup#find all used packages 
from typing import List
def get_requirements(file_path:str)->List[str]:
    #this func will return the list of requirements
    requirements=[]
    with open(file_path) as file_obj:
        requirements=file_obj.readlines()
        requirements=[req.replace("/n","") for req in requirements]
        
        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)
    return requirements

setup(
    name='Ml_projectApr23',
    version='0.0.1',
    author='Saksham Gupta',
    author_email='guptasaksham2311@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')#install all packages
    
    
)