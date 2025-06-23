#!/usr/bin/env python3
"""
YouTube Info Extractor - Secure Version (User Provides API Key at Runtime)
"""
import os
import json
import argparse
import getpass
from datetime import datetime
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def get_api_key():
    """Safely get API key from user input"""
    print("\nYouTube Data API v3 Key Required")
    print("-------------------------------")
    print("1. Get your API key from: https://console.cloud.google.com/")
    print("2. Enable 'YouTube Data API v3'")
    print("3. Enter your key below\n")
    
    api_key = getpass.getpass("Enter your YouTube API key: ").strip()
    if not api_key or api_key.lower() == "AIzaSyCVwe4UnuNjKAoPJA2_b8H3DiFYf_pzTDU":
        raise ValueError("Invalid API key provided")
    return api_key

class YouTubeExtractor:
    def __init__(self, api_key):
        self.youtube = build('youtube', 'v3', developerKey=api_key)
    
    def get_video_info(self, video_id):
        """Get detailed video information"""
        try:
            request = self.youtube.videos().list(
                part="snippet,contentDetails,statistics",
                id=video_id
            )
            response = request.execute()
            if not response.get('items'):
                return {"error": "Video not found or API quota exceeded"}
                
            video = response['items'][0]
            return {
                "video_id": video_id,
                "title": video['snippet']['title'],
                "channel": video['snippet']['channelTitle'],
                "published_at": video['snippet']['publishedAt'],
                "duration": video['contentDetails']['duration'],
                "views": video['statistics'].get('viewCount', 'N/A'),
                "likes": video['statistics'].get('likeCount', 'N/A'),
                "comments": video['statistics'].get('commentCount', 'N/A'),
                "thumbnail": video['snippet']['thumbnails']['high']['url']
            }
        except HttpError as e:
            return {"error": f"API Error: {str(e)}"}

    def get_channel_info(self, channel_id):
        """Get basic information about a channel"""
        try:
            request = self.youtube.channels().list(
                part="snippet,statistics",
                id=channel_id
            )
            response = request.execute()
            if not response.get('items'):
                return {"error": "Channel not found or API quota exceeded"}

            channel = response['items'][0]
            return {
                "channel_id": channel_id,
                "title": channel['snippet']['title'],
                "description": channel['snippet']['description'],
                "published_at": channel['snippet']['publishedAt'],
                "subscribers": channel['statistics'].get('subscriberCount', 'N/A'),
                "total_views": channel['statistics'].get('viewCount', 'N/A'),
                "total_videos": channel['statistics'].get('videoCount', 'N/A'),
                "thumbnail": channel['snippet']['thumbnails']['high']['url']
            }
        except HttpError as e:
            return {"error": f"API Error: {str(e)}"}

def main():
    parser = argparse.ArgumentParser(
        description="YouTube Information Extractor (Secure Version)",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument('--video', help='YouTube Video ID (e.g. dQw4w9WgXcQ)')
    parser.add_argument('--channel', help='YouTube Channel ID')
    parser.add_argument('--output', help='Output file (JSON format)')
    args = parser.parse_args()

    try:
        # Step 1: Get API key securely from user
        api_key = get_api_key()
        
        # Step 2: Initialize extractor
        extractor = YouTubeExtractor(api_key)
        
        # Step 3: Process requested operation
        if args.video:
            print(f"\nFetching info for video: {args.video}")
            result = extractor.get_video_info(args.video)
        elif args.channel:
            print(f"\nFetching info for channel: {args.channel}")
            result = extractor.get_channel_info(args.channel)
        else:
            print("Error: Please specify --video or --channel")
            return
        
        # Step 4: Display or save results
        if args.output:
            with open(args.output, 'w') as f:
                json.dump(result, f, indent=2)
            print(f"\nResults saved to: {args.output}")
        else:
            print("\nResults:")
            print(json.dumps(result, indent=2))
            
    except Exception as e:
        print(f"\nError: {str(e)}")
        print("Please check your API key and try again.")

if __name__ == "__main__":
    main()
