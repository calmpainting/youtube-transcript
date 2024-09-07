import requests
import os
from youtube_transcript_api import YouTubeTranscriptApi
from tqdm import tqdm
from dotenv import load_dotenv

def ensure_env_file():
    env_path = os.path.join(os.getcwd(), '.env')
    if not os.path.exists(env_path):
        print("No .env file found.")
        api_key = input("Please enter your API_KEY: ")
        with open(env_path, 'w') as env_file:
            env_file.write(f"API_KEY={api_key}\n")
        print(".env file created with your API_KEY.")
    load_dotenv()

ensure_env_file()  # Ensure .env file is loaded or created

API_KEY = os.getenv('API_KEY')

def get_channel_id(api_key, channel_name):
    print(f"Looking up channel ID for channel name: {channel_name}")
    base_url = "https://www.googleapis.com/youtube/v3/search?"
    url = f"{base_url}key={api_key}&q={channel_name}&type=channel&part=id"
    response = requests.get(url)
    data = response.json()
    if 'items' in data and len(data['items']) > 0:
        channel_id = data['items'][0]['id']['channelId']
        print(f"Found channel ID: {channel_id}")
        return channel_id
    else:
        raise ValueError("Channel not found")

def get_all_video_ids(api_key, channel_id, limit=None):
    print(f"Fetching video IDs for channel ID: {channel_id}")
    video_ids = []
    base_url = "https://www.googleapis.com/youtube/v3/search?"
    url = f"{base_url}key={api_key}&channelId={channel_id}&part=id&order=date&maxResults=50"
    page_count = 0
    while url and (limit is None or len(video_ids) < limit):
        response = requests.get(url)
        data = response.json()
        for item in data['items']:
            if item['id']['kind'] == 'youtube#video':
                video_ids.append(item['id']['videoId'])
                if limit is not None and len(video_ids) >= limit:
                    break
        if 'nextPageToken' in data and (limit is None or len(video_ids) < limit):
            url = f"{base_url}key={api_key}&channelId={channel_id}&part=id&order=date&maxResults=50&pageToken={data['nextPageToken']}"
            page_count += 1
            print(f"Fetched page {page_count}, total video IDs so far: {len(video_ids)}")
        else:
            url = None
    print(f"Found {len(video_ids)} video IDs")
    return video_ids[:limit] if limit else video_ids

def process_videos(api_key, video_ids, progress_bar):
    video_details = {}
    transcripts = {}
    errors = {}
    base_url = "https://www.googleapis.com/youtube/v3/videos?"
    for video_id in video_ids:
        url = f"{base_url}key={api_key}&id={video_id}&part=snippet"
        response = requests.get(url)
        data = response.json()
        if 'items' in data and len(data['items']) > 0:
            video_details[video_id] = {
                'title': data['items'][0]['snippet']['title'],
                'url': f"https://www.youtube.com/watch?v={video_id}"
            }
        else:
            print(f"Could not retrieve details for video ID: {video_id}")
        try:
            transcript = YouTubeTranscriptApi.get_transcript(video_id)
            transcripts[video_id] = transcript
        except Exception as e:
            errors[video_id] = str(e)
        progress_bar.update(1)
    return video_details, transcripts, errors

def save_transcripts_to_file(video_details, transcripts, errors, channel_name):
    print("Saving transcripts to file")
    filename = f"{channel_name}_transcripts.txt"
    with open(filename, mode='w', encoding='utf-8') as file:
        for video_id, transcript in transcripts.items():
            video_title = video_details[video_id]['title']
            video_url = video_details[video_id]['url']
            file.write(f"Video Title: {video_title} - {video_url}\n")
            for line in transcript:
                timestamp = line['start']
                hours = int(timestamp // 3600)
                minutes = int((timestamp % 3600) // 60)
                seconds = int(timestamp % 60)
                file.write(f"[{hours:02}:{minutes:02}:{seconds:02}] {line['text']}\n")
            file.write("===========================================\n")
        if errors:
            file.write("\nErrors:\n")
            for video_id, error in errors.items():
                video_title = video_details.get(video_id, {}).get('title', 'Unknown Title')
                video_url = video_details.get(video_id, {}).get('url', f"https://www.youtube.com/watch?v={video_id}")
                file.write(f"Video Title: {video_title} - {video_url}\nError: {error}\n")
    print(f"Transcripts saved to {filename}")

if __name__ == '__main__':
    channel_name = input("Enter the YouTube channel name: ")
    limit = input("Enter the number of videos to process (or press Enter to process all): ")
    limit = int(limit) if limit else None
    try:
        channel_id = get_channel_id(API_KEY, channel_name)
        video_ids = get_all_video_ids(API_KEY, channel_id, limit)
        print(f"Total videos found: {len(video_ids)}")
        
        with tqdm(total=len(video_ids), desc="Overall Progress") as progress_bar:
            video_details, transcripts, errors = process_videos(API_KEY, video_ids, progress_bar)
        
        save_transcripts_to_file(video_details, transcripts, errors, channel_name)
    except ValueError as e:
        print(e)