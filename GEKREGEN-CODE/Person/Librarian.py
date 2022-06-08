from Person.Person import Person


class Librarian(Person):
    def __init__(self, gender, firstName, surname, nameSet, username, password):
        super().__init__(gender, nameSet, firstName, surname, 0)
        self.username = username
        self.password = password

    def getObject(self):
        return self
