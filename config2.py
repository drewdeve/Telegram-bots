from enum import Enum

token = "1374553384:AAGvnXdFeO2nCbukRzgw0OPvtIj9_UEsN8o"
db_file = "database.vdb"

class States(Enum):
    S_START = "0"
    S_ENTER_NAME = "1"
    S_ENTER_AGE = "2"
    S_SEND_PIC = "3"