from yt_dlp import YoutubeDL
#from youtube_dl import YoutubeDL

from PyQt5 import QtCore


class YtDownloader(QtCore.QThread):

    finished = QtCore.pyqtSignal(dict)

    def __init__(self, url, ydl_opts, *args, **kwargs):
        QtCore.QThread.__init__(self, *args, **kwargs)
        self.url = url
        self.ydl_opts = ydl_opts
        self.info = None

    def run(self):
        with YoutubeDL(self.ydl_opts) as ydl:
            self.info = ydl.extract_info(self.url, download=False)
        self.finished.emit(self.info)