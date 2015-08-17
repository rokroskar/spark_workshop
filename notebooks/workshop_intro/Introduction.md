
# Distributed Data Analysis  

(for scientists) <!-- .element: style="font-size:75%;text-align:center" -->

### Scientific IT Services // ETH Zürich



## Purpose

What are we doing here? 

* presumably, you have some sort of a "data problem"
* you live in constant fear that your "data problem" will outgrow even your group's new shiny workstation
* you do some work in the batch queue of a cluster, but you find this limiting and rigid
* you've heard of "big data" tools, but it always seems like such a pain to get going with them

Hopefully we'll be able to address some of these problems!



### Who am I? 

* Rok Roškar --> I work for the SIS Research Informatics group
* background (PhD) in theoretical astrophysics -- spent many years running large simulations on supercomputers
* dove into "big data" tools about a year ago, trying to come up with a solution for a D-GESS project



## Big Data 
### Everyone is talking about it... but no one knows what it is

1 Gb? 50 Gb? 500 Gb? 500 Tb? 1 Pb? <!-- .element: style="text-align:center" -->

It doesn't matter! <!-- .element: style="text-align:center;font-weight:bold" class="fragment" data-fragment-index="1"-->

* "Big data" is when you start to seriously worry that your analysis will never complete <!-- .element: class="fragment" data-fragment-index="2" -->
* this could be due to memory or runtime <!-- .element: class="fragment" data-fragment-index="2" -->



## *Data exploration enables scientific discovery*
Big or small data isn't the point: we want to enable scientific discovery <!-- .element: class="fragment" data-fragment-index="1" -->

This happens through efficient data exploration, irrespective of size <!-- .element: class="fragment" data-fragment-index="2" -->

Static batch pipelines (think endless scripts) <!-- .element: class="fragment" data-fragment-index="3" -->

vs. limber, flexible, interactive, visual analysis <!-- .element: class="fragment" data-fragment-index="4" style="text-align:right"-->



### Unfortunately, data outgrows resources rather quickly...

#### ... so we have to try and "scale" our workflows <!-- .element: class="fragment" data-fragment-index="1" -->



<!-- .slide: data-background="figs/laptop_workstation.svg" data-background-size="contain" -->
### First try: move from laptop to a workstation 

* more memory! problem solved? handled by operating system...
* more cores! special libraries can provide simple multithreading support
* still, we want analysis on Tb of data at interactive speeds! 

*Obtain results* of a model within seconds of changing a parameter; 

*discover relationships* in high-dimensional data by slicing, dicing, reducing, visualizing

A single workstation will not cut it, and if it does for a problem today, it certainly won't tomorrow. 



<!-- .slide: data-background="figs/cluster-computing.svg" data-background-size="contain" -->
### Next, move to a *cluster* 

* a set of interconnected servers steered through some common gateway <!-- .element: class="fragment" data-fragment-index="1" -->
* easy for "embarrasingly" parallel work-loads <!-- .element: class="fragment" data-fragment-index="1" -->
* book-keeping nightmare (tons of files, intermediate products etc.) <!-- .element: class="fragment" data-fragment-index="1" -->
* not so easy for really parallel computation <!-- .element: class="fragment" data-fragment-index="1" -->
* definitely not easy for interactive use and data exploration <!-- .element: class="fragment" data-fragment-index="1" -->



What's so hard about distributed analysis/computation? 

* data and tasks need to be *coordinated* between the different machines
* consumption of data and production of results has to be controlled
* partial results calculated on various parts of the system need to be assembled for the user
* in a "true" parallel environment, this is done via very complicated sequences of communication library calls
* no longer have one machine but many, potentially hundreds --> hard to debug/control!



## Liberation through limitation

General multiprocessing/parallel libraries (e.g. MPI)
* give the user a lot of control and flexibility
* they are *very* hard to use and debug!
* not great for fast turn-around of home-grown code!

<hr class="fragment visible" data-fragment-index="0">

<h4 class="fragment visible" data-fragment-index="0">What if we only allowed the user a very rigid programming model?</h4>

<ul style="text-align:left" class="fragment visible" data-fragment-index="0">
<li>more robust out-of-the-box</li>
<li>predictable</li>
<li>easier to monitor, discover failures etc.</li>
</ul>


<!-- .slide: data-background="figs/mapreduce-background.svg" data-background-size="contain" -->


<!-- .slide: data-background="figs/mapreduce-background.svg" data-background-size="contain" data-state="blur"-->
####**MapReduce** is such a programming paradigm

We all know this to some extent --> it's all around us <!-- .element class="fragment" data-fragment-index="1" style="text-align:center"-->

* Web 2.0 <!-- .element class="fragment" data-fragment-index="2" -->
    * multimedia content (images, video, music/audio) 
    * user activity tracking 
    * recommendation engines (shopping, movies, ads. etc.) 
* Sensors <!-- .element class="fragment" data-fragment-index="3" -->
    * smartphone 
    * real-world, internet of things 
* Public infrastructure <!-- .element class="fragment" data-fragment-index="4" -->
    * telecom
    * transportation (trains, traffic)
* Science <!-- .element class="fragment" data-fragment-index="5" -->
    * CERN 
    * astronomy sky surveys
    * medicine + genomics --> translational science
    * high-content screening, lightsheet microscopy
    * social science

Many of these "production" systems based on MapReduce combined with efficient "data stores" (distributed databases etc) <!-- .element class="fragment" data-fragment-index="6" -->


<!-- .slide: data-background="figs/mapreduce-background.svg" data-background-size="contain" data-state="blur"-->
### Basic building block: the Distributed Filesystem

#### Moving data around is very expensive! 

* modern data centers consist of 1000s of machines
* often, this is "commodity" hardware (not like our Brutus/Euler)
* network between machines might be sluggish
* bring computation/algorithm to the data




#### Most common is the open source Apache Hadoop 

* Java-based MR implementation 
* used together with the Hadoop Distributed File System (HDFS)
* important feature: "bringing computation *to the data*"
* computation and storage are on the same machines!
