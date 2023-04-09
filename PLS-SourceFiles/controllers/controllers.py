from models import *
from userManager import *
from loanManager import *
from catalog import *
from backup import *
import sys

class ControllerView:
    initialized = False
    breadcrumbs = []
    def __init__(self, *args):
        # self.user = self.render_login()
        self.actions = []
        self.stop = False
        self.initialized = True
        self.usermanager = UserManager()
        self.catalog = Catalog()
        self.backup = Backup()
        self.loanmanager = LoanManager(self.catalog)

    def line(self):
        print('\n'+'-'*40)

    def reload_data(self):
        self.usermanager.all()
        self.catalog.listAllBookItems()
        self.catalog.listAllBooks()
        self.loanmanager = LoanManager(self.catalog)
        self.loanmanager.listAllBookItemsLoaned()
        
    def exit(self):
        sys.exit()

    def render_menu(self): 
        inp_option = False
        # _options.key should match _actions.key
        for i,item in enumerate(self.actions):
            print(f"{i}. {item[1]}")
        try:
            inp_option = int(input("Enter a menu option:"))
            callback = self.actions[inp_option][0]
        except:
            print("Invalid menu option. Enter the ID of the menu option")
            self.render_menu()
        
        callback()
        self.render_menu()
        return inp_option

    def edit_form(self, dataModel, skip = ['id', 'role', 'bookid', 'bookItemId', 'loanItemid', 'userid', 'itemStatus']):
        fields = dataModel.__dict__
        print('[fieldid]  [fieldname: fieldvalue] ')
        hide_value = ['password']
        for i, item in enumerate(fields.items()):
            if item[0] in skip:
                continue
            fvalue = '*'*8 if item[0] in hide_value else item[1]
            confirm_field = input(f"[{i}] [{item[0]}: {fvalue}] | edit field (input:y) or skip (press:Enter)?")
            if confirm_field == 'y':
                fields[item[0]] = input(f'[{i}] {item[0]}: ')
            if item[0] == 'username':
                for l in fields[item[0]]:
                    if l.isupper():
                        print(f'Username:{fields[item[0]]} should only contain lowercase')
                        confirm, user = self.edit_form(dataModel)
                        return confirm, user
        confirm_save = input('Save changes (input:y) or skip (Enter)? ')
        if confirm_save == 'y':
            dataModelClass = dataModel.__class__
            dataModel = dataModelClass(fields)
            return True, dataModel
        
        return False, dataModel

    def select_field_id(self, label = "[0] Selected ID? "):
        try:
            id = int(input(label))
            return id
        except:
            print("Invalid ID entered. Retry.")
            id = self.select_field_id(label)
            return id