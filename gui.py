import subprocess
import sys
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import (
    QAction, QApplication, QCheckBox, QFileDialog, QHBoxLayout, QLabel,
    QMainWindow, QMenu, QMenuBar, QPushButton, QSpacerItem, QSizePolicy,
    QVBoxLayout, QWidget
)
from image import PBImages


MAX_IMAGE_HEIGHT = 600
SLIDESHOW_INTERVAL = 3000
MIN_SLIDESHOW_INTERVAL = 1000
SLIDESHOW_INCREMENT = 500
PLATFORMS = {'darwin': 'open'}


class PicBrowserGui(QMainWindow):

    def __init__(self, images=None):
        super().__init__()
        self.platform = sys.platform
        self.images = images
        self.screen = QApplication.primaryScreen()
        self.screen_size = self.screen.size()
        self.screen_width = self.screen_size.width() - 100
        self.screen_height = self.screen_size.height() - 100
        self.time_interval = SLIDESHOW_INTERVAL
        self.num_increments = 0
        self._init_ui()

    def _init_ui(self):
        self.menuBar = QMenuBar(self)
        self.menuBar.setNativeMenuBar(False)
        file_menu = QMenu(' &Stuff', self)
        open_action = QAction("Open Directory        ctrl+r", self)
        shuffle_action = QAction("Shuffle          ctrl+r", self)
        slideshow_action = QAction("Slideshow     ctrl+f", self)
        shuffle_action.triggered.connect(self.shuffle)
        slideshow_action.triggered.connect(self.start_slideshow)
        open_action.triggered.connect(self.load_directory)
        file_menu.addAction(open_action)
        file_menu.addAction(shuffle_action)
        file_menu.addAction(slideshow_action)
        self.menuBar.addMenu(file_menu)
        self.setMenuBar(self.menuBar)

        self.central_widget = QWidget(self)
        self.main_layout = QVBoxLayout()

        self.check_box_layout = QHBoxLayout()
        self.delete_check_box = QCheckBox()
        self.check_box_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.check_box_layout.addWidget(self.delete_check_box)

        self.button_layout = QHBoxLayout()
        self.next_button = QPushButton()
        self.next_button.setText("Next")
        self.prev_button = QPushButton()
        self.prev_button.setText("Previous")

        self.image_layout = QVBoxLayout()
        self.path_label = QLabel()
        self.counter_label = QLabel()
        self.label = QLabel()
        # TODO: replace with proper stylesheet
        self.setStyleSheet("QMainWindow {background-color: black;}")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.path_label.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.path_label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.path_label.hide()
        if self.images:
            self._set_image(self.images.current)

        self.button_layout.addWidget(self.counter_label)
        self.button_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.button_layout.addWidget(self.path_label)
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)
        self.image_layout.addWidget(self.label)

        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.addLayout(self.check_box_layout)
        self.main_layout.addLayout(self.image_layout)
        self.main_layout.addLayout(self.button_layout)

        self.timer = QTimer()
        self.timer.timeout.connect(self.slide_show)

        self.next_button.clicked.connect(self.next_image)
        self.prev_button.clicked.connect(self.previous_image)
        self.delete_check_box.clicked.connect(self.toggle_delete)
        self.showMaximized()

    def load_directory(self):
        d = QFileDialog.getExistingDirectory()
        if d:
            images = PBImages(d)
            if images.files:
                self.images = images
                self._set_image(self.images.current)

    def contextMenuEvent(self, event):
        menu = QMenu(self)
        preview_action = menu.addAction("Open in Preview")
        action = menu.exec_(self.mapToGlobal(event.pos()))
        if action == preview_action:
            subprocess.run([PLATFORMS[self.platform], self.images.current.filepath])

    def change_timer_speed(self, increment=0):
        if self.timer.isActive():
            time_interval = self.time_interval + (increment * SLIDESHOW_INCREMENT)
            if time_interval < MIN_SLIDESHOW_INTERVAL:
                self.time_interval = MIN_SLIDESHOW_INTERVAL
                self.timer.stop()
                self.timer.start(self.time_interval)
            elif time_interval != self.time_interval:
                self.time_interval = time_interval
                self.timer.stop()
                self.timer.start(self.time_interval)

    def toggle_timer(self):
        if self.timer.isActive():
            self.timer.stop()
        else:
            self.timer.start(self.time_interval)

    def update_counter_label(self):
        text = f'{self.images.current_count} / {self.images.length}'
        self.counter_label.setText(text)

    def shuffle(self):
        self.images.shuffle()
        self._set_image(self.images.current)

    def start_slideshow(self):
        self.delete_check_box.hide()
        self.prev_button.hide()
        self.next_button.hide()
        self.path_label.hide()
        self.counter_label.hide()
        # self.main_layout.removeItem(self.button_layout)
        self.menuBar.hide()
        self.showFullScreen()
        self.setCursor(Qt.BlankCursor)
        if not self.timer.isActive():
            self.timer.start(SLIDESHOW_INTERVAL)

    def slide_show(self):
        self.next_image()

    def toggle_counter(self):
        if self.counter_label.isHidden():
            self.counter_label.show()
        else:
            self.counter_label.hide()

    def toggle_delete(self):
        self.images.current.delete = not self.images.current.delete
        self.delete_check_box.setChecked(self.images.current.delete)

    def toggle_path(self):
        if self.path_label.isHidden():
            path = self.images.current.filepath
            self.path_label.setText(path)
            self.path_label.show()
        else:
            self.path_label.hide()

    def next_image(self):
        self._set_image(self.images.next)

    def previous_image(self):
        self._set_image(self.images.previous)

    def _show_maximized(self):
        self.unsetCursor()
        self.delete_check_box.show()
        self.prev_button.show()
        self.next_button.show()
        self.menuBar.show()
        self.showMaximized()

    def _set_image(self, image):
        pixmap = QPixmap(image.filepath).scaled(
            self.images.current.width, MAX_IMAGE_HEIGHT, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.delete_check_box.setChecked(image.delete)
        self.path_label.setText(self.images.current.filepath)
        self.update_counter_label()

    def keyPressEvent(self, event):

        if event.key() == Qt.Key_R and event.modifiers() == Qt.ControlModifier:
            self.shuffle()
        elif event.key() == Qt.Key_F and event.modifiers() == Qt.ControlModifier:
            self.start_slideshow()
        elif event.key() == Qt.Key_O and event.modifiers() == Qt.ControlModifier:
            self.load_directory()
        elif event.key() == Qt.Key_Left:
            self.previous_image()
        elif event.key() == Qt.Key_Right:
            self.next_image()
        elif event.key() == Qt.Key_Escape:
            self._show_maximized()
        elif event.key() == Qt.Key_C:
            self.toggle_counter()
        elif event.key() == Qt.Key_D:
            self.toggle_delete()
        elif event.key() == Qt.Key_F:
            self.setCursor(Qt.BlankCursor)
            self.showFullScreen()
        elif event.key() == Qt.Key_P:
            self.toggle_path()
        elif event.key() == Qt.Key_Space:
            self.toggle_timer()
        elif event.key() == Qt.Key_Equal:
            self.change_timer_speed(-1)
        elif event.key() == Qt.Key_Minus:
            self.change_timer_speed(1)

        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PicBrowserGui()
    sys.exit(app.exec_())
