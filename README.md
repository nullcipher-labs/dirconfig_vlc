![dirconfig_vlc_icon_small](https://github.com/nullcipher-labs/dirconfig_vlc/assets/35743548/f8bd12c3-09d2-4d98-bb7d-533ca60261b2)

 **Dirconfig VLC** is a tool to autoselect audio and subtitles in vlc based on folder name.

 Watching mkv files in vlc media player can be extremely annoying if there are multiple audio tracks and subtitle options built into the file.
 One has to manually set the audio (say, if you are watching a japanese anime but for some reason the english dub track appears earlier on the track list) and subtitles every time you run another episode of the same show using vlc.
 You can set default tracks, but those are based on numbers (location in the track list) and are not constant between different files, sources, etc.
 I've looked for a plugin to fix this and couldn't find one, so I wrote this script.

Here's a link to an exe file for easy use:
https://drive.google.com/file/d/1fgNwKd7rWTXiGfiEna9OBHVzbm3OaZw7/view?usp=sharing
<br/>You'll need to configure to be the one opening your mkv files instead of vlc (it runs vlc itself, it just sets the tracks automatically before doing so).

 # Features

1. Set the subtitle track of your choice per folder, by changing the folder name.
   If you rename the folder and add (doesn't matter where) the phrase: SPECSUB_XXX_
   where XXX is replaced by the name of the subtitle track you want, every mkv file in this folder (directly, no subfolders) will open with that subtitle track set automatically.

   For example, if your folder is named "Chernobyl-SPECSUB_italian_" and the mkv files within have subtitle tracks named "italian" (case-insensetive), they will always open with the italian subtitle track already chosen.

2. Set the audio track of your choice per folder, by changing the folder name.
   If you rename the folder and add (doesn't matter where) the phrase: SPECAUD_XXX_
   where XXX is replaced by the name of the audio track you want, every mkv file in this folder (directly, no subfolders) will open with that audio track set automatically.

   For example, if your folder is named "westworld-SPECAUD_french_" and the mkv files within have audio tracks named "french" (case-insensetive), they will always open with the french audio track already chosen.

3. for you anime watchers out there, you can add the phrase ANIME to the folder name (doesn't matter where), and it will:
   - choose japanese audio, doesn't matter where it is placed on the audio track list
   - choose english subtitles.
     Sometimes in anime there are multiple english sub tracks, say one for dialogue, one for signs and such, and one for the opening and closing themes.
     With this option, the program will automatically look for a english sub track with the word "full" in it (which means all of the above).
     If it can't find one, it will search for one that says "dialogue", and if it can't find one like that either, it will default to choose the first english sub track in the tracklist.

   This option is designed to save you time on figuring out what are the names of the tracks you want, if you're watching anime. You can still use SPECSUB too if you want a specific subtrack by sub group, for example crunchyroll.


* You can use all the phrases simultaneously. SPECSUB and SPECAUD override ANIME.
* If at any point a requested audio track isn't found, the video runs with the first audio track in the track list.
* If at any point a requested subtitle track isn't found, the video runs without subtitles.

# Installation

There isn't really any installation required, just two easy setup steps, once you download and extract the exe file.

1. Keep the exe file in some safe folder. If your VLC is installed on the default windows installation path (C:\Program Files\VideoLAN\VLC\vlc.exe), you can skip to the next step.

   If not, create a txt file and put it in the same folder as the exe file. Name it vlc_path.txt, and inside it put the full path to your vlc.exe, whatever it is.

   ![1](https://github.com/nullcipher-labs/dirconfig_vlc/assets/35743548/1b831701-d7c9-43bd-9002-e5e821101ab2)


2. Configure your computer to open all mkv files using the exe by default.

   If you don't know how to do this (in windows), take any mkv video file and right click on it, then choose properties:

   ![2](https://github.com/nullcipher-labs/dirconfig_vlc/assets/35743548/55d01cb5-48f3-4df6-ab5e-57dfcce438ad)


   Then click the change button next to the Open With area (1, red),
   scroll down in the menu that pops up (2, blue), and click "show more" if you need to.
   Once you are done scrolling all the way, click the "Look for another up on this pc" option (3, green):

   ![3](https://github.com/nullcipher-labs/dirconfig_vlc/assets/35743548/e57536c8-309a-4c88-bb11-8c1c8c5f9523)


   Then, navigate to where you kept the exe file, click it (1, red), click open (2, blue) and click ok in the previous window (3, green):

   ![4](https://github.com/nullcipher-labs/dirconfig_vlc/assets/35743548/d2fc0111-0f63-4143-8dc3-b3731c4d28cc)


That's it :)


# Code

The only non-standard library used is python-vlc:
https://pypi.org/project/python-vlc/

Each function is described in the documentation.

There a bunch of consts at the beginning, I wouldn't lower SLEEP_TIME anymore if I were you.
