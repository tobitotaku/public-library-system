from controllers.controllers import ControllerView
from controllers.userscontroller import *
from controllers.catalogcontroller import *
from controllers.bookitemcontroller import *
from controllers.backupcontroller import *
from controllers.loancontroller import *

class MainCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized

        self.render_login()
        self.usercv = MembersCV(ControllerView)
        self.breadcrumbs.append(self)
        self.catalogcv = CatalogMemberCV(ControllerView)
        self.bookitemcv = BookItemMemberCV(ControllerView)
        self.backupcv = BackupCV(ControllerView)
        if self.user and self.user.role == 'admin':
            self.catalogcv = CatalogAdminCV(CatalogMemberCV) 
            self.bookitemcv = BookItemAdminCV(BookItemMemberCV)
            self.actions = [
                (self.usercv.render_menu, "Manage Members"),
                (self.catalogcv.render_menu, "Manage Catalog"),
                (self.bookitemcv.render_menu, "Manage Library"),
                (self.backupcv.render_menu, "Manage Backup"),
                (exit, "Exit application"),
            ]
        else:
            self.actions = [
                (self.catalogcv.render_menu, "Catalog"),
                (self.bookitemcv.render_menu, "Library"),
                (exit, "Exit application"),
            ]
    def render_menu(self):
        self.line()
        print("Menu options:")
        ControllerView.render_menu(self)

    def render_login(self):
        if not self.user:
            inp_username = str(input('Username:'))
            inp_password = str(input('Password:'))

            user = self.usermanager.findbyname(inp_username)
            if (user and inp_username == user.username and inp_password == user.password):
                self.user = user
                print(f'Welcome,{user.username}!')
            else:
                print('Password or Username is incorrect')
                self.render_login()

# MainCV().render_menu()