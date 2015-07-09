#!/usr/bin/env python

notebook_config_template = """c = get_config()
c.NotebookApp.ip = '*'
c.NotebookApp.open_browser = False
c.NotebookApp.password = "{password}"
c.NotebookApp.certfile = "{certfile}"
c.NotebookApp.port = 8889
"""


def setup_notebook():
    # get home directory
    import os
    from os.path import expanduser, exists
    home = expanduser("~")

    ipython_profile_path = "{home}/.ipython/profile_sparkbook".format(
        home=home)

    # if the profile doesn't exist, create it -- otherwise we've probably
    # already done this step
    if not exists(ipython_profile_path):
        os.system("ipython profile create sparkbook")

        # get a password
        from IPython.lib import passwd

        new_pass = passwd()

        # make an ssl certificate
        import os
        certfile = "{home}/.ssh/notebook_cert.pem".format(home=home)
        os.system(
            "openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout {certfile} -out {certfile} -batch".format(certfile=certfile))

        # write the notebook config
        with open("{profile_path}/ipython_notebook_config.py".format(profile_path=ipython_profile_path), 'w') as f:
            f.write(notebook_config_template.format(
                password=new_pass, certfile=certfile))

    else:
        print "The ipython notebook already looks set up -- if this is not the case, delete {dir} and run the script again.".format(dir=ipython_profile_path)


def launch_notebook():
    # launch the notebook
    import sys
    from IPython.terminal.ipapp import launch_new_instance
    argv = sys.argv[:1]
    argv.append('notebook')
    argv.append('--profile=sparkbook')
    sys.argv = argv
    print "\033[1mTo access the notebook, inspect the output below for the port number, then point your browser to https://localhost:<port_number>\033[0m\n"
    launch_new_instance()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description='Setup and launch a python notebook set up to serve a Spark session')
    parser.add_argument('--setup', dest='setup', action='store_true',
            			default=False, help='setup the notebook (does not launch)')

    parser.add_argument('--launch', dest='launch', action='store_true',
    					default=False, help='launch the notebook')

    args = parser.parse_args()

    if args.setup : setup_notebook()
    if args.launch: launch_notebook()

    if not args.setup and not args.launch : 
    	print '*****************************************************'
    	print 'Please specify either "--setup" or "--launch" or both'
    	print '*****************************************************'
    	parser.print_help()

   	
