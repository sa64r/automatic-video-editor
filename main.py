from moviepy.editor import VideoFileClip, concatenate_videoclips
import os


def formatVideoInputs(fileName):
    return VideoFileClip('videos/' + fileName)


videoFileNames = os.listdir("./videos")
videos = []

for fileName in videoFileNames:
    videos.append(VideoFileClip('videos/' + fileName))

final_clip = concatenate_videoclips(videos)

final_clip.write_videofile("final_clip.mp4")
