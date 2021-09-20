
import spotipy
import time

from requests.exceptions import ReadTimeout

from pycaw.pycaw import AudioUtilities

from spotipy.oauth2 import SpotifyOAuth

#These scopes seem to handle authentication, and need to be one string with spaces.
scope = 'user-read-currently-playing' + ' user-read-playback-state' + ' user-modify-playback-state'

#Create a connection to spotify. Verify by identifying current user.
spotify_client = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='737d8b22db9c448eac2d89b1c775c619', client_secret='4e402f8f79544617b34e3826f143688e', redirect_uri='http://google.com', scope=scope), requests_timeout=10, retries=10)
print("Connected to spotify client! Current user: " + spotify_client.current_user()['display_name'])

# Grab the current playback's JSON data, and distinguish between regular playbacks and icky ads.
spotify_state = " "
expected_playback_name = ''


def get_current_playback() -> dict:
    """Returns the spotify user's current playback regardless of time out errors. JSON formatted to a dict."""
    successful_retrieval = False
    while successful_retrieval == False:
        try:
            # print("Now attempting playback retrieval!")
            current_playback_json = spotify_client.current_playback()
            successful_retrieval = True
            return current_playback_json
        except ReadTimeout:
            print("Spotify seems to have timed out on us. Hm... We will try again!") #TODO: Maybe someday I'll have a more elegant solution than this - not sure why the readtimeout happens.

while True:
    current_playback_json = get_current_playback()
    #Identify whether an ad is playing, mute/unmute accordingly.
    try:
        current_playback_name = current_playback_json['item']['name']

        #Log playback changes (mostly just for testing and convenience).
        if spotify_state != "regular_playback" or expected_playback_name != current_playback_name:
            print("New playback identified. It is a regular playback. We are currently playing: " + current_playback_name + ". " + "We'll let this play.")
            expected_playback_name = current_playback_name
            spotify_state = "regular_playback"

        #Unmute spotify if we aren't playing an ad.
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() == 'Spotify.exe' and volume.GetMute() == 1:
                time.sleep(0.5) #current_playback() updates slightly before playbacks end. This line makes sure we don't accidentally unmute during the last bit of an ad due to current_playback() prematurely updating before spotify client switches off the ad.
                volume.SetMute(0, None)

    # Trying to get the current playback's name returns a type error when you use it during an ad; ads don't seem to support it. Probably spotify devs trying to make me pay money, hmph!
    # Anyway since they seem to only do that for ads, we can error handling to identify them, nasty as that sounds.
    except TypeError:

        #Log ad identification.
        if spotify_state != "ad":
            print("We couldn't retrieve the current playback name. This probably means an ad! DEATH!")
            spotify_state = "ad"
        sessions = AudioUtilities.GetAllSessions()

        #Mute the process. Can't do it conveniently via spotify client because the spotifyClient.volume(0) is premium only, so change system volume.
        for session in sessions:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() == 'Spotify.exe':
                volume.SetMute(1, None)
    #Repeating every half second (assuming negligible delay for code execution) is a simple, (still lightweight) way to make it detect track change at reasonable precision.
    time.sleep(0.5)



#TODO: the problem seems to be that I'm getting clowned by the spotify rate limit. Will have to look at that.