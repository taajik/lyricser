
import os
import eyed3
from mutagen.mp4 import MP4
import lyricsgenius


songs_path = '/' + input("Enter path of your musics folder: ").strip(" \'\"/").replace("\'\\\'\'", '\'') + '/'
sss = input(" 1.Set lyrics\n 2.Show lyrics\n 3.Search lyrics\n:")
manual_search = sss == '1u'

realpath = os.path.realpath(__file__)
realpath = realpath[:realpath.rindex('/')]

if not (os.path.isdir(songs_path) and songs_path!="//" and songs_path!="/./"):
    songs_path = realpath + "/songs/"
    if not os.path.isdir(songs_path):
        os.mkdir(songs_path)

without_lyrics_path = realpath + "/without_lyrics/"
if not os.path.isdir(without_lyrics_path):
    os.mkdir(without_lyrics_path)

files = sorted(os.listdir(songs_path))
if not files:
    print("\n Songs folder is empty!\n")
    raise SystemExit

def move_to_without_lyrics(file):
    mv = f"mv \"{file}\" \"{without_lyrics_path}\""
    if os.path.isfile(file) and not input(f"  CONFIRM: {mv} "):
        os.system(mv)

added_lyrics = 0
not_added_lyrics = 0
def add(b, file=''):
    global added_lyrics
    global not_added_lyrics
    if b:
        added_lyrics += 1
    else:
        not_added_lyrics += 1
        if file:
            move_to_without_lyrics(file)

client_access_token = "JPmYaQ8e0nffrGMNZB-S2-5qxjAlVEb7YNtrGUG58PyCmy4jG5Z9pK2BN6kPZ6kW"
if manual_search:
    genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True)
    # genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Live)"])
else:
    genius = lyricsgenius.Genius(client_access_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"])


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
        add(False, file)
        return

    try:
        if manual_search:
            print(t, '-', aa)
            lyrics = genius.lyrics(input("  url: "))
        else:
            lyrics = genius.search_song(t, aa, get_full_info=False).lyrics
            # lyrics = genius.search_song(song_id=input("  id: "), get_full_info=False).lyrics
        # lyrics = """"""
        tag.lyrics.set(lyrics.strip())
        tag.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")
        add(True)
        return
    except Exception:
        print(" X Lyrics Error: ", file)
        add(False, file)
        return


def set_lyrics_m4a(file):
    try:
        tags = MP4(file).tags
        t = tags.get("\xa9nam")
        aa = tags.get("aART")
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
                t = tags.get("\xa9nam")[0]
    except Exception:
        print(" X File Error: ", file)
        add(False, file)
        return

    try:
        if manual_search:
            print(t, '-', aa)
            lyrics = genius.lyrics(input("  url: "))
        else:
            lyrics = genius.search_song(t, aa, get_full_info=False).lyrics
            # lyrics = genius.search_song(song_id=input("  id: "), get_full_info=False).lyrics
        # lyrics = """"""
        tags["\xa9lyr"] = lyrics.strip()
        tags.save(file)
        add(True)
        return
    except Exception:
        print(" X Lyrics Error: ", file)
        add(False, file)
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
            if file[-4:].lower() == ".m4a":
                set_lyrics_m4a(file)
            elif file[-4:].lower() == ".mp3":
                set_lyrics_mp3(file)
        elif os.path.isdir(file):
            files2.append(file + '/')

    for path2 in files2:
        set_lyrics(path2, sorted(os.listdir(path2)))


def show_lyrics(path, files, txt):
    lyrics = ''
    folder = path.split('/')[-2]
    lyrics += f"\n┌─{'─'*len(folder)}─┐\n│ {folder} │ {len(files)}\n└─{'─'*len(folder)}─┘\n"
    files2 = []
    for file in files:
        file = path + file
        if os.path.isfile(file):
            lyrics += f"\n\n{'─'*os.get_terminal_size()[0]}\n\n  {file[len(path):-4]}\n\n\n"

            try:
                if file[-4:].lower() == ".m4a":
                    lyrics += MP4(file).tags.get("\xa9lyr")[0] + '\n'
                elif file[-4:].lower() == ".mp3":
                    lyrics += eyed3.load(file).tag.lyrics[0].text + '\n'
            except Exception:
                lyrics += " X No Lyrics: " + file[len(path):] + '\n'

        elif os.path.isdir(file):
            files2.append(file + '/')
    lyrics += f"\n\n{'─'*os.get_terminal_size()[0]}\n"

    if txt:
        if os.path.isfile("/home/leli/Music/Lyrics/"+folder+" (Lyrics).txt"):
            print("\n Lyrics file already exists.")
        else:
            lyricstxt = open("/home/leli/Music/Lyrics/"+folder+" (Lyrics).txt", 'w')
            # lyricstxt = open(path+folder+" (Lyrics).txt", 'w')
            lyricstxt.write(lyrics)
            lyricstxt.close()
            print("\n Lyrics file generated.")
    else:
        print(lyrics)

    for path2 in files2:
        show_lyrics(path2, sorted(os.listdir(path2)), txt)


def search_lyrics(path, files):
    # print('\n', path, '\n')
    files2 = []
    for file in files:
        file = path + file
        if os.path.isfile(file):
            try:
                if file[-4:].lower() == ".m4a":
                    lyrics = MP4(file).tags.get("\xa9lyr")[0].lower()
                elif file[-4:].lower() == ".mp3":
                    lyrics = eyed3.load(file).tag.lyrics[0].text.lower()
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


if sss == '1' or sss == '1u':
    set_lyrics(songs_path, files)
    print(f"\n\n\n successfulls: {added_lyrics} \n unsuccessfulls: {not_added_lyrics}")
elif sss == '2':
    show_lyrics(songs_path, files, False)
elif sss == '2t':
    show_lyrics(songs_path, files, True)
elif sss == '3':
    q = input(" q: ").lower()
    # if len(q) < 4:
    #     q = ''
    search_lyrics(songs_path, files)
elif sss == '4':
    print(songs_path)
    print(files)

print()
