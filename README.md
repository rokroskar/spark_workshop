# Distributed data analysis
This workshop demonstrates some techniques for pre/post processing large 
data sets, which do not fit onto a single machine. While there are many 
methods to accomplish such a task, here we focus on the *map/reduce* (MR) 
paradigm that has gained a lot of traction in industry, but only seldom in 
academia. To explore the possibilities of using such a framework, we make 
use of [Spark](http://spark.apache.org), which is a modern MR framework with a 
rich API and properties attractive for data exploration. 

## Prerequisites

### Programming knowledge

We assume fluency with basic programming constructs such as loops and functions. In the first session of the workshop, basics of functional programming and other python-specific constructs are introduced, as they are  useful for writing Spark applications. Knowing how to use the command line (or terminal) is also expected. 

### Python

The language used in the workshop is python. If you are not familiar with python at all, we recommend finding a basic tutorial and working through some examples before participating in the workshop. 

## Setting up

There are quite a few requirements for all the software used in this workshop to function properly. You can either install it all by hand (or perhaps you have it installed already), but if you don't want to bother with the set up, you can simply use the virtual machine option. 

### Easiest Setup: use a Virtual Machine

If you want to simply get up and running, then we recommend you use the 
workshop materials through the Virtual Machine environment set up specifically
for this purpose. This way you will only have to deal with the minimal set of
installations.

Download and install [Vagrant](https://www.vagrantup.com/downloads.html) and 
[VirtualBox](https://www.virtualbox.org/wiki/Downloads). Then you can simply
open up a terminal, navigate to this repository and type 

```bash
$ vagrant up
```

This will first download, configure, and boot the virtual machine (VM). The first time you do this, it has to download everything off the internet so it
will take some time. Once it's finished, you can log in to the VM with
```bash
$ vagrant ssh
```

To shut down the VM temporarily, you can do
```
$ vagrant halt
```

or to get rid of it completely

```
$ vagrant destroy
```



### Advanced setup 
If you want to run Spark from your own machine and you really want to do 
the setup yourself, or if you are an experienced user, you can follow 
the instructions below. 

#### python dependencies

The python installation should have the following packages: numpy, scipy, scikit-learn, pip, ipython, ipython notebook, matplotlib

If you are not sure how to meet these dependency requirements, we recommend 
that you [download the miniconda installer](http://conda.pydata.org/miniconda.html) appropriate for your system. Once it's installed, run the following commands: 

    > conda update conda 
    > conda install -y numpy scipy scikit-learn pip ipython ipython-notebook matplotlib


#### Java
You need a JDK installed. 

#### Spark

Spark requires a Java installation -- if you don't have it already (most systems come with some flavor of Java installed), you can get it [here](https://java.com/en/download/).

Once you have java installed, grab a spark hadoop 2.6 compiled binary package from http://spark.apache.org/downloads.html and extract it somewhere. Then create a symbolic link in your home directory to this location: 

    > ln -s /path/to/spark/package ~/spark
  
To make your life easier later on, add this line to your `.bashrc` (or whatever startup file is appropriate for the shell you are using): 

    export SPARK_HOME=~/spark

Now source the file you just added this line to, e.g. 

    > source .bashrc
  
and try to run a basic spark example to see if everything is working: 

    > $SPARK_HOME/bin/spark-submit $SPARK_HOME/examples/src/main/python/pi.py 10

## Using this material

Notebooks can be downloaded and run on a local machine or any spark cluster. 
The notebooks are created using `ipython` `v3.1.0` and will probably not work with earlier versions. 

### Running in the VM

If the VM is not running, start it with `vagrant up`. Then:
```
$ vagrant up
Last login: Tue Jul  7 13:26:09 2015 from 10.0.2.2
[vagrant@sparkws ~]$
```

Go to the `notebooks` directory and start the ipython notebook
```
[vagrant@sparkws ~]$ cd notebooks
[vagrant@sparkws notebooks]$ ipython notebook
```

This will bring up a firefox window with the ipython notebook. 

### Running localy without a VM

Once you have `ipython` installed, you can simply type 

    > ipython notebook 
 
in the base directory and select the notebook you are interested in. Alternatively, you can view the 
notebooks as slides by using the notebook conversion feature of ipython: 

    > ipython nbconvert --to slides --post serve <notebook_path>

This will convert the notebook to html and display the slides in your browser using the [Reveal.js](https://github.com/hakimel/reveal.js/) library. 



## Outline
### Basics

* map/reduce/filter operations
* some python concepts that are useful for Spark
   * lambda functions
   * list comprehensions (generator expressions) 
   * generators (needed for mapPartitions)
   * key/value tuples

### Applying the basics in Spark
* description of Spark data and computation model (RDDs)
* different ways of running Spark apps 
   * local (i.e. laptop)
   * stand-alone (i.e. Euler)
   * YARN (Brutus cluster)
   * Amazon EC2
* map/reduce in Spark
   * intro to the computation graph
   * creating key, value RDDs
   * standard library functions (reduceByKey, aggregate, sortBy, etc.)

### Advanced
* optimizations/profiling
* writing aggregator classes

