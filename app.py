import sys
import os
from PyQt6.QtGui import QGuiApplication
from PyQt6.QtQml import QQmlApplicationEngine
from PyQt6.QtQuick import QQuickWindow
from PyQt6.QtCore import QObject, pyqtSignal
import threading
import time

from sheets.saintquote import pick_quote


QQuickWindow.setSceneGraphBackend('software')
app = QGuiApplication(sys.argv)
engine = QQmlApplicationEngine()
engine.quit.connect(app.quit)

class Backend(QObject):

    def __init__(self):
        QObject.__init__(self)
    updated = pyqtSignal(str, arguments=['updater'])
    def updater(self, curr_time):
        self.updated.emit(curr_time)
    def bootUp(self):
        t_thread = threading.Thread(target=self._bootUp)
        t_thread.daemon = True
        t_thread.start()
    def _bootUp(self):
        while True:
            curr_time = time.strftime("%H:%M:%S", time.localtime())
            self.updater(curr_time)
            time.sleep(0.1)
    
QQuickWindow.setSceneGraphBackend('software')

quote = pick_quote()


engine.load('./app.qml')

back_end = Backend()
back_end.bootUp()
engine.rootObjects()[0].setProperty('backend', back_end)

sys.exit(app.exec())