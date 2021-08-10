
import os
import re
import eyed3
from mutagen.mp4 import MP4
import lyricsgenius



added_lyrics = 0
not_added_lyrics = 0

def add(successful):
    global added_lyrics, not_added_lyrics
    if successful:
        added_lyrics += 1
    else:
        not_added_lyrics += 1


def get_lyrics(title, artist):
    if manual_search:       # manual_search is a global variable, so... not cool
        print(title, '-', artist)
        lyrics = genius.lyrics(input("  url: "))
    else:
        lyrics = genius.search_song(title, artist, get_full_info=False).lyrics
        # lyrics = genius.search_song(song_id=input("  id: "), get_full_info=False).lyrics
    # lyrics = """"""

    lyrics = re.sub("\n*\[", "\n\n[", lyrics)
    lyrics = lyrics.replace('’', "'").strip()
    lyrics = re.sub("[0-9]*EmbedShare URLCopyEmbedCopy$", '', lyrics)

    return lyrics


def set_lyrics_mp3(file):
    try:
        tag = eyed3.load(file).tag
        t = tag._getTitle()
        aa = tag._getAlbumArtist()

        if '(' in t or ')' in t:
            print(t, '-', aa)
            t = input("  t: ")
            if not t.strip():
                t = tag._getTitle()

    except Exception:
        print(" X File Error: ", file)
        add(False)
        return

    try:
        lyrics = get_lyrics(t, aa)
        tag.lyrics.set(lyrics)
        tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")
        add(True)
        return

    except Exception:
        print(" X Lyrics Error: ", file)
        add(False)
        return


def set_lyrics_m4a(file):
    try:
        tag = MP4(file).tags
        t = tag.get("\xa9nam")
        aa = tag.get("aART")

        if len(t) == 1 and len(aa) == 1:
            t = t[0]
            aa = aa[0]
        else:
            print(t, '-', aa)
            t = input("  t: ")
            aa = input("  aa: ")
        if '(' in t or ')' in t:
            print(t, '-', aa)
            t = input("  t: ")
            if not t.strip():
                t = tag.get("\xa9nam")[0]

    except Exception:
        print(" X File Error: ", file)
        add(False)
        return

    try:
        lyrics = get_lyrics(t, aa)
        tag["\xa9lyr"] = lyrics
        tag.save(file)
        add(True)
        return

    except Exception:
        print(" X Lyrics Error: ", file)
        add(False)
        return


def set_lyrics(path, files):
    print('\n' + '─'*len(path) + '──┐')
    print(' ' + path + ' │', len(files))
    print('─'*len(path) + '──┘')

    files2 = []
    i = 0
    for file in files:
        file = path + file
        if os.path.isfile(file):
            i += 1
            print('\n', i, end=": ")

            if file[-4:].lower() == ".mp3":
                set_lyrics_mp3(file)
            elif file[-4:].lower() == ".m4a":
                set_lyrics_m4a(file)

        elif os.path.isdir(file):
            files2.append(file + '/')

    for path2 in files2:
        set_lyrics(path2, sorted(os.listdir(path2)))


def load_lyrics(file):
    try:
        if file[-4:].lower() == ".mp3":
            lyrics = eyed3.load(file).tag.lyrics[0].text
        elif file[-4:].lower() == ".m4a":
            lyrics = MP4(file).tags.get("\xa9lyr")[0]
        else:
            lyrics = " X Not supported file format"

    except Exception:
        # lyrics = " X No Lyrics: " + file[len(path):]
        lyrics = " X No Lyrics"
        print(lyrics, file)

    return lyrics


def show_lyrics(path, files, txt=False):
    lyrics = ""
    folder = path.split('/')[-2]
    lyrics += f"\n┌─{'─'*len(folder)}─┐\n│ {folder} │ {len(files)}\n└─{'─'*len(folder)}─┘\n"
    files2 = []

    for file in files:
        file = path + file
        if os.path.isfile(file):
            lyrics += f"\n\n{'─'*120}\n\n  {file[len(path):-4]}\n\n\n"
            lyrics += load_lyrics(file) + '\n'

        elif os.path.isdir(file):
            files2.append(file + '/')
    lyrics += f"\n\n{'─'*120}\n"

    if txt:
        if os.path.isfile("/home/leli/Music/Lyrics/"+folder+" (Lyrics).txt"):       ## WORKS ON MY MACHINE ERROR
            print(" Lyrics file already exists.")
        else:
            with open("/home/leli/Music/Lyrics/"+folder+" (Lyrics).txt", 'w') as lyricstxt:
                # path+folder+" (Lyrics).txt"
                lyricstxt.write(lyrics)
            print(" Lyrics file generated.")
    else:
        print(lyrics)

    for path2 in files2:
        show_lyrics(path2, sorted(os.listdir(path2)), txt)


def edit_lyrics(path, files, editor_path):
    files2 = []
    for file in files:
        print(file, end='')
        file = path + file
        if os.path.isfile(file):
            lyrics = load_lyrics(file)

            with open(editor_path, 'w') as lyricstxt:
                lyricstxt.write(lyrics)
            if input(" >< "):
                break
            with open(editor_path, 'r') as lyricstxt:
                lyrics = lyricstxt.read().strip()

            if file[-4:].lower() == ".mp3":
                tag = eyed3.load(file).tag
                tag.lyrics.set(lyrics)
                tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")

            elif file[-4:].lower() == ".m4a":
                tag = MP4(file).tags
                tag["\xa9lyr"] = lyrics
                tag.save(file)

        elif os.path.isdir(file):
            files2.append(file + '/')

    for path2 in files2:
        edit_lyrics(path2, sorted(os.listdir(path2)), editor_path)


def search_lyrics(path, files):     ## deprecated
    # print('\n', path, '\n')
    files2 = []
    for file in files:
        file = path + file
        if os.path.isfile(file):
            try:
                if file[-4:].lower() == ".mp3":
                    lyrics = eyed3.load(file).tag.lyrics[0].text.lower()
                elif file[-4:].lower() == ".m4a":
                    lyrics = MP4(file).tags.get("\xa9lyr")[0].lower()
                if lyrics.strip() == '':
                    raise Exception
                if q != '' and q in lyrics:
                    print('\n', file[len(path):])
                    # print(lyrics[lyrics.index(q)-50:lyrics.index(q)+50])
            except Exception:
                print('\n', " X No Lyrics: ", file[len(path):], '\n')
        elif os.path.isdir(file):
            files2.append(file + '/')
    for path2 in files2:
        search_lyrics(path2, sorted(os.listdir(path2)))



if __name__ == "__main__":

    songs_path = '/' + input("Enter path of your musics folder: ").strip(" \'\"/").replace("\'\\\'\'", '\'') + '/'
    realpath = os.path.realpath(__file__)  ##TODO: its not so efficient, mabye os.getcwd() was good enough
    realpath = realpath[:realpath.rindex('/')]

    if not (os.path.isdir(songs_path) and songs_path!="//" and songs_path!="/./"):
        songs_path = realpath + "/songs/"
        if not os.path.isdir(songs_path):
            os.mkdir(songs_path)

    files = sorted(os.listdir(songs_path))
    if not files:
        print("\n Songs folder is empty!\n")
        raise SystemExit


    sss = input(" 1.Set Lyrics\n 2.Show Lyrics\n 3.Search Lyrics\n 4.Edit Lyrics\n:")
    print('\n')

    if sss == '1' or sss == '1m':
        manual_search = sss == '1m'
        client_access_token = "JPmYaQ8e0nffrGMNZB-S2-5qxjAlVEb7YNtrGUG58PyCmy4jG5Z9pK2BN6kPZ6kW"

        if manual_search:
            genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True)
            # genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Live)"])
        else:
            genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])

        set_lyrics(songs_path, files)
        print(f"\n\n\n successfulls: {added_lyrics} \n unsuccessfulls: {not_added_lyrics}")

    elif sss == '2':
        show_lyrics(songs_path, files)

    elif sss == '2t':
        show_lyrics(songs_path, files, True)

    elif sss == '3':
        q = input(" q: ").lower()
        # if len(q) < 4:
        #     q = ''
        search_lyrics(songs_path, files)

    elif sss == '4':
        edit_lyrics(songs_path, files, realpath + "/lyrics_editor.txt")

    elif sss == '5':
        print(songs_path)
        print(files)

    print()

