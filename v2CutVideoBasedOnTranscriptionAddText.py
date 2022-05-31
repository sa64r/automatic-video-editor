from secrets import randbelow
from moviepy.editor import *
import os
import json
import datetime
import string
# CONSTANTS
VIDEO_CLIP_BUFFER = 50
JOIN_CLIP_BUFFER = 10


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
filename = 'final_clip'
video = VideoFileClip(filename + '.MP4')


# import transcription JSON
print('Reading Transcription')
transcription = json.load(open('transcriptions/' + filename + '.json'))

# create sections to keep
print('Obtaining Video Clips')
sectionsToKeep = []
for i in transcription['words']:
    sectionsToKeep.append([i['start'], i['end']])

# creating text clips
print('Creating Text Clips')
NEXT_TEXT_CLIP_START_BUFFER = 5
textClips = []
nextClipStart = transcription['words'][0]['start'] + \
    NEXT_TEXT_CLIP_START_BUFFER
for i in transcription['words']:
    textClip = TextClip(i['text'].upper().translate(str.maketrans('', '', string.punctuation)), font='Berlin-Sans-FB-Demi-Bold',
                        fontsize=400, color='white')
    textClip = textClip.set_pos('center').set_duration(
        (i['end'] - i['start'] + 2 * JOIN_CLIP_BUFFER)/1000)
    textClip = textClip.set_start(nextClipStart/1000)
    nextClipStart = i['end'] + NEXT_TEXT_CLIP_START_BUFFER
    if(i['confidence'] >= 0.5):
        textClips.append(textClip)


videoWithText = CompositeVideoClip([video, *textClips])

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
print(sectionsToKeep)


def createFinalVideo(videoToCut, hasText):
    subClips = []

    print('Cutting Clips')
    for i in sectionsToKeep:
        subClips.append(videoToCut.subclip(
            (i[0])/1000, (i[1])/1000))

    # join sections together
    final_clip = concatenate_videoclips(subClips)

    # save video
    final_clip.write_videofile(
        "final_clip-" + str(VIDEO_CLIP_BUFFER) + '-has text = ' + str(hasText) + ".mp4")


createFinalVideo(video, False)
createFinalVideo(videoWithText, True)


print('Time Taken to Complete: ' + str(datetime.datetime.now() - startTime))
