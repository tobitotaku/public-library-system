class Book:
    def __init__(self, author, country, imageLink, language, link, pages, title, year):
        self.title = title
        self.author = author
        self.country = country
        self.language = language
        self.link = link
        self.imageLink = imageLink
        self.pages = pages
        self.year = year
        self.list_book = []

    def update(self, obj):
        obj.id = len(self.list_book) + 1
        self.list_book.append(obj)

    def checkAvailibility(self):
        count = 0
        for i in self.list_book:
            if i.available:
                count += 1
        return False if count == 0 else True
