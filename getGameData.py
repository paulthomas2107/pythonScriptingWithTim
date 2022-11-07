import os
import json
import shutil
from subprocess import PIPE, run
import sys


GAME_DIR_PATTERN = "game"


def findAllGameDirsPaths(source):
    game_paths = []

    for root, dirs, files in os.walk(source):
        for directory in dirs:
            if GAME_DIR_PATTERN in directory.lower():
                path = os.path.join(source, directory)
                game_paths.append(path)
        break
    return game_paths


def getNameFromPaths(paths, to_strip):
    new_names = []
    for path in paths:
        _, dir_name = os.path.split(path)
        new_dir_name = dir_name.replace(to_strip, "")
        new_names.append(new_dir_name)

    return new_names


def createDir(path):
    if not os.path.exists(path):
        os.mkdir(path)


def copyAndOverwrite(source, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    shutil.copytree(source, dest)


def makeJSONMetaDataFile(path, game_dirs):
    data = {
        'gameNames': game_dirs,
        "numberOfGames": len(game_dirs)
    }
    with open(path, 'w') as f:
        json.dump(data, f)


def main(source, target):
    cwd = os.getcwd()
    source_path = os.path.join(cwd, source)
    target_path = os.path.join(cwd, target)

    game_paths = findAllGameDirsPaths(source_path)
    new_game_dirs = getNameFromPaths(game_paths, "_game")

    createDir(target_path)

    for src, dest in zip(game_paths, new_game_dirs):
        dest_path = os.path.join(target_path, dest)
        copyAndOverwrite(src, dest_path)


if __name__ == "__main__":
    args = sys.argv
    if len(args) != 3:
        raise Exception("You must pass a source and target directory only")

    source, target = args[1:]
    main(source, target)
