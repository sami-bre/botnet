import sqlite3

class DatabaseHelper:
    def __init__(self, databaseName):
        self._connection = sqlite3.connect(databaseName)

    def setUpDatabase(self):
        self._connection.execute('create table if not exists zombies (id INTEGER PRIMARY KEY, command TEXT)')
        self._connection.execute('delete from zombies')
        self._connection.commit()

    def readZombiesTable(self):
        cur = self._connection.execute('select * from zombies')
        return cur.fetchall()

    def readOneZombieTable(self, zid):
        cur = self._connection.execute('select * from z{}'.format(zid))
        return cur.fetchall()

    def writeCommand(self, zid, command):
        # used to set the waiting command for a certain zombie (for administration purpose)
        cur = self._connection.execute('update zombies set command="{}" where id={}'.format(command, zid))
        self._connection.commit()
        return cur.fetchall()

    def getLastId(self):
        cur = self._connection.execute("select id from zombies order by id desc limit(1)")
        res = cur.fetchall()
        # cur.fetchall returns a list of tuples (that's what a table is)
        last_id = 0 if len(res)==0 else int(res[0][0])
        return last_id

    def writeResult(self, zid, command, result):
        # returns empty list if seccessful
        cur = self._connection.execute("insert into z{} values ('{}','{}');".format(zid, command, result))
        self._connection.commit()
        return cur.fetchall()

    def idExists(self, id):
        cur = self._connection.execute("select id from zombies where id='{}'".format(id))
        result = cur.fetchall()
        if len(result) == 1:
            return True
        elif len(result) == 0:
            return False
        else:
            raise Exception('More than one zombie found in the database with the same ID.')

    def registerZombie(self, zid):
        # add into the zombies table
        self._connection.execute("insert into zombies (id, command) values ('{}', '{}')".format(zid, "die"))
        # create a table for the execution history of this particular zombie.
        # the die command here means that all zombies die after the newcomer_command. I'll see their result
        # for the newcomer_command and revive them if they're interesting.
        self._connection.execute("create table z{} (command, response)".format(zid))
        self._connection.commit()

    def readWaitingCommand(self, zid):
        # return the command I've put in the database for the zombie
        # the command waiting to be sent is stored in the zombies table next to the id of the zombie.
        cur = self._connection.execute("select command from zombies where id='{}'".format(zid))
        result = cur.fetchall()
        # if len(result) != 1, it means there's more or less than 1 zombie with the same zid
        assert(len(result) == 1)
        command = result[0][0]
        return command


    def close(self):
        self._connection.close()


# a context manager that gives a DatabseHelper object
class OpenDatabase:
    def __init__(self, database_name):
        self.database_name = database_name

    def __enter__(self):
        self.helper = DatabaseHelper(self.database_name)
        return self.helper

    def __exit__(self, exc_type, exc_value, exc_tb):
        self.helper.close()
