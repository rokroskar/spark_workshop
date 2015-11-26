#!/usr/bin/env python
from __future__ import print_function
import os
from os.path import expanduser, exists
import subprocess

#
# Initial inspiration for this script from https://github.com/felixcheung/vagrant-projects
#

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
home = expanduser("~")

# setup the path to the jupyter notebook configuration
jupyter_config_path = "{home}/.jupyter_spark_notebook".format(home=home)

# spark home
spark_home = os.environ['SPARK_HOME']

def setup_notebook(port):
    # if the profile doesn't exist, create it -- otherwise we've probably
    # already done this step
    if not exists(jupyter_config_path):
        # get a password
        from notebook.auth import passwd
        
        print(bc.WARNING + '[setup_notebook] '+bc.ENDC+'This script will create a Jupyter notebook profile for working remotely')
        print(bc.WARNING + '[setup_notebook] '+bc.ENDC+'When it is finished, you can find the configuration in %s\n'%(bc.UNDERLINE + jupyter_config_path + bc.ENDC))
        print(bc.WARNING + '[setup_notebook] '+bc.ENDC+'First, we need a *new* password for your Jupyter notebook\n')
        new_pass = passwd()

        print(bc.WARNING + '[setup_notebook] '+bc.ENDC+'Creating an SSL certificate to enable a secure connection\nThe certificate will be in your ~/.ssh directory\n')

        # make an ssl certificate
        certfile = "{home}/.ssh/notebook_cert.pem".format(home=home)

        out = subprocess.check_output(['openssl', 'req', '-x509', '-nodes', '-days', '365', '-newkey', 'rsa:1024', '-keyout', '%s'%certfile, '-out', '%s'%certfile, '-batch'], stderr=subprocess.STDOUT)

        lines = out.split('\n')
        for l in lines : 
            print(bc.OKGREEN + '[openssl] ' + bc.ENDC + l)
        
        # write the notebook config

        # create the directory
        os.makedirs(jupyter_config_path)
        with open("{profile_path}/jupyter_notebook_config.py".format(profile_path=jupyter_config_path), 'w') as f:
            f.write(notebook_config_template.format(
                password=new_pass, certfile=certfile, port=port))
        
        print(bc.WARNING + '[setup_notebook] '+ bc.BOLD + 'Notebook setup complete' + bc.ENDC)
            
    else:
        print(bc.FAIL + "The jupyter notebook already looks set up -- if this is not the case, delete {dir} and run the script again.".format(dir=jupyter_config_path) + bc.ENDC)

def launch_notebook(port):
    # launch the notebook
    import sys
    import re
    import socket
    from IPython.terminal.ipapp import launch_new_instance
    argv = sys.argv[:1]
    argv.append('notebook')

    argv.append('--config={profile_path}/jupyter_notebook_config.py'.format(profile_path=jupyter_config_path))

    # check if we passed in a port that is different from the one in the
    # configuration
    with open("{profile_path}/jupyter_notebook_config.py".format(profile_path=jupyter_config_path), 'r') as conf:
        conf_port = int(re.findall('port = (\d+)', conf.read())[0])

    if conf_port != port:
        print(bc.WARNING + "Overriding the port found in the existing configuration" + bc.ENDC)
        argv.append('--port={port}'.format(port=port))

    # determine if we're running on a compute node
    if 'LSB_HOSTS' in os.environ:
        compute = True
    else:
        compute = False

    sys.argv = argv

    if compute:
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = 'localhost'

    print(bc.BOLD + "To access the notebook, inspect the output below for the port number, then point your browser to https://{ip}:<port_number>".format(ip=ip) + bc.ENDC)
    launch_new_instance()

def launch_spark(port, spark_options, spark_conf):
    # launch the notebook
    import sys
    import re
    import socket
    import os
    import subprocess

    # set this to whatever python executable you want to use
    os.environ['PYSPARK_PYTHON'] = subprocess.check_output('which python', shell=True).rstrip()

    os.environ['PYSPARK_DRIVER_PYTHON'] = "jupyter"
    os.environ['PYSPARK_DRIVER_PYTHON_OPTS'] = \
        "notebook --config {profile_path}/jupyter_notebook_config.py".format(profile_path=jupyter_config_path)

    if spark_conf is not None:
        os.environ['SPARK_CONF_DIR'] = spark_conf

    # check if we passed in a port that is different from the one in the
    # configuration
    with open("{profile_path}/jupyter_notebook_config.py".format(profile_path=jupyter_config_path), 'r') as conf:
        conf_port = int(re.findall('port = (\d+)', conf.read())[0])

    if conf_port != port:
        print(bc.WARNING + "Overriding the port found in the existing configuration" + bc.ENDC)
        os.environ['PYSPARK_DRIVER_PYTHON_OPTS'] += ' --port={port}'.format(port=port)

    # determine if we're running on a compute node
    if 'LSB_HOSTS' in os.environ:
        compute = True
    else:
        compute = False

    if compute:
        ip = socket.gethostbyname(socket.gethostname())
    else:
        ip = 'localhost'

    print(bc.BOLD + "To access the notebook, inspect the output below for the port number, then point your browser to https://{ip}:<port_number>".format(ip=ip) \
+ bc.ENDC)
    
    args = ["{spark_home}/bin/pyspark".format(spark_home=spark_home)]

    if spark_options is not None: 
        for opt in spark_options.split(' '): 
            args.append(opt)

    print(args)

    subprocess.call(args)


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

    parser.add_argument('--spark', dest='spark', action='store_true',
                        default=False, help='launch the notebook with a spark backend')                        

    parser.add_argument('--spark_options', dest='spark_options', action='store', 
                        default=None, help='options to pass to spark')

    parser.add_argument('--spark_conf', dest='spark_conf', action = 'store', 
                        default=None, help='spark_configuration_directory')

    args = parser.parse_args()

    port = args.port

    if args.setup:
        setup_notebook(port)
    if args.launch:
        launch_notebook(port)
    if args.spark: 
        launch_spark(port, args.spark_options, args.spark_conf)

    if not args.setup and not args.launch and not args.spark:
        parser.print_help()
