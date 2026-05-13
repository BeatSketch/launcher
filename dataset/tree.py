import os


def filesystem_walker(dir: str) -> list[str]:
    files = os.listdir(dir)
    file_list = []
    for file in files:
        path = dir + "/" + file
        if os.path.isdir(path):
            file_list += filesystem_walker(path)
        else:
            if file.split(".")[-1] == "bsor":
                file_list.append(path)

    return file_list
