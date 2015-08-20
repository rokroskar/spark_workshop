# Analyzing the Gutenberg Project book corpus

The [Gutenberg Project](http://link) hosts books in the public domain in many languages. Here, we will first use the English book corpus to construct an "N-Gram viewer" and later we will combine this with the German book corpus to develop a language model. 

The corpus is not "Big Data" per-se, but it is big enough that it cannot be comfortably analyzed on a laptop. We will do the analysis using Spark running on nodes controlled by a YARN resource manager. Our analysis will be done interactively by spawning a Jupyter notebook on the remote cluster and connecting to it from the comfort of a browser on the laptop.


## Cluster setup

There are a few things we need to get configured before we can use the 

### Getting the workshop repository

Log in to your account on the cluster and clone the repository:

```
$ ssh username@cluster
cluster~ $ git clone https://github.com/rokroskar/spark_workshop.git
```

### Install python dependencies

Once again, the python dependencies are the same as above. If you are a python user already and you know what you are doing, just install `python2.7`, `numpy`, `matplotlib`, and `ipython` (v4.0) and `jupyter`. 

If you are already a conda/miniconda user, you can simply do 

```
cluster~ $ conda -y create -n spark_workshop python>=2.7 numpy pip ipython jupyter matplotlib
cluster~ $ source activate spark_workshop
```

If you are not sure how to navigate the python universe, you can use the `setup_cluster.sh` script in the `scripts` directory like so:

```
cluster~ $ module load python
cluster~ $ cd spark_workshop
cluster~/spark_workshop $ scripts/setup_cluster.sh
```

You will see a lot of activity while the python packages are downloaded and configured. 


### Configure the Jupyter Notebook

When the python installation process is complete, you can set up the jupyter notebook just like we did before on the laptop/VM: 

```
cluster~ spark_workshop $ scripts/start_notebook.py --setup
```

Only run the setup part now -- we will launch it later from an interactive job running on one of the compute nodes of the cluster. 


### Set up a secure tunnel to the cluster

In order to work with the cluster interactively, we need to set up a secure proxy to the cluster. Once this channel is open, we will then instruct the Firefox browser to direct all traffic over this secure channel. This way, we will be able to access our notebook that is running on the firewalled cluster. 

#### On Linux or Mac OS X

Open up the terminal/console and open a dynamic port forward to the cluster head node:

```
$ ssh -Nf -D 9999 username@cluster
```

You might be prompted for a password, but then nothing much will happen: the tunnel will work in the background and will remain active as long as you maintain an internet connection. This is especially nice if you have a long working session and you don't want to worry about accidentaly closing a terminal window. If you want the prompt for some reason, ommit the `-Nf` flags.

#### On Windows

Start up PuTTY and enter your cluster name into the host field. On the left, scroll down to "SSH" options and find "Tunnel". Check the "Dynamic" radio button, enter 9999 into the "Host Port" field and click "Add" so that the window shows "D9999". Then connect to the host and enter your user credentials. You must keep the PuTTY window open to maintain the connection. 

#### Configuring the Firefox browser

Go to the `Settings` or `Preferences` --> `Advanced`, and click on `Network`: 

![firefox_settings](../figs/firefox_settings.png)

Click on `Settings` and configure the proxy settings as shown here: 

![firefox_proxy](../figs/firefox_proxy.png)

Now your Firefox browser's traffic is being routed through the cluster head node. This makes the otherwise inaccessible compute nodes available. 


### Obtain an interactive job on the cluster

Every Spark job consists of a driver application and tasks running on executors. The driver orchestrates the flow of the analysis and can sometimes consume significant resources. When we run applications in interactive mode, it is therefore imperative to first obtain resources for the driver, and then use it to start the Spark job. 

We obtain resources by requesting an interactive job in the normal job queue on the HPC cluster. In LSF, this is done with a line like

```
cluster~/ $ bsub -Is -W 4:00 -n 12 bash
```

After a brief while (hopefully not longer than a minute or two) the system will grant us the job and we will be given a bash prompt on one of the compute nodes, i.e. something like 

```
a6583~/ $ 
```

First, make sure your python environment is set up correctly by running the `setup_cluster.sh` script. Then we can launch the jupyter notebook using the same script as before

```
a6583~/ $ spark_workshop/scripts/setup_cluster.sh
a6583~/ $ spark_workshop/scripts/start_notebook.py 
```
