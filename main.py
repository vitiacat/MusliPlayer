import html
import os
import re
import threading
from functools import partial
from urllib.parse import urlparse, unquote
from urllib.request import urlretrieve

from PyQt5 import QtWidgets, uic
import sys
from tinytag import TinyTag
import m3u8
from PyQt5.QtCore import QUrl

from PyQt5.QtMultimedia import QMediaPlayer, QMediaPlaylist, QMediaContent
from PyQt5.QtWidgets import QFileDialog, QDialog, QMessageBox
from m3u8 import protocol
from m3u8.parser import save_segment_custom_value

from playlist_item import PlaylistItem
from main_window import Ui_MainWindow
from add_url import Ui_Dialog as AddUrlDialog
from settings import Settings, SettingsError
from loading import Ui_Dialog as LoadingDialog

from y_logger import YLogger
from yt_downloader import YtDownloader


def convert_secs(secs):
    # convert to hours:minutes:seconds
    hours = secs // 3600
    minutes = (secs % 3600) // 60
    seconds = secs % 60
    return '{:02d}:{:02d}:{:02d}'.format(int(hours), int(minutes), int(seconds))


def parse_iptv_attributes(line, lineno, data, state):
    # Customize parsing #EXTINF
    if line.startswith(protocol.extinf):
        title = ''
        chunks = line.replace(protocol.extinf + ':', '').split(',', 1)
        if len(chunks) == 2:
            duration_and_props, title = chunks
        elif len(chunks) == 1:
            duration_and_props = chunks[0]

        additional_props = {}
        chunks = duration_and_props.strip().split(' ', 1)
        if len(chunks) == 2:
            duration, raw_props = chunks
            matched_props = re.finditer(r'([\w\-]+)="([^"]*)"', raw_props)
            for match in matched_props:
                additional_props[match.group(1)] = match.group(2)
        else:
            duration = duration_and_props

        if 'segment' not in state:
            state['segment'] = {}
        state['segment']['duration'] = float(duration)
        state['segment']['title'] = title

        # Helper function for saving custom values
        save_segment_custom_value(state, 'extinf_props', additional_props)

        # Tell 'main parser' that we expect an URL on next lines
        state['expect_segment'] = True

        # Tell 'main parser' that it can go to next line, we've parsed current fully.
        return True


class Ui(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui, self).__init__()  # Call the inherited classes __init__ method
        self.thread = None
        self.music_duration = 0
        Ui_MainWindow().setupUi(self)
        # uic.loadUi('main.ui', self)
        self.player = QMediaPlayer(self)
        self.playlist = QMediaPlaylist(self)
        self.openFile = self.findChild(QtWidgets.QAction, 'openFile')
        self.openUrl = self.findChild(QtWidgets.QAction, 'openUrl')
        self.openPlaylist = self.findChild(QtWidgets.QAction, 'openPlaylist')
        self.clearPlaylist = self.findChild(QtWidgets.QAction, 'clearPlaylist')
        self.playBtn = self.findChild(QtWidgets.QToolButton, 'playBtn')
        self.previousBtn = self.findChild(QtWidgets.QToolButton, 'previousBtn')
        self.pauseBtn = self.findChild(QtWidgets.QToolButton, 'pauseBtn')
        self.nextBtn = self.findChild(QtWidgets.QToolButton, 'nextBtn')
        self.stopBtn = self.findChild(QtWidgets.QToolButton, 'stopBtn')
        self.playlist_table = self.findChild(QtWidgets.QTableWidget, 'playlist')
        self.length_bar = self.findChild(QtWidgets.QProgressBar, 'lengthBar')
        self.radioMenu = self.findChild(QtWidgets.QMenu, 'radioMenu')
        self.volumeDial = self.findChild(QtWidgets.QDial, 'volumeDial')
        self.trackSlider = self.findChild(QtWidgets.QSlider, 'trackSlider')
        self.openFile.triggered.connect(self.add_file)
        self.openUrl.triggered.connect(self.add_url)
        self.openPlaylist.triggered.connect(self.open_playlist)
        self.clearPlaylist.triggered.connect(self.clear_all)
        self.playBtn.clicked.connect(self.player.play)
        self.pauseBtn.clicked.connect(self.player.pause)
        self.stopBtn.clicked.connect(self.player.stop)
        self.previousBtn.clicked.connect(self.playlist.previous)
        self.nextBtn.clicked.connect(self.playlist.next)

        self.playlist_table.horizontalHeader().setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        self.playlist_table.horizontalHeader().setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        self.playlist_table.customContextMenuRequested.connect(self.show_playlist_menu)

        self.player.setPlaylist(self.playlist)
        self.player.positionChanged.connect(self.duration_changed)
        self.player.stateChanged.connect(self.state_changed)
        self.player.currentMediaChanged.connect(self.media_changed)
        self.player.error.connect(self.error)
        self.playlist_table.cellDoubleClicked.connect(self.change_track)
        self.volumeDial.valueChanged.connect(self.set_volume)
        self.trackSlider.valueChanged.connect(self.set_position)
        # self.trackSlider.sliderPressed.connect(self.position_pressed)
        # self.trackSlider.sliderReleased.connect(self.position_released)

        self.init_radio()
        self.settings = Settings()
        self.settings.load()
        self.volumeDial.setValue(self.settings.volume)
        self._playlist = []

        self.loading_dialog = QDialog()
        LoadingDialog().setupUi(self.loading_dialog)
        self.loading_dialog.status = self.loading_dialog.findChild(QtWidgets.QLabel, 'status')
        self.loading_dialog.progressBar = self.loading_dialog.findChild(QtWidgets.QProgressBar, 'progressBar')
        self.loading_dialog.actionsBox = self.loading_dialog.findChild(QtWidgets.QDialogButtonBox, 'actions')

        self.show()  # Show the GUI

    def init_radio(self):
        # Create a menu for radio stations from radio directory
        radio_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'radio')
        for file in os.listdir(radio_dir):
            if file.endswith('.m3u'):
                radio_name = file.split('.')[0]
                radio_url = os.path.join(radio_dir, file)
                radio_action = QtWidgets.QAction(radio_name, self)
                radio_action.triggered.connect(lambda x, radio_url=radio_url: self.load_playlist(radio_url))
                self.radioMenu.addAction(radio_action)

    def add_file(self):
        file, _ = QFileDialog.getOpenFileName(caption='Выбрать файлы', filter='Музыка (*.mp3 *.wav *.ogg *.flac *.m4a)')
        if file:
            tag = TinyTag.get(file)
            name = os.path.splitext(os.path.basename(file))[0]
            print(tag)
            title = tag.title if tag.title else name
            artist = tag.artist + ' - ' if tag.artist else ''
            self.add_item(artist + title,
                          convert_secs(tag.duration))
            self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self._playlist.append(PlaylistItem(file, artist + title, tag.duration))

    def d(self, result):
        self.loading_dialog.status.setText('Завершение...')
        if 'entries' not in result:
            self.add_youtube_video(result)
        else:
            for entry in result['entries']:
                self.add_youtube_video(entry)
        self.loading_dialog.close()

    def yt_log(self, msg):
        print(msg)
        if 'Downloading playlist' in msg:
            self.loading_dialog.status.setText('Загрузка плейлиста...')
        elif 'Downloading video' in msg:
            groups = re.search(r"(\d{1,}) of (\d{1,})", msg).groups()
            self.loading_dialog.status.setText('Загрузка видео... ({}/{})'.format(groups[0], groups[1]))
            self.loading_dialog.progressBar.setMaximum(int(groups[1]))
            self.loading_dialog.progressBar.setValue(int(groups[0]))

    def add_url(self):
        dialog = QDialog()
        AddUrlDialog().setupUi(dialog)
        if dialog.exec():
            url = dialog.findChild(QtWidgets.QLineEdit, 'url').text()
            if urlparse(url).netloc == 'www.youtube.com':
                logger = YLogger()
                logger.messageSignal.connect(self.yt_log)
                self.thread = YtDownloader(url, {'outtmpl': '%(id)s.%(ext)s', 'logger': logger, 'clean_infojson': True, 'skip_download': True, 'nocheckcertificate': True, 'ignoreerrors': True})
                self.thread.finished.connect(lambda result: self.d(result))
                self.thread.start()
                self.loading_dialog.actionsBox.rejected.connect(self.thread.terminate)
                self.loading_dialog.open()

            else:
                self.add_item(urlparse(url).path.split('/')[-1], convert_secs(0))
                self.playlist.addMedia(QMediaContent(QUrl(url)))
                self._playlist.append(PlaylistItem(url, urlparse(url).path.split('/')[-1], 0, True))

    def add_youtube_video(self, entry):
        self.add_item(entry['title'], convert_secs(entry['duration']))
        self.playlist.addMedia(QMediaContent(QUrl(entry['formats'][0]['url'])))
        self._playlist.append(PlaylistItem(entry['formats'][0]['url'], entry['title'], entry['duration'], True))

    def add_item(self, name, duration):
        self.playlist_table: QtWidgets.QTableWidget
        row_count = self.playlist_table.rowCount()
        self.playlist_table.insertRow(row_count)
        self.playlist_table.setItem(row_count, 0, QtWidgets.QTableWidgetItem(name))
        self.playlist_table.setItem(row_count, 1, QtWidgets.QTableWidgetItem(duration))

    def remove_current(self):
        self.playlist_table.removeRow(self.playlist_table.currentRow())
        self.playlist.removeMedia(self.playlist.currentIndex())

    def change_track(self, row, column):
        self.playlist.setCurrentIndex(row)
        self.player.play()

    def duration_changed(self, duration):
        duration = duration // 1000
        if self.music_duration != 0:
            self.length_bar.setValue(int(duration / self.music_duration * 100))
            self.length_bar.setFormat('%p% {}/{}'.format(convert_secs(duration), convert_secs(self.music_duration)))
            self.trackSlider.blockSignals(True)
            self.trackSlider.setValue(duration)
            self.trackSlider.blockSignals(False)
        else:
            self.length_bar.setFormat('{}'.format(convert_secs(duration)))

    def state_changed(self, state):
        if state == QMediaPlayer.PlayingState:
            self.playBtn.setChecked(True)
            self.pauseBtn.setChecked(False)
            self.stopBtn.setChecked(False)

            self.playBtn.setEnabled(False)
            self.pauseBtn.setEnabled(True)
            self.stopBtn.setEnabled(True)
        elif state == QMediaPlayer.PausedState:
            self.playBtn.setChecked(False)
            self.pauseBtn.setChecked(True)
            self.stopBtn.setChecked(False)

            self.playBtn.setEnabled(True)
            self.pauseBtn.setEnabled(False)
            self.stopBtn.setEnabled(True)
        elif state == QMediaPlayer.StoppedState:
            self.playBtn.setChecked(False)
            self.pauseBtn.setChecked(False)
            self.stopBtn.setChecked(True)

            self.playBtn.setEnabled(True)
            self.pauseBtn.setEnabled(True)
            self.stopBtn.setEnabled(False)

    def media_changed(self, media):
        item = self._playlist[self.playlist.currentIndex()]
        self.music_duration = item.duration
        # if 'googlevideo' in media.canonicalUrl().host():
        #     result = ydl.extract_info(media.canonicalUrl().toString(), download=False)
        #     self.music_duration = convert_secs(result['duration'])
        # elif media.canonicalUrl().isLocalFile():
        #     self.music_duration = eyed3.load(media.canonicalUrl().path()).info.time_secs
        # else:
        #     self.music_duration = 0
        self.playlist_table.selectRow(self.playlist.currentIndex())
        self.trackSlider.blockSignals(True)
        self.trackSlider.setMaximum(int(self.music_duration))
        self.trackSlider.blockSignals(False)

    def error(self, error):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText("Ошибка при проигрывании")
        msg.setInformativeText(self.player.errorString())
        msg.setWindowTitle("Ошибка")
        if error == QMediaPlayer.ResourceError:
            self.remove_current()
        msg.exec()

    def show_playlist_menu(self, pos):
        playlist_menu = QtWidgets.QMenu(self)
        # write var selected if playlist has selected row
        selected = len(self.playlist_table.selectedItems()) > 0
        remove_action = playlist_menu.addAction('Удалить')
        #remove_action = playlist_menu.addAction('Добавить в закладки')
        remove_action.setEnabled(selected)
        a = playlist_menu.exec(self.playlist_table.mapToGlobal(pos))
        if a == remove_action:
            self.remove_current()

    def open_playlist(self):
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Открыть плейлист', '',
                                                             'Файлы плейлистов (*.m3u *.m3u8)')
        if file_name:
            self.load_playlist(file_name)

    def load_playlist(self, file_name):
        playlist = m3u8.load(file_name, custom_tags_parser=parse_iptv_attributes)
        for segment in playlist.segments:
            self.add_item(segment.title, convert_secs(segment.duration if segment.duration > 0 else 0))
            if 'http' in segment.uri:
                self.playlist.addMedia(QMediaContent(QUrl(segment.uri)))
            elif 'file' in segment.uri:
                self.playlist.addMedia(QMediaContent(QUrl.fromLocalFile(unquote(segment.uri[7:]))))
            self._playlist.append(
                PlaylistItem(segment.title, segment.uri, segment.duration if segment.duration > 0 else 0))

    def clear_all(self):
        self.player.stop()
        self.playlist.clear()
        self.playlist_table.clearContents()
        self.playlist_table.setRowCount(0)
        self.music_duration = 0

    def set_volume(self, value):
        self.player.setVolume(value),
        self.volumeDial.setToolTip(str(value) + '%')
        self.settings.volume = value
        self.settings.save()

    def set_position(self, value):
        self.player.setPosition(value * 1000)

    # pressed = False
    #
    # def position_pressed(self):
    #     if self.player.state() == QMediaPlayer.PlayingState:
    #         self.player.pause()
    #         self.pressed = True
    #
    # def position_released(self):
    #     if self.player.state() == QMediaPlayer.PausedState and self.pressed:
    #         self.player.play()
    #         self.pressed = False


app = QtWidgets.QApplication(sys.argv)
window = Ui()
app.exec()
