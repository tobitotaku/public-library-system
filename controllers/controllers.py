from models import *
from userManager import *
from catalog import *

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

    def line(self):
        print('\n'+'-'*40)

    def render_menu(self): 
        if self.stop:
            return 0

        inp_option = False
        # _options.key should match _actions.key
        i = 0
        for item in self.actions:
            print("{i}. {1}".format(i = i,*item))
            i += 1
        try:
            inp_option = int(input("Enter a menu option:"))
            callback = self.actions[inp_option][0]
        except:
            print("Invalid menu option. Enter the ID of the menu option")
            self.render_menu()
        
        callback()
        self.render_menu()
        return inp_option

