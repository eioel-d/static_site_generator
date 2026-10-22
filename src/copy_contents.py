import os
import shutil


def copy_contents(source, destination):

    if not os.path.exists(source):
        return f"{source} doesn't exist"
    if os.path.exists(destination):
        shutil.rmtree(
            destination, ignore_errors=False, onerror=None, onexc=None, dir_fd=None
        )
    os.mkdir(destination)
    paths = os.listdir(source)
    for path in paths:
        current_path = os.path.join(source, path)
        if os.path.isfile(current_path):
            print(f"Copying {current_path} -> {destination}/")
            shutil.copy(current_path, destination)
        else:
            copy_contents(current_path, os.path.join(destination, path))
