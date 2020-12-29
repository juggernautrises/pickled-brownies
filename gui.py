import sys
from PyQt5.QtWidgets import (
    QMainWindow, QApplication, QHBoxLayout,
    QVBoxLayout, QWidget, QPushButton,
    QSpacerItem, QSizePolicy, QCheckBox, QLabel
)
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import Qt

MAX_IMAGE_HEIGHT = 600


class PicBrowserGui(QMainWindow):

    def __init__(self, images=None):
        super().__init__()
        self.images = images
        self.screen = QApplication.primaryScreen()
        self.screen_size = self.screen.size()
        self.screen_width = self.screen_size.width() - 100
        self.screen_height = self.screen_size.height() - 100
        self._init_ui()

    def _init_ui(self):
        # self.resize(self.screen_width, self.screen_height)
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

        self.button_layout.addItem(QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Minimum))
        self.button_layout.addWidget(self.prev_button)
        self.button_layout.addWidget(self.next_button)

        self.image_layout = QVBoxLayout()
        self.label = QLabel()
        if self.images:
            pixmap = QPixmap(self.images.current.filepath)
            self.label.setPixmap(pixmap)
        # self.label.setStyleSheet("QLabel {background-color: red;}")
        self.label.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.image_layout.addWidget(self.label)

        self.setCentralWidget(self.central_widget)
        self.central_widget.setLayout(self.main_layout)
        self.main_layout.addLayout(self.check_box_layout)
        self.main_layout.addLayout(self.image_layout)

        self.main_layout.addLayout(self.button_layout)
        self.next_button.clicked.connect(self.next_image)
        self.prev_button.clicked.connect(self.previous_image)
        self.showMaximized()

    def next_image(self):
        self._set_image(self.images.next)

    def previous_image(self):
        self._set_image(self.images.previous)

    def _set_image(self, image):
        pixmap = QPixmap(image.filepath).scaled(
            self.images.current.width, MAX_IMAGE_HEIGHT, Qt.KeepAspectRatio)
        self.label.setPixmap(pixmap)
        self.delete_check_box.setChecked(image.delete)

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Left:
            self.previous_image()
        if event.key() == Qt.Key_Right:
            self.next_image()
        if event.key() == Qt.Key_Escape:
            self.showMaximized()
        if event.key() == Qt.Key_F:
            self.showFullScreen()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = PicBrowserGui()
    sys.exit(app.exec_())