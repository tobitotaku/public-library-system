from controllers.controllers import ControllerView
# from controllers.maincontroller import MainCV
import os
import sys
class BackupCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List backups"),
            (self.render_add, "Save backup"),
            (self.render_load_backup, "Load backup"),
            (self.render_main, "Back to main menu"),
            (exit, "Exit application"),
        ]
        self.backups = self.backup.readBackupsAvailable()

    def render_main(self):
        if len(self.breadcrumbs)>0:
            self.breadcrumbs[0].render_menu()
        else:
            print('Main menu not found')
 
    def render_menu(self):
        self.line()
        print("Backup management options:")
        ControllerView.render_menu(self)

    def render_add(self):
        self.line()
        confirm = input("Confirm backup of current data? (y/Enter) ")
        if confirm == 'y':
            self.backup.StoreBackup()

    def render_list(self):
        self.line()
        print('Backups Available')
        print('- ID - backup -')
        if len(self.backups) == 0:
            print('Empty list.')
        for i,item in enumerate(self.backups):
            print(f'- {i} - {item} -')

    def render_load_backup(self):
        self.render_list()
        backupid = self.select_field_id('Select backup ID? ')
        if len(self.backups) > backupid:
            loadbackup = self.backups[backupid]
            print(f'Backup [{backupid}] {loadbackup} selected')
            confirm = input('Confirm loading backup? (y/Enter)')
            if confirm == 'y':
                res = self.backup.loadBackup(loadbackup)
                print(res)
                if(res == True):
                    print(f'Backup [{backupid}] {loadbackup} loaded')
                    # ControllerView.reload_data(self)
                    print("backup succesful, restarting application.")
                    os.execl(sys.executable, os.path.abspath(__file__), *sys.argv) 
                else:
                    print('Something went wrong with loading the backup, please restart the application.')
                
        else:
            print('Backup not found')
