![dirconfig_vlc_icon](https://github.com/nullcipher-labs/dirconfig_vlc/assets/35743548/298b1a08-2776-473a-a03b-c8394c104e58)

 Dirconfig Vlc is a tool to autoselect audio and subtitles in vlc based on folder name.

 Watching mkv files in vlc media player can be extremely annoying if there are multiple audio tracks and subtitle options built into the file.
 One has to manually set the audio (say, if you are watching a japanese anime but for some reason the english dub track appears earlier on the track list) and subtitles every time you run another episode of the same show using vlc.
 You can set default tracks, but those are based on numbers (location in the track list) and are not constant between different files, sources, etc.
 I've looked for a plugin to fix this and couldn't find one, so I wrote this script.

This is an exe file you'll need to configure to be the one opening your mkv files instead of vlc (it runs vlc itself, it just sets the tracks automatically before doing so).

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
 

* You can use all the phrases simultaneously. SPECSUB and SPECAUD override ANIME.
* If at any point a requested audio track isn't found, the video runs with the first audio track in the track list.
* If at any point a requested subtitle track isn't found, the video runs without subtitles.
  
