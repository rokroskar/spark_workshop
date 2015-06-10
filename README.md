# Distributed data analysis
This workshop will try to show some techniques for processing large data sets that do not fit into a single machine. 
While there are many methods to accomplish such a task, we will focus on the *map/reduce* (MR) paradigm that has
gained a lot of traction in industry, but only seldom in academia. To explore the possibilities of using 
such a framework, we will make use of [Spark](http://spark.apache.org), which is a modern MR framework with a rich
API and many properties which make it attractive for data exploration. 

## Prerequisites

To work with this material, you will need: 

* a python installation including ipython and ipython notebook.
    * python packages: numpy, scikit-learn, scipy, itertools (note: make a miniconda script that grabs all the dependencies)
* [spark](http://spark.apache.org): grab a hadoop 2.6 compiled binary from http://spark.apache.org/downloads.html


## Using this material

Notebooks can be downloaded and run on a local machine or any spark cluster. 
The notebooks are created using `ipython` `v3.1.0` and will probably not work with earlier versions. 

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

