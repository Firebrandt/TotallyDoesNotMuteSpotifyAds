This repo contains a spotify program I made for myself. I was getting annoyed at having my concentration be shattered constantly by obtrusive ads. The program will detect when spotify is playing an advertisement, and system mute the application until the ad is done with. 

Bundled together into an .exe with PyInstaller - which, unfortunately, seems to use some hacky tricks to get that to work. The program is false positived as an anti-virus as a result.

Made in Python. The project began during my high school days and was topped off a bit at the beginning of first year university.

This project is largely for my own use. If for some reason, you would like to install it and have it work:

Windows may prevent the program from writing a spotify token to .cache, (because of the pyinstaller virus false positive) but it needs to. So you actually have to allow main.exe through controlled folder access through windows defender. It'll usually work without that if the .cache folder does not yet exist, as well. So you could just keep deleting it over and over again, and on a first-ever-run, it should also work reasonably well.

If you are running it, follow the directions given to you in the console when the program launches.


