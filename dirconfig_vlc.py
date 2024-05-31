import vlc
import time
import subprocess
import sys
import os

ANIME_WORD = 'ANIME'
SPEC_SUB_WORD = 'SPECSUB'
SPEC_SUB_SEP = '_'
SPEC_AUD_WORD = 'SPECAUD'
SPEC_AUD_SEP = '_'
VLC_PATH_FILENAME = 'vlc_path.txt'
DEFAULT_VLC_PATH = r'C:\Program Files\VideoLAN\VLC\vlc.exe'
SLEEP_TIME = 0.5


def get_exe_dir():
    # get the directory where the .exe is running for pyinstaller purposes
    # it is used so that even in exe form, the script could know which folder it is in,
    # in order to read the vlc path txt file if needed
    if getattr(sys, 'frozen', False):
        # if the application is run as a bundle, sys.executable points to the executable file
        return os.path.dirname(sys.executable)
    else:
        # if it's run in a normal Python environment, __file__ points to the script file
        return os.path.dirname(__file__)


def get_vlc_path():
    # returns the path to the vlc executable
    # if a txt file indicating the path exists, it returns its contents
    # otherwise, it returns the default path
    filepath = os.path.join(get_exe_dir(), 'vlc_path.txt')

    if os.path.isfile(filepath):
        with open(filepath, 'r') as f:
            return f.read().strip()
    else:
        return DEFAULT_VLC_PATH


def get_tracks_info(media_path):
    # opens up vlc using python-vlc, and extracts info on all audio and subtitle tracks
    # returns a list of audio tracks and subtitle tracks as string, each string of the format:
    # name-of-track <id>
    player = vlc.MediaPlayer(media_path)
    player.play()
    time.sleep(SLEEP_TIME)
    audio_tracks = [f"{t[1].decode('utf - 8')} <{t[0]}>" for t in player.audio_get_track_description()]
    sub_tracks = [f"{t[1].decode('utf - 8')} <{t[0]}>" for t in player.video_get_spu_description()]
    player.stop()
    return audio_tracks, sub_tracks


def get_id_from_str(track_str):
    # gets the id of a track as an int, out of the string of the format:
    # name-of-track <id>
    return int(track_str[track_str.rfind('<')+1:-1])


def get_jap_audio_id(audio_tracks):
    # returns the track id (an int) of the japanese audio track if it exists, and 1 otherwise

    for at in audio_tracks:
        if 'japanese' in at.lower():
            return get_id_from_str(at)

    # if there isn't a jap audio track, keep to the default first track
    return 1


def get_eng_sub(sub_tracks):
    # returns the sub track id (int) of the english sub track
    # if there are multiple, it tries looking for one that says "full", and if there isn't one,
    # then one that says "dialogue"
    # if there are not english subs, it returns 0 to disable subs altogether

    # get all english audio tracks
    eng_tracks = [st for st in sub_tracks if 'english' in st.lower()]

    if len(eng_tracks) == 1:
        return get_id_from_str(eng_tracks[0])

    # if there are multiple such tracks, return the one that says "full", and if there isn't one
    # return the one that says "dialogue"
    # if there isn't a "dialogue" one either, return the first english track in the list
    if len(eng_tracks) > 1:
        for et in eng_tracks:
            if 'full' in et.lower():
                return get_id_from_str(et)
        for et in eng_tracks:
            if 'dialogue' in et.lower():
                return get_id_from_str(et)
        return get_id_from_str(eng_tracks[0])

    # if there are no english tracks, choose to disable subtitles
    return 0


def get_specific_subs_request(media_path):
    # returns the specific sub name request out of the folder name in which the file is located
    basename = os.path.basename(os.path.dirname(media_path))
    i = basename.find(SPEC_SUB_WORD) + len(SPEC_SUB_WORD) + len(SPEC_SUB_SEP)
    j = basename[i:].find(SPEC_SUB_SEP) + i
    return basename[i:j]


def get_specific_audio_request(media_path):
    # returns the specific audio name request out of the folder name in which the file is located
    basename = os.path.basename(os.path.dirname(media_path))
    i = basename.find(SPEC_AUD_WORD) + len(SPEC_AUD_WORD) + len(SPEC_AUD_SEP)
    j = basename[i:].find(SPEC_AUD_SEP) + i
    return basename[i:j]


def get_specific_subs(media_path, sub_tracks):
    # returns the sub track id of the specific sub requested
    request = get_specific_subs_request(media_path)

    for st in sub_tracks:
        if request.lower() in st.lower():
            return get_id_from_str(st)

    return 0


def get_specific_audio(media_path, audio_tracks):
    # returns the sub track id of the specific sub requested
    request = get_specific_audio_request(media_path)

    for at in audio_tracks:
        if request.lower() in at.lower():
            return get_id_from_str(at)

    return 0


def is_anime(media_path):
    # checks if the name of the folder in which the media file is located has the string that indicates anime
    return ANIME_WORD in os.path.basename(os.path.dirname(media_path))


def is_specific_sub(media_path):
    # checks if the name of the folder in which the media file is located has the string that indicates a sub request
    return SPEC_SUB_WORD in os.path.basename(os.path.dirname(media_path))


def is_specific_audio(media_path):
    # checks if the name of the folder in which the media file is located has the string that indicates a sub request
    return SPEC_AUD_WORD in os.path.basename(os.path.dirname(media_path))


def get_track_ids(media_path):
    # returns the correct track ids to set for both subtitles and audio
    audio_tracks, sub_tracks = get_tracks_info(media_path)

    audio_id = 1
    if is_anime(media_path):
        audio_id = get_jap_audio_id(audio_tracks)
    if is_specific_audio(media_path):
        audio_id = get_specific_audio(media_path, audio_tracks)

    sub_id = get_eng_sub(sub_tracks)
    if is_specific_sub(media_path):
        sub_id = get_specific_subs(media_path, sub_tracks)

    return audio_id, sub_id


def run_vlc(media_path, audio_id=1, sub_id=-1):
    # runs vlc as a new subprocess and sets the subtitles and audio tracks as needed
    vlc_path = get_vlc_path()
    command = [vlc_path, media_path]
    command.extend(['--audio-track-id', str(audio_id)])
    command.extend(['--sub-track-id', str(sub_id)])
    subprocess.Popen(command)


def run_all(media_path):
    # gets the info and runs vlc in one function
    audio_id, sub_id = get_track_ids(media_path)
    run_vlc(media_path, audio_id, sub_id)


if len(sys.argv) > 1:
    # in order to include spaces, the path to the video file must be delivered to python with "" around it
    # so we remove them before moving on
    file_path = sys.argv[1].replace('"', '')

    run_all(file_path)
