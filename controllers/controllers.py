from models import *
from userManager import *
from loanManager import *
from catalog import *
from backup import *

class ControllerView:
    user = False
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

    def render_menu(self): 
        if self.stop:
            return 0

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

    def edit_form(self, dataModel, skip = ['id', 'role']):
        fields = dataModel.__dict__
        print('[fieldid]  [fieldname: fieldvalue] ')
        hide_value = ['password']
        for i, item in enumerate(fields.items()):
            if item[0] in skip:
                continue
            fvalue = '*'*8 if item[0] in hide_value else item[1]
            confirm_field = input(f"[{i}] [{item[0]}: {fvalue}] | edit field or skip? (y/Enter) ")
            if confirm_field == 'y':
                fields[item[0]] = input(f'[{i}] {item[0]}: ')

        confirm_save = input('Save changes or skip? (y/Enter) ')
        if confirm_save == 'y':
            dataModelClass = dataModel.__class__
            dataModel = dataModelClass(fields)
            return True, dataModel
        
        return False, dataModel
