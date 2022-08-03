import json
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import awsFunctions as aws
import requests
from dotenv import load_dotenv
import time
import createVideo as cv
import datetime

load_dotenv()

ASSEMBLY_AI_API_KEY = os.getenv('ASSEMBLY_AI_API_KEY')
VIDEO_OUTPUT_PATH = 'output'
VIDEO_INPUT_PATH = './videos'

# Get all the video files in the videos folder


def uploadVideos(videoFilenames):
    videos = []

    # Format each video file
    for filename in videoFilenames:
        videos.append(VideoFileClip('videos/' + filename))
    return videos


# Concatenate all the videos
def concatenateVideos(videos):
    return concatenate_videoclips(videos)


# Save the final video
def saveFinalVideo(final_clip, filename):
    final_clip.write_videofile(VIDEO_OUTPUT_PATH + '/' + filename)


def uploadVideoToAssemblyAI(filename):

    # used to upload file from computer
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data

    headers = {'Content-Type': 'application/json',
               'authorization': ASSEMBLY_AI_API_KEY}
    response = requests.post('https://api.assemblyai.com/v2/upload',
                             headers=headers,
                             data=read_file(filename))
    return response.json()['upload_url']


def sendVideoToBeTranscribed(video_url):
    endpoint = "https://api.assemblyai.com/v2/transcript"
    json = {
        "audio_url": video_url
    }
    headers = {
        'Content-Type': 'application/json',
        'authorization': ASSEMBLY_AI_API_KEY
    }
    response = requests.post(endpoint, json=json, headers=headers)
    return response.json()['id']


def getTranscription(transcription_id):
    endpoint = "https://api.assemblyai.com/v2/transcript/" + transcription_id
    headers = {
        'Content-Type': 'application/json',
        'authorization': ASSEMBLY_AI_API_KEY
    }
    response = requests.get(endpoint, headers=headers)
    print('Transcription Status: ' + (response.json())['status'])

    while (response.json())['status'] != 'completed' and (response.json())['status'] != 'error':
        response = requests.get(endpoint, headers=headers)
        print('Transcription Status: ' + (response.json())['status'])
        time.sleep(30)
    if (response.json())['status'] == 'error':
        print('TRANSCRIPTION ERROR: ' + (response.json())['error'])
        return None
    return response.json()


def saveTranscription(transcription, filename, path):
    with open(path + '/' + filename, 'w') as outfile:
        json.dump(transcription, outfile)


def getStartTime():
    return datetime.datetime.now()


def showTimeTaken(startTime):
    print('Time Taken to Complete: ' + str(datetime.datetime.now() - startTime))


def main():
    BUCKET_NAME = 'sagar-youtube-video'
    FINAL_CLIP_NAME = 'final_clip'
    FINAL_CLIP_FILE_NAME = FINAL_CLIP_NAME + '.mp4'

    startTime = getStartTime()

    videos = uploadVideos(os.listdir(VIDEO_INPUT_PATH))
    final_clip = concatenateVideos(videos)
    saveFinalVideo(final_clip, FINAL_CLIP_FILE_NAME)
    # aws.create_s3_bucket(BUCKET_NAME)
    # aws.upload_video_to_s3(BUCKET_NAME, FINAL_CLIP_FILE_NAME,
    #                        './' + VIDEO_OUTPUT_PATH)
    # print(ASSEMBLY_AI_API_KEY)
    # video_url = aws.get_video_url(BUCKET_NAME, FINAL_CLIP_FILE_NAME)
    video_url = uploadVideoToAssemblyAI('./output/'+FINAL_CLIP_FILE_NAME)
    transcription_id = sendVideoToBeTranscribed(video_url)
    transcription = getTranscription(transcription_id)
    saveTranscription(transcription, FINAL_CLIP_NAME +
                      '.json', './transcriptions')
    aws.empty_and_delete_bucket(BUCKET_NAME)
    cv.main(FINAL_CLIP_NAME)

    showTimeTaken(startTime)


main()
