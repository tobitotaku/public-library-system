from Config.file_checker import file_checker
from FrontEnd.Homepage import Page


class PublicLibrary:
    def __init__(self):
        file_checker()

    def main(self):
        session = Page()
        session.homePage()


sys = PublicLibrary()
sys.main()

