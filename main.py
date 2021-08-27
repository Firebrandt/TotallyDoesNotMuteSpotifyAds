
import spotipy
import time

from pycaw.pycaw import AudioUtilities

from spotipy.oauth2 import SpotifyOAuth

#These scopes seem to handle authentication, and need to be one string with spaces.
scope = 'user-read-currently-playing' + ' user-read-playback-state' + ' user-modify-playback-state'

#Create a connection to spotify. Verify by identifying current user.
spotifyClient = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id='737d8b22db9c448eac2d89b1c775c619', client_secret='4e402f8f79544617b34e3826f143688e', redirect_uri='http://google.com', scope=scope))
print("Connected to spotify client! Current user: " + spotifyClient.current_user()['display_name'])

# Grab the current playback's JSON data, and distinguish between regular playbacks and icky ads.
while True:
    currentPlaybackJSON = spotifyClient.current_playback()
    try:
        currentPlaybackName = currentPlaybackJSON['item']['name']
        print('It seems we got data about the current playback successfully. It is called: ' + currentPlaybackName + ". We'll let this play.")
        #Unmute spotify if we aren't playing an ad.
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() == 'Spotify.exe' and volume.GetMute() == 1:
                time.sleep(0.5) #current_playback() updates slightly before playbacks end. This line makes sure we don't accidentally unmute during the last bit of an ad due to current_playback() prematurely updating before spotify client switches off the ad.
                volume.SetMute(0, None)
    # current_playback() returns a type error when you use it during an ad; ads don't seem to support it. Probably spotify devs trying to make me pay money, hmph!
    # Anyway since they seem to only do that for ads, we can error handling to identify them, nasty as that sounds.
    except TypeError:
        print("We couldn't retrieve the current playback. This probably means an ad! DEATH!")
        sessions = AudioUtilities.GetAllSessions()

        #Mute the process. Can't do it conveniently via spotify client because the spotifyClient.volume(0) is premium only, so system volume.
        for session in sessions:
            volume = session.SimpleAudioVolume
            if session.Process and session.Process.name() == 'Spotify.exe':
                volume.SetMute(1, None)

    #Repeating every quarter second (assuming negligible delay for code execution) is a simple, (still lightweight) way to make it detect track change at reasonable precision.
    time.sleep(0.25)



