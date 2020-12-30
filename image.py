import random
from PIL import Image, UnidentifiedImageError
from pathlib import Path

EXTENSIONS = ['.jpg', '.JPG', '.jpeg', '.png']


class PBImage(object):

    def __init__(self, pathlib_obj):
        self.pathlib_obj = pathlib_obj
        self.filepath = str(pathlib_obj)
        self.name = pathlib_obj.name
        self.delete = False
        self.width = 0
        self.height = 0
        self._set_dimensions()

    def _set_dimensions(self):
        try:
            img = Image.open(self.filepath)
            self.height = img.height
            self.width = img.width
            img.close()
        except UnidentifiedImageError:
            print(self.filepath)

class PBImages(object):

    def __init__(self, source_dir):
        self.source_dir = Path(source_dir)
        self.files = []
        self.index = 0
        self.max_height = 0
        self.max_width = 0
        for f in self.source_dir.glob("**/*"):
            if f.suffix in EXTENSIONS:
                img = PBImage(f)
                if img.width > self.max_width:
                    self.max_width = img.width
                if img.height > self.max_height:
                    self.max_height = img.height
                self.files.append(img)

    @property
    def current_count(self):
        return self.index + 1

    @property
    def length(self):
        return len(self.files)

    @property
    def current(self):
        return self.files[self.index]

    @property
    def next(self):
        self.index += 1
        if self.index >= len(self.files):
            self.index = 0
        return self.files[self.index]

    @property
    def previous(self):
        self.index -= 1
        if self.index < 0:
            self.index = len(self.files) - 1
        return self.files[self.index]

    def shuffle(self):
        random.shuffle(self.files)
        self.index = 0


if __name__ == '__main__':
    directory = '/Users/ash/code/pickled-brownies/test_images'
    i = PBImages(directory)
    for x in range(15):
        print(i.current, "/", i.length-1)
        i.next

