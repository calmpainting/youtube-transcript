from setuptools import setup, find_packages
from setuptools.command.install import install
import os

class CustomInstallCommand(install):
    def run(self):
        install.run(self)
        self.create_env_file()

    def create_env_file(self):
        env_path = os.path.join(os.getcwd(), '.env')
        if not os.path.exists(env_path):
            with open(env_path, 'w') as env_file:
                env_file.write("API_KEY=\n")
            print(".env file created. Please add your API_KEY.")

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