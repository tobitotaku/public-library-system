from controllers.controllers import ControllerView
from utils import *
import sys

class MembersCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List all members"),
            (self.render_add, "Add a member"),
            (self.render_edit, "Edit a member"),
            (self.render_delete, "Delete a member"),
            (self.render_import_list, "List Imports(CSV)"),
            (self.render_import, "Import Bulk Members(CSV)"),
            (self.render_main, "Back to main menu"),
            (self.exit, "Exit application"),
        ]

    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')
 
    def render_menu(self):
        self.line()
        self.usermanager.all(True)
        print("Members management options:")
        ControllerView.render_menu(self)

    def render_add(self):
        self.line()
        print("Enter member info in fields:")
        username = input("[0] username? ")
        # input("confirm? yes[y]/no[n]")
        if username:
            for l in username:
                if l.isupper():
                    print(f'Username:{username} should only contain lowercase')
                    self.render_add()
                    return
        user = self.usermanager.findbyname(username)
        if user:
            print(f'Member: {user.username} already exists')
        else:
            user = self.usermanager.add(
                username,
                input("[1] surname? "),
                input("[2] age? "),
                input("[3] password? ")
            )
            print(f"Member: {user.username} was added succesfully")
        
    def render_list(self):
        self.line()
        self.usermanager.all(True)
        print('list of active members')
        print(f'{s("#", 3)} - {s("username")} - {s("surname")} - {s("age", 3)} -')
        if len(self.usermanager.users) == 0:
            print('Empty list.')
        for i,item in enumerate(self.usermanager.users):
            print(f'{s(i, 3)} - {s(item.username)} - {s(item.surname)} - {s(item.age, 3)} -')

    def render_edit(self):
        self.render_list()
        id = None
        user = None
        try:
            id = input("Enter number from column #: ")
        except:
            print("Invalid option entered. Retry.")
            self.render_edit()

        if len(self.usermanager.users) == 0:
            return
        if len(str(id)) > 0:
            id = int(id)
            if id >=0:
                user = self.usermanager.findbyid(id)
        if user:
            confirm, user = self.edit_form(user)
            if confirm:
                self.usermanager.update(id, user)
                print(f"Member: {user.username} was changed succesfully.")
            else:
                print(f"Member: {user.username} was NOT changed.")
        else:
            print('Member not found')

    def render_delete(self):
        self.line()
        self.render_list()
        id = None
        user = None
        try:
            id = int(input("Enter number from column #: "))
        except:
            print("Invalid number entered. Retry.")
            self.render_delete()
        
        if len(self.usermanager.users) == 0:
            return
        if len(str(id)) > 0:
            id = int(id)
            if id >=0:
                user = self.usermanager.findbyid(id)
        if user:
            is_confirm = input("Confirm delete (input:y) or (press:Enter)?")
            if is_confirm == 'y':
                self.usermanager.delete(id)
                print(f"Member: {user.username} was deleted succesfully")
            else:
                print(f"Member: {user.username} was NOT deleted")
        else:
            print('Member not found')

    def render_import_list(self):
        print('Available Members Import Files')
        importfiles = self.usermanager.readImportAvailable()
        print(f'{s("#", 3)} - {s("Files", 40)}')
        if len(importfiles) == 0:
            print('Empty list.')
        for i,item in enumerate(importfiles):
            print(f'{s(i, 3)} - {s(item, 40)}')
        return importfiles

    def render_import(self):
        importlist = self.render_import_list()
        importid = self.select_field_id('Enter a number from column #: ')
        if len(importlist) > importid:
            loadimport = importlist[importid]
            print(f'Importfile [{importid}] {loadimport} selected')
            confirm = input('Confirm loading import (input:y) or cancel (press:Enter)?')
            if confirm == 'y':
                notadded = self.usermanager.bulkInsert(loadimport)
                print(f'Import [{importid}] {loadimport} loaded')
                for item in notadded:
                    print(f'Member: {item.username} Skipped. Already exists or username contains uppercase letters')
        else:
            print('Import not found')