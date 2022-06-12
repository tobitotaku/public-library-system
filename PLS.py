# entrypoint of the application
# from config import configurationhelper
from datahelpers import DataResolver, JSONDataLayer, TargetFile
from loanManager import LoanManager
from userManager import UserManager
from utils import getNewId, getNewIdTarget
from models import Book, BookItem, LibraryAdmin, Person, Member
from catalog import Catalog
# from usermodels import LibraryAdmin, Person, Member
from controllers.maincontroller import *
from backup import Backup

MainCV().render_menu()
