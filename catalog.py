from operator import contains
from models import Book
from datahelpers import DataResolver, TargetFile
import re

class Catalog:
    
    allBooks = list()

    def __init__ (self):
        self.allBooks = DataResolver.Read(self, TargetFile.Book, Book)
        # return


    def addBook(self, ID, Author, Title, ISBN) :
        self.allBooks.append(Book(ID, Author, Title, ISBN))
        return

    def UpdateBook(self, ID, Author, Title, ISBN ) :
        
        return

    def search(self, query) :
        r = re.compile(".*" + query + "*.")
        listToStr = ' '.join([str(element.toRow()) for element in self.allBooks])
        ret = list()
        # print(listToStr)


        for book in  self.allBooks :
            if re.search(query, book.author, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.ID, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.title, re.IGNORECASE) :
                ret.append(book)
                # return book
            elif re.search(query, book.ISBN, re.IGNORECASE) :
                ret.append(book)
                # return book

        return ret

            


        # print(listToStr)
        # res = list(filter(r.match, listToStr))
        # print(res)
        # if contains(self.allBooks, lambda x: x.n ==):
        # print(listToStr.find(query))
        # return -1



    def contains(list, filter):
        for x in list:
            if filter(x):
                return True
        return False
