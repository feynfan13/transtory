import os


class FileSystemHelper(object):
    @staticmethod
    def _log_message(func, message):
        return "%s::%s: %s".format(__class__.__name__, func, message)

    def get_parent_folder(self, folder, up_level=1):
        func_name = "get_parent_folder"
        actual_folder = folder
        if folder[-1] == "\\":
            actual_folder = actual_folder[0:-1]
        if os.path.isdir(actual_folder):
            pass
        elif os.path.isfile(actual_folder):
            actual_folder = os.sep.join(actual_folder.split(os.sep)[0:-1])
        else:
            raise ValueError(self._log_message(func_name, "input is neither folder nor file"))
        actual_folder_parts = actual_folder.split(os.sep)
        len_parts = len(actual_folder_parts)
        if up_level >= len_parts:
            raise ValueError(self._log_message(func_name, "up-level %d is too large "
                                                          "for total folder level %d").format(up_level, len_parts))
        return os.sep.join(actual_folder_parts[0:-up_level])

    def get_file_name(self, fpath):
        assert(os.path.isfile(fpath))
        return fpath.split(os.sep)[-1]
