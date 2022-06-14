from setuptools import setup

PACKAGE_NAME = 'fill_field_jira_tool'
VERSION = '0.0.6'

with open('requirements.txt') as f:
    lines = f.readlines()
install_requires = [
    line.strip() for line in lines if line and not line.startswith('--')
]

setup(
    name=PACKAGE_NAME,
    version=VERSION,
    keywords='fill_field_jira_tool',
    description='jira related tools',
    license='',
    url='https://gitlab.momenta.works/quality/HDMap-Algorithm-QA/tools_group/road_test_jira_tool',
    author='xuhongyuan',
    author_email='xuhongyuan@momenta.ai',
    py_modules=["fill_field_jira_tool","get_encoding_info"],
    platforms='any',
    zip_safe=False,
    install_requires=install_requires
)
