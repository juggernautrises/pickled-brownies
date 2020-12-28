from pathlib import Path


class Image(object):

    def __init__(self, filepath):
        self.filepath = filepath
        self.filename = os.path.basename(self.filepath)
        self.delete = False


if __name__ == '__main__':
    EXTENSIONS = ['.jpg', 'jpeg', '.png']
    image_dir_source = Path("/home/ash/codeshit/pic_browser/test_images")
    files = []
    for extension in EXTENSIONS:
        files.extend(image_dir_source.glob("**/*"+extension))

    for i in files:
        print(i)
        # print(i)