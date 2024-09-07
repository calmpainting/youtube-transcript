from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        self.create_env_file()
        self.install_requirements()

    def create_env_file(self):
        env_path = os.path.join(os.getcwd(), '.env')
        if not os.path.exists(env_path):
            api_key = input("Please enter your API_KEY: ")
            with open(env_path, 'w') as env_file:
                env_file.write(f"API_KEY={api_key}\n")
            print(".env file created with your API_KEY.")

    def install_requirements(self):
        requirements_path = os.path.join(os.getcwd(), 'requirements.txt')
        if os.path.exists(requirements_path):
            subprocess.check_call(['pip', 'install', '-r', requirements_path])
            print("Requirements installed from requirements.txt.")

setup(
    name='youtube_transcript_fetcher',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'requests',
        'youtube-transcript-api',
        'tqdm',
        'python-dotenv'
    ],
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'fetch_transcripts=main:main',
        ],
    },
)