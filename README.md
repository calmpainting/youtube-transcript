# YouTube Transcript downloader
This project fetches transcripts from videos from specified YouTube channels and saves them to a file.

## Setup

### Prerequisites

- Python 3.x
- pip (Python package installer)
- [YouTube Data API v3 key](https://console.cloud.google.com/apis/library/youtube.googleapis.com)

## Installation

### Windows

Please use the executable (.exe).

### Linux

1. Clone the repository:

    ```bash
    git clone https://github.com/calmpainting/youtube_transcript.git
    cd youtube_transcript
    ```

2. Install the dependencies using `pip`:

    ```bash
    pip install -r requirements.txt
    ```

3. Alternatively, you can install the project using the `setup.py` script, which will guide you through creating a `.env` file:

    ```bash
    python setup.py install
    ```

4. Create a `.env` file manually with your YouTube API key, or let the `setup.py` handle it for you:

    ```bash
    echo "API_KEY=your_api_key_here" > .env
    ```

## Usage

1. Run the script by executing:

    ```bash
    python main.py
    ```

2. Enter the name of the YouTube channel you want to fetch transcripts from.

3. Optionally, specify the number of videos to process. If left empty, it will fetch transcripts for all available videos.

4. The script will save the transcripts in a text file named `{channel_name}_transcripts.txt`.
