import os
import jsmin
import json


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


class ModuleSysConfigs(object):
    def __init__(self):
        self.fs_helper = FileSystemHelper()
        self.root_folder = self.fs_helper.get_parent_folder(os.path.abspath(__file__), 2)
        self.data_folder = self.root_folder
        self.temp_folder = self.root_folder
        self.result_folder = self.root_folder
        self.import_configs()

    def import_configs(self):
        with open(os.sep.join([self.root_folder, "configs.json"]), "r") as fin:
            configs = json.loads(jsmin.jsmin(fin.read()))
            self.data_folder = configs["data_folder"]
            self.temp_folder = configs["temp_folder"]
            self.result_folder = configs["result_folder"]

    def switch_to_test_configs(self):
        self.data_folder = self.root_folder
        self.temp_folder = self.root_folder
        self.result_folder = self.root_folder
