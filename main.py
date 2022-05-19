from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
from clip import Clip

# Get all the video files in the videos folder
videoFileNames = os.listdir("./videos")
videos = []
clippedVideos = []

# Format each video file
# for fileName in videoFileNames:
#     videos.append(VideoFileClip('videos/' + fileName))

for fileName in videoFileNames:
    clip = Clip('videos/' + fileName, -1, 0.5)
    outputs = clip.jumpcut(
        cuts,
        args.magnitude_threshold_ratio,
        args.duration_threshold,
        args.failure_tolerance_ratio,
        args.space_on_edges,
    )

# Concatenate all the videos
final_clip = concatenate_videoclips(videos)


# Save the final video
final_clip.write_videofile("final_clip.mp4")
