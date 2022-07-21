
import eyed3
from mutagen.mp4 import MP4


class MP3Song:
    def __init__(self, path) -> None:
        self.ext = "mp3"
        self.path = path
        self.song = eyed3.load(path)
        self.tags = self.song.tag

    @property
    def title(self):
        return self.tags.title

    @title.setter
    def title(self, t):
        self.tags.title = t

    @property
    def album_artist(self):
        return self.tags.album_artist

    @album_artist.setter
    def album_artist(self, aa):
        self.tags.album_artist = aa

    @property
    def lyrics(self):
        l = self.tags.lyrics
        if any(l):
            return l[0].text

    @lyrics.setter
    def lyrics(self, l):
        self.tags.lyrics.set(l)

    def save(self):
        self.tags.save(version=eyed3.id3.ID3_V2_4, encoding="utf8")


class M4ASong:
    def __init__(self, path) -> None:
        self.ext = "m4a"
        self.path = path
        self.song = MP4(path)
        self.tags = self.song.tags

    def _get_tag(self, tag):
        t = self.tags.get(tag)
        if t:
            return t[0]
        else:
            return None

    @property
    def title(self):
        return self._get_tag("\xa9nam")

    @title.setter
    def title(self, t):
        self.tags["\xa9nam"] = t

    @property
    def album_artist(self):
        return self._get_tag("aART")

    @album_artist.setter
    def album_artist(self, aa):
        self.tags["aART"] = aa

    @property
    def lyrics(self):
        return self._get_tag("\xa9lyr")

    @lyrics.setter
    def lyrics(self, new_lyrics):
        self.tags["\xa9lyr"] = new_lyrics

    def save(self):
        self.tags.save(self.path)


class Song:
    def __new__(cls, path):
        if path[-4:].lower() == ".mp3":
            return MP3Song(path)
        elif path[-4:].lower() == ".m4a":
            return M4ASong(path)
        else:
            raise Exception(
                " X Not supported file format: " + path.split("/")[-1]
            )
