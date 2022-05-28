from secrets import randbelow
from moviepy.editor import VideoFileClip, concatenate_videoclips
import os
import json
import datetime

# CONSTANTS
VIDEO_CLIP_BUFFER = 50
JOIN_CLIP_BUFFER = 10


startTime = datetime.datetime.now()
# import videos
print('Reading Video File')
filename = 'final_clip'
video = VideoFileClip(filename + '.mp4')


# import transcription JSON
print('Reading Transcription')
transcription = json.load(open('transcriptions/' + filename + '.json'))

# create sections to keep
print('Obtaining Video Clips')
sectionsToKeep = []
for i in transcription['words']:
    sectionsToKeep.append([i['start'], i['end']])

# refine sections to keep


def checkIfClipsOverLap(i):
    if(i+1 < len(sectionsToKeep)):
        if(sectionsToKeep[i][1] > sectionsToKeep[i+1][0] - VIDEO_CLIP_BUFFER):
            sectionsToKeep[i][1] = sectionsToKeep[i+1][1] + VIDEO_CLIP_BUFFER if sectionsToKeep[i +
                                                                                                1][1] + VIDEO_CLIP_BUFFER < video.duration * 1000 else video.duration * 1000
            sectionsToKeep.pop(i+1)
            checkIfClipsOverLap(i)


print('Refining Clips')
for i in range(len(sectionsToKeep)):
    if(i < len(sectionsToKeep)):
        if(sectionsToKeep[i][0] - VIDEO_CLIP_BUFFER < 0):
            sectionsToKeep[i][0] = 0
        else:
            sectionsToKeep[i][0] = sectionsToKeep[i][0] - VIDEO_CLIP_BUFFER

        if(sectionsToKeep[i][1] + VIDEO_CLIP_BUFFER > video.duration * 1000):
            sectionsToKeep[i][1] = video.duration * 1000
        else:
            sectionsToKeep[i][1] = sectionsToKeep[i][1] + VIDEO_CLIP_BUFFER
        checkIfClipsOverLap(i)

for i in range(len(sectionsToKeep)):
    if(i == 0):
        sectionsToKeep[i][1] = sectionsToKeep[i][1] - \
            VIDEO_CLIP_BUFFER + JOIN_CLIP_BUFFER
    elif(i == len(sectionsToKeep)-1):
        sectionsToKeep[i][0] = sectionsToKeep[i][0] + \
            VIDEO_CLIP_BUFFER - JOIN_CLIP_BUFFER
    else:
        sectionsToKeep[i][0] = sectionsToKeep[i][0] + \
            VIDEO_CLIP_BUFFER - JOIN_CLIP_BUFFER
        sectionsToKeep[i][1] = sectionsToKeep[i][1] - \
            VIDEO_CLIP_BUFFER + JOIN_CLIP_BUFFER

# cut out sections from video
sectionsToKeep[0][0] = sectionsToKeep[0][0] - VIDEO_CLIP_BUFFER
sectionsToKeep[len(sectionsToKeep) -
               1][0] = sectionsToKeep[len(sectionsToKeep)-1][0] + VIDEO_CLIP_BUFFER
print(sectionsToKeep)
subClips = []

print('Cutting Clips')
for i in sectionsToKeep:
    subClips.append(video.subclip(
        (i[0])/1000, (i[1])/1000))

# join sections together
final_clip = concatenate_videoclips(subClips)

# save video
final_clip.write_videofile("final_clip-" + str(VIDEO_CLIP_BUFFER) + ".mp4")

print('Time Taken to Complete: ' + str(datetime.datetime.now() - startTime))
