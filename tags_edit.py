# Unfinished!

import os
import eyed3


def edit_tags_mp3(path, files, artist, album):

    for song in files:
        song = path + song

        tag = eyed3.load(song).tag

        newfile = f"{path}{('0'+str(tag.track_num[0]))[-2:]} {tag.title}_{tag.album_artist}.mp3"
        print(newfile)
        os.system(f"mv \"{file}\" \"{newfile}\"")


def edit_tags_m4a(path, files, artist, album):
    pass


def edit_tags(path, files):
    print("\n\n\n", path, files)

    if all([os.path.isfile(path+f) for f in files]):
        ext = files[0][-4:].lower()

        if all([ext in f.lower() for f in files]):
            folder = path.split('/')[-2]
            artist, album = folder.split(" - ")
            album = album + " - " + artist

            if ext == ".mp3":
                edit_tags_mp3(path, files, artist, album)
            elif ext == ".m4a":
                edit_tags_m4a(path, files, artist, album)
            else:
                print(" X Not supported file formats:", path)

        else:
            print(" X Various file formats:", path)
        return

    files2 = []
    for file in files:
        file = path + file

        if os.path.isdir(file):
            files2.append(file + '/')

    for path2 in files2:
        edit_tags(path2, sorted(os.listdir(path2)))


origin_path = "/home/leli/Desktop/EASY/TEMP/"
origin_files = sorted(os.listdir(origin_path))

edit_tags(origin_path, origin_files)
