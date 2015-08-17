#!/usr/bin/env python

notebook_config_template = """c = get_config()
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.password = "{password}"
c.NotebookApp.certfile = "{certfile}"
c.NotebookApp.port = {port}
"""

default_port = 8889

class bc:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# get home directory
import os
from os.path import expanduser, exists
home = expanduser("~")

ipython_profile_path = "{home}/.ipython/profile_sparkbook".format(home=home)

def setup_notebook(port):
    import os
        
    # if the profile doesn't exist, create it -- otherwise we've probably
    # already done this step
    if not exists(ipython_profile_path):
        os.system("ipython profile create sparkbook")

        # get a password
        from IPython.lib import passwd

        new_pass = passwd()

        # make an ssl certificate
        certfile = "{home}/.ssh/notebook_cert.pem".format(home=home)
        os.system(
            "openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout {certfile} -out {certfile} -batch".format(certfile=certfile))

        # write the notebook config
        with open("{profile_path}/ipython_notebook_config.py".format(profile_path=ipython_profile_path), 'w') as f:
            f.write(notebook_config_template.format(
                password=new_pass, certfile=certfile, port=port))

    else:
        print bc.WARNING+"The ipython notebook already looks set up -- if this is not the case, delete {dir} and run the script again.".format(dir=ipython_profile_path)+bc.ENDC


def launch_notebook(port):
    # launch the notebook
    import sys, re
    from IPython.terminal.ipapp import launch_new_instance
    argv = sys.argv[:1]
    argv.append('notebook')
    argv.append('--profile=sparkbook')

    # check if we passed in a port that is different from the one in the configuration
    with open("{profile_path}/ipython_notebook_config.py".format(profile_path=ipython_profile_path), 'r') as conf :
        conf_port = int(re.findall('port = (\d+)', conf.read())[0])
                  
    if conf_port != port :
        print bc.WARNING+"Overriding the port found in the existing configuration"+bc.ENDC
        argv.append('--port={port}'.format(port=port))

    sys.argv = argv
    print bc.BOLD+"To access the notebook, inspect the output below for the port number, then point your browser to https://localhost:<port_number>"+bc.ENDC
    launch_new_instance()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Setup and launch a python notebook set up to serve a Spark session')
    parser.add_argument('--setup', dest='setup', action='store_true',
            			default=False, help='setup the notebook (does not launch)')

    parser.add_argument('--launch', dest='launch', action='store_true',
    					default=False, help='launch the notebook')

    parser.add_argument('--port', dest='port', action='store', 
                        type=int, help='Port number for the notebook server', default=default_port)

    args = parser.parse_args()

    port = args.port

    if args.setup : setup_notebook(port)
    if args.launch: launch_notebook(port)

    if not args.setup and not args.launch : 
    	print '*****************************************************'
    	print 'Please specify either "--setup" or "--launch" or both'
    	print '*****************************************************'
    	parser.print_help()

   	