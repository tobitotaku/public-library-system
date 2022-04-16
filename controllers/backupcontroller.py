from controllers.controllers import ControllerView

class BackupCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized
        self.actions = [
            (self.render_list, "List"),
            (self.render_add, "Add"),
            (self.render_load_backup, "Edit"),
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
        if backupid in self.backups:
            loadbackup = self.backups[backupid]
            print(f'Backup {backupid}.{loadbackup} selected')
            confirm = input('Confirm loading backup? (y/Enter)')
            if confirm == 'y':
                self.backup.loadBackup()
                print(f'Backup {backupid}.{loadbackup} loaded')
