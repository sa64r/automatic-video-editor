from secrets import randbelow
from moviepy.editor import *
import json
import datetime
import string
# CONSTANTS
VIDEO_CLIP_BUFFER = 50  # used to pad around the duration words are said
JOIN_CLIP_BUFFER = 10  # real buffer between sections
VIDEO_OUTPUT_PATH = 'output/'
STOP_WORDS = json.load(open('stop_words.json'))


# HELPER FUNCTIONS
def generateTextClip(word):
    textClip = TextClip(word['text'], font='Arial',
                        fontsize=50, color='white')
    textClip = textClip.set_pos(('center').set_duration(
        (word['end'] - word['start'])/1000))
    return textClip


def isWordStopWord(word):
    return word.lower() in STOP_WORDS

# import videos


def importVideo(filename):
    print('Reading Video File')
    filename = 'final_clip'
    return VideoFileClip(VIDEO_OUTPUT_PATH + filename + '.MP4')


# import transcription JSON
def importTranscription(filename):
    print('Reading Transcription')
    return json.load(open('transcriptions/' + filename + '.json'))


# create sections to keep
def createSectionsToKeep(transcription):
    print('Obtaining Video Clips')
    sectionsToKeep = []
    for i in transcription['words']:
        sectionsToKeep.append([i['start'], i['end']])
    return sectionsToKeep


# creating text clips
def createVideoWithTextGraphics(transcription, video):
    print('Creating Text Clips')
    NEXT_TEXT_CLIP_START_BUFFER = 5
    textClips = []
    nextClipStart = transcription['words'][0]['start'] + \
        NEXT_TEXT_CLIP_START_BUFFER
    for i in transcription['words']:
        # need to have a space to create an empty text image
        word = ' ' if isWordStopWord(i['text']) else i['text']
        textClip = TextClip(word.upper().translate(str.maketrans('', '', string.punctuation)), font='Berlin-Sans-FB-Demi-Bold',
                            fontsize=400, color='white').set_pos(('center', 'bottom')).set_duration(
            (i['end'] - i['start'] + 2 * JOIN_CLIP_BUFFER)/1000).set_start(nextClipStart/1000)
        nextClipStart = i['end'] + NEXT_TEXT_CLIP_START_BUFFER
        if(i['confidence'] >= 0.5):
            textClips.append(textClip)
    return CompositeVideoClip([video, *textClips])


# refine sections to keep
def checkIfClipsOverLap(i, sectionsToKeep, video):
    if(i+1 < len(sectionsToKeep)):
        if(sectionsToKeep[i][1] >= sectionsToKeep[i+1][0] - VIDEO_CLIP_BUFFER):
            sectionsToKeep[i][1] = sectionsToKeep[i+1][1] + VIDEO_CLIP_BUFFER if sectionsToKeep[i +
                                                                                                1][1] + VIDEO_CLIP_BUFFER < video.duration * 1000 else video.duration * 1000
            sectionsToKeep.pop(i+1)
            checkIfClipsOverLap(i, sectionsToKeep, video)


def refineSections(sectionsToKeep, video):
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
            checkIfClipsOverLap(i, sectionsToKeep, video)

    sectionsToKeep[0][1] = sectionsToKeep[0][1] - \
        VIDEO_CLIP_BUFFER + JOIN_CLIP_BUFFER

    sectionsToKeep[len(sectionsToKeep)-1][0] = sectionsToKeep[len(sectionsToKeep)-1][0] + \
        VIDEO_CLIP_BUFFER - JOIN_CLIP_BUFFER

    for i in range(1, len(sectionsToKeep)-1):
        sectionsToKeep[i][0] = sectionsToKeep[i][0] + \
            VIDEO_CLIP_BUFFER - JOIN_CLIP_BUFFER
        sectionsToKeep[i][1] = sectionsToKeep[i][1] - \
            VIDEO_CLIP_BUFFER + JOIN_CLIP_BUFFER
    print(sectionsToKeep)

    return sectionsToKeep

 # cut out sections from video


def createFinalVideo(videoToCut, hasText, sectionsToKeep):
    subClips = []
    print('Cutting Clips')
    for i in sectionsToKeep:
        subClips.append(videoToCut.subclip(
            (i[0])/1000, (i[1])/1000))

    # join sections together
    final_clip = concatenate_videoclips(subClips)

    # save video
    final_clip.write_videofile(
        VIDEO_OUTPUT_PATH + "final_clip-" + str(VIDEO_CLIP_BUFFER) + '- has text = ' + str(hasText) + ".mp4")


# SEQUENCE OF FUNCTIONS
def main(filename):
    print('Video Creation Started')

    video = importVideo(filename)
    transcription = importTranscription(filename)
    sectionsToKeep = createSectionsToKeep(transcription)
    sectionsToKeep = refineSections(sectionsToKeep, video)
    videoWithText = createVideoWithTextGraphics(transcription, video)
    createFinalVideo(video, False, sectionsToKeep)
    #createFinalVideo(videoWithText, True, sectionsToKeep)
