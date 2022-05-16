import os


def file_checker():
    mydir = ["Backups", "Backups/Users", "Backups/Category", "Backups/Loanitems"]

    for file in mydir:
        check_folder = os.path.isdir(file)

        if not check_folder:
            os.makedirs(file)


def cat_file_checker(name):
    name = name.capitalize()
    mydir = ["Backups/Category/" + name]

    for file in mydir:
        check_folder = os.path.isdir(file)

        if not check_folder:
            os.makedirs(file)
