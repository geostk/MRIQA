"""
Jpeg Input
"""
from PIL import Image
from core.component import Component

class JpegInput(Component):
    """
    Class for Jpeg Input
    """
    def __init__(self, options):
        super(JpegInput, self).__init__(options)
        self.__file_path = ""
        self.file_path = self.properties['file_path']

    @property
    def file_path(self):
        """
        getter of file_path
        """
        return self.__file_path

    @file_path.setter
    def file_path(self, value):
        self.__file_path = value

    @staticmethod
    def get_parameters():
        """
        return all parameters of the component
        """
        for key, value in JpegInput.__dict__.items():
            if isinstance(value, property):
                print(key)

    def start(self):
        """
        open a file and sends notifier
        """
        super(JpegInput, self).start()
        self.package['data'] = Image.open(self.file_path)
        self.log_line('open file')
        self.output_notifier.notify_observers(self.package)
