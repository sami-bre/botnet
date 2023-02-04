# botnet
a botnet consisting of zombies and central control.

The zombies (zombie.py) are python scripts that need to somehow make their way into the host computer and ... into the startup directory.
there's no mechanism built into the code in this repository to achieve that. It'll be a job for the future. If you want to test it now, you 
first need to manually put the zombie script on your machine and execute it. Also, don't
forget to run the flask app locally (as a web server) and tweak the zombie script to give it the correct address of the flask app.) But once
the zombie starts executing on a host computer, the magic starts to unfold :)

The zombie connects to a central controll (the fask app hosted somewhere - the wsgi.py file) and sets itself up for accepting and
executing terminal commands. A master script (running on the hacker's machine) will be able to connect to the central command to set commands
that shall be fetched and executed by each zombie.

The flow of events is as follows: a new zombie script starts executing on a host, it fetches a default command for newcomer zombies,
executes it and sends the result of execution back to the central command to be stored. The master script later fetches the result of
execution and allows the hacker to inspect it. The hacker then set's another command through the master script so the zombie fetches this
new command, executes and sends the result of execution to the command again. The cycle continues till the hacker set's a special command
that makes the zombie shut down every time it's read. This effectively gives the hacker an administrative power (depending on the privilege of
the zombie script on the host system) on multiple host systems at once.
