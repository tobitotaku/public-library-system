import json
from Config.file_checker import *
from Library.Book import Book
from Library.Bookitem import Bookitem


class Catalog:
    def __init__(self, genre):
        self.list_books = []
        self.id = None
        self.genre = genre
        cat_file_checker(self.genre)

    def getCatListBooks(self):
        return len(self.list_books)

    def searchBook(self, title, author, country, language, pages, year):
        bookList = []
        for i in self.list_books:
            if i.title == title or i.author == author or i.country == country or i.pages == pages or i.year == year or i.language == language:
                bookList.append(i)
        return bookList

    def addBook(self, obj):
        self.list_books.append(obj)

    def addBookFromFile(self, filename):
        try:
            with open(filename, 'r') as file:
                list_json = json.load(file)
                for i in list_json:
                    self.list_books.append(
                        Book(i["author"], i["country"], i["imageLink"], i["language"], i["link"],
                             i["pages"], i["title"], i["year"]))

        except FileNotFoundError:
            return "File not found!"

    def createBackup(self):
        with open(f'Backups/Category/{self.genre.capitalize()}/list_booksBackup.json', 'w') as json_file:
            dict_book = []
            for i in self.list_books:
                list_b = []
                for j in i.list_book:
                    arr = {"id": j.id,
                           "available": j.available}
                    list_b.append(arr)
                arr = {
                       "author": i.author,
                       "country": i.country,
                       "imageLink": i.imageLink,
                       "language": i.language,
                       "link": i.link,
                       "pages": i.pages,
                       "title": i.title,
                       "year": i.year,
                       "list_book": list_b,
                       }
                dict_book.append(arr)
            json.dump(dict_book, json_file)

    def restoreBackup(self):
        try:
            with open(f'Backups/Category/{self.genre.capitalize()}/list_booksBackup.json') as json_file:
                json_list = json.load(json_file)
                self.list_books = []
                for i in json_list:
                    obj = Book(i["author"], i["country"], i["imageLink"], i["language"],
                               i["link"], i["pages"], i["title"], i["year"])
                    for j in i["list_book"]:
                        obj.list_book.append(Bookitem(obj, j["available"]))

                    self.list_books.append(obj)

                #self.list_books = new_list
        except FileNotFoundError:
            print("No backup found. Please make one first.")
