from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from clip import Clip

ASSEMBLY_AI_API_KEY = os.environ.get('ASSEMBLY_AI_API_KEY')

# Get all the video files in the videos folder
videoFileNames = os.listdir("./videos")
videos = []
clippedVideos = []

# Format each video file
for fileName in videoFileNames:
    videos.append(VideoFileClip('videos/' + fileName))

# Concatenate all the videos
final_clip = concatenate_videoclips(videos)


# Save the final video
final_clip.write_videofile("final_clip.mp4")
