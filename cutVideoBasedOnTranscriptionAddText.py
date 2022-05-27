from secrets import randbelow
from moviepy.editor import VideoFileClip, concatenate_videoclips, TextClip
import os
import json
import datetime
# CONSTANTS
VIDEO_CLIP_BUFFER = 50


# HELPER FUNCTIONS
def generateTextClip(word):
    textClip = TextClip(word['text'], font='Arial',
                        fontsize=50, color='white')
    textClip = textClip.set_pos(('center').set_duration(
        (word['end'] - word['start'])/1000))
    return textClip


# import videos
startTime = datetime.datetime.now()

print('Reading Video File')
filename = 'C1114'
video = VideoFileClip('videos/' + filename + '.MP4')


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
        if(sectionsToKeep[i][1] >= sectionsToKeep[i+1][0] - VIDEO_CLIP_BUFFER):
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

# cut out sections from video
print(sectionsToKeep)
subClips = []

print('Cutting Clips')
for i in sectionsToKeep:
    subClips.append(video.subclip(
        (i[0])/1000, (i[1])/1000))

# join sections together
final_clip = concatenate_videoclips(subClips)

# save video
final_clip.write_videofile(
    "final_clip-" + str(VIDEO_CLIP_BUFFER) + '-with text' ".mp4")

print('Time Taken to Complete: ' + str(datetime.datetime.now() - startTime))