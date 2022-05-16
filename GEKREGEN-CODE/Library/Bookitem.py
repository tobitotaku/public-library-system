class Bookitem:
    def __init__(self, book_obj, available=True):
        self.id = None
        self.book_obj = book_obj
        self.available = available

    def checkAvailability(self):
        if self.available:
            return True
        return False

    def returnBookitem(self):
        if self.available is False:
            self.available = True
