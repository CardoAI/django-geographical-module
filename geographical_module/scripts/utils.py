import errno
import os


def remove_file(file_path):
    if file_exists(file_path):
        os.remove(file_path)


def file_exists(file_path, raise_exception=False):
    if os.path.isfile(file_path):
        return True
    elif raise_exception:
        raise FileNotFoundError(
            errno.ENOENT, os.strerror(errno.ENOENT), file_path.split('/')[-1])
    else:
        return False


def create_path_to_directory_or_file(directory, filename=None):
    cur_path = os.path.dirname(__file__)
    return os.path.join(cur_path, directory, filename) if filename else os.path.join(cur_path,
                                                                                     directory)
