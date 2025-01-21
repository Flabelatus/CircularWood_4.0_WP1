import os
import re

from typing import Union, Iterable

import flask_uploads

from werkzeug.datastructures import FileStorage


class FileUploadHandler:
    
    def __init__(self, **kwargs):
        self.extensions = {
            'CAD': tuple(
                'stp step '
                'igs iges '
                'dwg dxf '
                'prt '
                'aim ipt '
                'sldprt sldasm '
                'jt'.split()),
            'CAM': tuple('mod gcode'.split()),
            'MESH': tuple('obj stl'.split()),
            'POINTCLOUD': tuple('pcd ply'.split()),
            'IMAGES': flask_uploads.IMAGES,
            'DOCS': flask_uploads.DOCUMENTS,
            'TEXT': flask_uploads.TEXT,
            'SRC': flask_uploads.SOURCE,
            'DEFAULTS': flask_uploads.DEFAULTS,
            'DATA': flask_uploads.DATA,
            'ARCHIVES': flask_uploads.ARCHIVES,
            'ALL': flask_uploads.ALL
        }

        self._folder = str(kwargs.get('folder'))
        self._filename = str(kwargs.get('filename'))
        self._file_type = 'DEFAULTS'
        self.upload_set = flask_uploads.UploadSet(self._file_type, self.extensions[self.file_type])

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, filename: str):
        self._filename = filename

    @property
    def folder(self) -> str:
        return self._folder
    
    @folder.setter
    def folder(self, folder: str):
        self._folder = folder

    @property
    def file_type(self):
        return self._file_type

    @file_type.setter
    def file_type(self, file_type_name: str):
        assert file_type_name.upper() in self.extensions, 'The file type cannot be set'
        new_defined_type = file_type_name
        self._file_type = new_defined_type
        self.upload_set = flask_uploads.UploadSet(new_defined_type.lower(), self.extensions[new_defined_type])

    def get_basename(self, file: Union[str, FileStorage]) -> str:
        """
        Return file's basename, for example
        get_basename('some/folder/image.jpg') returns 'image.jpg'
        """
        filename = self._retrieve_filename(file)
        return os.path.split(filename)[1]

    def get_extention(self, file: Union[str, FileStorage]) -> str:
        """
        Return file's extension, for example
        get_extension('image.jpg') returns '.jpg'
        """
        filename = self._retrieve_filename(file)
        return os.path.splitext(filename)[1]

    def is_filename_safe(self, file: Union[str, FileStorage]) -> bool:
        """
        Check if a filename is secure according to our definition
        - starts with a-z A-Z 0-9 at least one time
        - only contains a-z A-Z 0-9 and _().-
        - followed by a dot (.) and a allowed_format at the end
        """
        filename = self._retrieve_filename(file)

        allowed_format = "|".join(self.extensions[self.file_type])
        # format into regex, eg: ('jpeg','png') --> 'jpeg|png'
        regex = f"^[a-zA-Z0-9][a-zA-Z0-9_()-\.]*\.({allowed_format})$"
        return re.match(regex, filename) is not None

    def _retrieve_filename(self, file: Union[str, FileStorage]) -> str:
        """
        Make our filename related functions generic, able to deal with FileStorage object as well as filename str.
        """
        if isinstance(file, FileStorage):
            return file.filename
        return file

    def find_file_any_format(self, filename: str, folder: str, file_type: str = 'DEFAULTS') -> Union[str, None]:
        assert file_type in self.extensions, 'File type is not supported'
        self.set_file_type(file_type)

        for extension in self.extensions[file_type]:
            file = f"{filename}.{extension}"
            file_path = self.upload_set.path(filename=file, folder=folder)
            if os.path.isfile(file_path):
                return file_path
        return None

    def get_path(self, filename: str = None, folder: str = None) -> str:
        return self.upload_set.path(filename=filename, folder=folder)

    def save_file(self, file: FileStorage, folder: str = None, name: str = None) -> str:
        return self.upload_set.save(storage=file, folder=folder, name=name)
