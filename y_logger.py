from PyQt5 import QtCore


class YLogger(QtCore.QObject):
    messageSignal = QtCore.pyqtSignal(str)

    def debug(self, msg):
        self.messageSignal.emit(msg)

    def warning(self, msg):
        self.messageSignal.emit(msg)

    def error(self, msg):
        self.messageSignal.emit(msg)
