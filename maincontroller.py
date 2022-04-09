from controllers import *
from userscontroller import *
from catalogcontroller import *

class MainCV(ControllerView):
    def __init__(self, *args):
        not self.initialized if ControllerView.__init__(self, *args) else self.initialized

        self.usercv = MembersCV(ControllerView)
        self.actions = [
            (self.usercv.render_menu, "Manage Members"),
            # (self.render_add_member, "Add a member"),
            # (self.render_edit_member, "Edit a member"),
            # (self.render_delete_member, "Delete a member"),
            (exit, "Exit application"),
        ]
        self.render_menu()