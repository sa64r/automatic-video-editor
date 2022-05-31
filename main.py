from moviepy.editor import VideoFileClip, concatenate_videoclips
import os

ASSEMBLY_AI_API_KEY = os.environ.get('ASSEMBLY_AI_API_KEY')
VIDEO_OUTPUT_PATH = 'output/'
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
def saveFinalVideo(final_clip):
    final_clip.write_videofile(VIDEO_OUTPUT_PATH + "final_clip.mp4")


def main():
    videos = uploadVideos(os.listdir(VIDEO_INPUT_PATH))
    final_clip = concatenateVideos(videos)
    saveFinalVideo(final_clip)


main()
