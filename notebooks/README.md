# Spark tutorial notebooks

## Using this material 

See the [general README](../README.md) for information on how to get started. Once you have the notebook running, you can dive in to the three directories:

* [Python concepts introduction](https://github.com/rokroskar/spark_workshop/tree/master/notebooks/python_intro) - basic introduction to Big Data and python concepts
* [Introduction to Spark](https://github.com/rokroskar/spark_workshop/tree/master/notebooks/spark_intro) - essential Spark skills
* [Analyzing the Gutenberg Corpus](https://github.com/rokroskar/spark_workshop/tree/master/notebooks/gutenberg) - "project" notebook building up an analysis of the Gutenberg books corpus
* [Using DataFrames to analyze Twitter](https://github.com/rokroskar/spark_workshop/tree/master/notebooks/twitter_dataframes)

You should start by having a look at the python introduction notebook (where you can also execute cells) which introduces some essential python concepts. When you open the notebooks running on the notebook server (i.e. in your browser at `localhost:8889`), you can execute any cell in the notebook by entering `Shift+Enter`. You can also modify any of the cells to experiment. Once you're happy with the python introduction, continue on to the notebook marked "EMPTY" in the same directory and complete the exercises.  

## Tutorial content

The two introductory tutorials cover the basics to get you started with Spark using Python. The Gutenberg tutorials are the start of the more advanced content. Part 1 focuses on basic data manipulation in RDDs. Parts 2 and 3 cover the following:

* Part 2: Gutenberg N-gram Viewer: 
  * using broadcast variables as lookup tables
  * use of `mapPartitions` to reduce memory pressure
  * using `reduceByKey` to gain insight of the data content
  * efficient use of pre-partitioning to reduce shuffle and lookup times
  * using vectors in `(key, value)` pair RDDs
  * aggregation using custom aggregators 
* Part 3: Building a language model: 
  * identifying and correcting data skew
  * using generator functions to lower the memory footprint
  * using broadcast variables as lookup tables
  * preparing data for use with [MLlib](http://spark.apache.org/docs/latest/mllib-guide.html)
  * training a classification model and assessing its performance
* Twitter DataFrames
  * using the `DataFrame` API to process twitter data
  * contrasting `DataFrame` `groupBy` with RDD `reduceByKey` methods
  * using simple and not-so-simple window functions on time-series data
  * switching between `RDD` and `DataFrame` methods 
