from Person.Person import Person


class Subscriber(Person):
    def __init__(self, gender, nameSet, firstName, surname, address, zipcode, city, email, username, telephone):
        self.address = address
        self.zipcode = zipcode
        self.city = city
        self.emailAddress = email
        self.username = username
        self.telephoneNumber = telephone
        super().__init__(gender, nameSet, firstName, surname, 1)

    def getObject(self):
        return self
