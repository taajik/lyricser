
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
    def album(self):
        return self.tags.album

    @album.setter
    def album(self, a):
        self.tags.album = a

    @property
    def track_num(self):
        return self.tags.track_num[0]

    @track_num.setter
    def track_num(self, tn):
        if tn is not None:
            tn = int(tn)
        self.tags.track_num = tn

    @property
    def lyrics(self):
        l = self.tags.lyrics
        if any(l):
            return l[0].text
        else:
            return ""

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
        self.tags["\xa9nam"] = [t]

    @property
    def album_artist(self):
        return self._get_tag("aART")

    @album_artist.setter
    def album_artist(self, aa):
        self.tags["aART"] = [aa]

    @property
    def album(self):
        return self._get_tag("\xa9alb")

    @album.setter
    def album(self, a):
        self.tags["\xa9alb"] = [a]

    @property
    def track_num(self):
        tn = self._get_tag("trkn")
        if tn:
            return tn[0]
        return tn

    @track_num.setter
    def track_num(self, tn):
        if tn is not None:
            self.tags["trkn"] = [(int(tn), 0)]
        else:
            self.tags.pop("trkn", None)

    @property
    def lyrics(self):
        l = self._get_tag("\xa9lyr")
        if l is None:
            return ""
        return l

    @lyrics.setter
    def lyrics(self, l):
        self.tags["\xa9lyr"] = [l]

    def save(self):
        self.tags.save(self.path)


class Song:
    def __new__(cls, path):
        ext = path[-3:].lower()
        if ext == "mp3":
            return MP3Song(path)
        elif ext == "m4a":
            return M4ASong(path)
        else:
            raise Exception(
                " X Not supported file format: " + path.split("/")[-1]
            )
