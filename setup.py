from setuptools import setup, find_packages

setup(
    name='employee-attrition-prediction',
    version='0.1.0',
    description='Employee attrition prediction system with Streamlit deployment.',
    author='Student Project',
    packages=find_packages(),
    install_requires=[
        'streamlit',
        'pandas',
        'numpy',
        'scikit-learn',
        'seaborn',
        'matplotlib',
        'imbalanced-learn',
        'joblib',
        'openpyxl'
    ],
)
