import os
from shutil import copy
from PIL import Image
import tempfile


class image_editor:
    def __init__(self, windowsize):
        self.temp_images = tempfile.TemporaryDirectory(delete=True)
        print(self.temp_images.name)
        self.windowsize = windowsize
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.src_path = os.path.join(self.base_path, "images")
        self.dst_path = self.temp_images.name

    def create_copys(self):
        for file in os.listdir(self.src_path):
            copy (os.path.join(self.src_path, file), self.dst_path)
        
    def resize(self):
        for file in os.listdir(self.dst_path):
            img = Image.open(os.path.join(self.dst_path, file))
            wanted_size = int(self.windowsize * 0.075)
            img = img.resize((wanted_size, wanted_size), Image.Resampling.LANCZOS)
            img.save(os.path.join(self.dst_path, file))

    def rmv(self):
        for file in os.listdir(self.dst_path):
            os.remove(os.path.join(self.dst_path, file))
        

    @property
    def path(self):
        return self.temp_images.name

if __name__ == "__main__":
    editor = image_editor(800)
    editor.create_copys()
    editor.resize()