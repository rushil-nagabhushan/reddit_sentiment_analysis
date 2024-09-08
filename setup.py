from setuptools import setup, find_packages

# List of dependencies required by your CLI tool
requirements = [
    'pandas',
    'numpy',
    'matplotlib',
    'seaborn',
    'praw',
    'transformers',
    'torch',
    'scipy',
    'click',
    'python-dotenv',
    'xlsxwriter',
    'tqdm'
]

# Setup function to configure the package
setup(
    name='sentiment-analysis-tool',  # Name of the package
    version='0.1.0',  # Version of the package
    packages=find_packages(),  # Automatically find and include all packages in the directory
    install_requires=requirements,  # Specify the list of dependencies
    entry_points={
        'console_scripts': [
            'sentiment-analysis=cli.sentiment_analysis_tool:cli_entrypoint'  # Define the CLI entry point
        ],
    },
    python_requires='>=3.10',  # Specify the required Python version
    author='Rushil Nagabhushan',  # Replace with your name
    author_email='rushilbhushan@gmail.com',  # Replace with your email
    description='A sentiment analysis CLI tool using transformers',  # Brief description of the package
    classifiers=[
        'Development Status :: Beta',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)
