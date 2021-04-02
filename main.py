import sys
from gui import PicBrowserGui
from image import PBImages
from PyQt5.QtWidgets import QApplication

if __name__ == '__main__':
    app = QApplication(sys.argv)
    directory = '/Users/ash/code/pickled-brownies/test_images'
    i = PBImages(directory)
    i.shuffle()
    ex = PicBrowserGui(images=i)
    sys.exit(app.exec_())
