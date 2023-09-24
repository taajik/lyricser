
# working_with_songs_lyrics
![Linux Support](https://img.shields.io/badge/Linux-Support-brightgreen.svg)
![Windows Support](https://img.shields.io/badge/Windows-Support-brightgreen.svg)


These scripts are for dealing with lyrics of songs. Automatically adding lyrics to songs, editing lyrics, reading lyrics and more.


## Features
- Using Genius API, you can add lyrics to your songs and albums easily.
- You can add lyrics to musics in nested folders at once.
- You can have lyrics of albums in a text file.
- You can search through all of your lyrics files.
- Also, you can read lyrics of a song in a text file, edit it and then save it back to the song file.
- Support for MP3 and M4A formats.


## Run
It's written in python 3.6, but maybe with some modifications you can run it on python 2.

For fetching the lyrics from Genius.com and adding them to your songs (`./lyricser set -h`),
you need an API token, which you can get from [Genius](https://genius.com/api-clients).
Then you need to set it as an environment variable:
```
export API_TOKEN=YOUR_API_KEY

# or on Windows:
set API_TOKEN=YOUR_API_KEY
```
And then you can run it:
```
./lyricser --help
```
Note that you don't need an API key to work with options other than '_set_'.
