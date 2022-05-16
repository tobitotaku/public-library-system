import json
from Library.Book import Book
from Library.Bookitem import Bookitem
from Person.Subscriber import Subscriber
from Library.Loanitem import Loanitem


class LoanAdministration:
    def __init__(self):
        self.borrowedBooks = []

    def update(self, Loanitem):
        Loanitem.id = len(self.borrowedBooks) + 1
        self.borrowedBooks.append(Loanitem)

    def createBackup(self):
        with open('Backups/Loanitems/borrowedbooksBackup.json', 'w') as json_file:
            dict_book = []
            for i in self.borrowedBooks:
                sub_obj = {"id": i.subscriber.id,
                           "gender": i.subscriber.gender,
                           "nameSet": i.subscriber.nameSet,
                           "firstName": i.subscriber.firstName,
                           "surname": i.subscriber.surname,
                           "address": i.subscriber.address,
                           "zipcode": i.subscriber.zipcode,
                           "city": i.subscriber.city,
                           "email": i.subscriber.emailAddress,
                           "username": i.subscriber.username,
                           "telephone": i.subscriber.telephoneNumber,
                           "bookitems": []
                           }
                for j in i.list_bookitems:
                    arr = {"id": j.id,
                           "author": j.book_obj.author,
                           "country": j.book_obj.country,
                           "imageLink": j.book_obj.imageLink,
                           "language": j.book_obj.language,
                           "link": j.book_obj.link,
                           "pages": j.book_obj.pages,
                           "title": j.book_obj.title,
                           "year": j.book_obj.year
                           }
                    sub_obj["bookitems"].append(arr)
                dict_book.append(sub_obj)
            json.dump(dict_book, json_file)

    def restoreBackup(self):
        try:
            with open('Backups/Loanitems/borrowedbooksBackup.json') as json_file:
                json_list = json.load(json_file)
                self.borrowedBooks = []
                for i in json_list:
                    sub_obj = Subscriber(i["gender"], i["nameSet"], i["firstName"], i["surname"], i["address"],
                                         i["zipcode"], i["city"], i["email"], i["username"], i["telephone"])
                    sub_obj.id = i["id"]
                    loanItem = Loanitem(sub_obj)
                    for j in i["bookitems"]:
                        obj = Bookitem(Book(j["author"], j["country"], j["imageLink"], j["language"], j["link"],
                                            j["pages"], j["title"], j["year"]))
                        obj.id = j["id"]
                        loanItem.addBookToList(obj)
                    self.borrowedBooks.append(loanItem)
        except FileNotFoundError:
            print("No backup found. Please make one first.")
