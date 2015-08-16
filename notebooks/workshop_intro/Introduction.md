
# Distributed Data Analysis  

(for scientists)

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

1 Gb? 50 Gb? 500 Gb? 500 Tb? 1 Pb? 

**It doesn't matter! ** <!-- .element: class="fragment" data-fragment-index="1" -->

* "Big data" is when you start to seriously worry that your analysis will never complete <!-- .element: class="fragment" data-fragment-index="2" -->
* this could be due to memory or runtime <!-- .element: class="fragment" data-fragment-index="2" -->



## *Data exploration enables scientific discovery*
Big or small data isn't the point: we want to enable scientific discovery

This happens through efficient data exploration, irrespective of size

Static, complicated, batch pipelines vs. limber, flexible, interactive analysis 



### Unfortunately, our data outgrows our resources rather quickly...

#### ... So we have to try and "scale" our workflows <!-- .element: class="fragment" data-fragment-index="1" -->



First try: move from laptop to a workstation

<img src="https://raw.githubusercontent.com/rokroskar/spark_workshop/master/notebooks/figs/laptop_workstation.png?token=ADMr8uMMwA8iTKzHy4z2SAwdKuxTuWHhks5V10nZwA%3D%3D">

* more memory! problem solved? handled by operating system...
* more cores! special libraries can provide simple multithreading support
* still, we want analysis on Tb of data at interactive speeds! 

*Obtain results* of a model within seconds of changing a parameter; 

*discover relationships* in high-dimensional data by slicing, dicing, reducing, visualizing

A single workstation will not cut it, and if it does for a problem today, it certainly won't tomorrow. 



Next, move to a *cluster* 

a set of interconnected servers steered through some common gateway

<img src="https://raw.githubusercontent.com/rokroskar/spark_workshop/master/notebooks/figs/cluster-computing.png?token=ADMr8vpYR6DRDeRu8zTuySiCGIIWdqUYks5V2JG2wA%3D%3D">


* easy for "embarrasingly" parallel work-loads
* book-keeping nightmare (tons of files, intermediate products etc.)
* not so easy for really parallel computation 
* definitely not easy for interactive use and data exploration

What's so hard about distributed analysis/computation? 

* data and tasks need to be *coordinated* between the different machines
* consumption of data and production of results has to be controlled
* partial results calculated on various parts of the system need to be assembled for the user
* in a "true" parallel environment, this is done via very complicated sequences of communication library calls
* no longer have one machine but many, potentially hundreds --> hard to debug/control!


## Liberation through limitation

What if we only allowed the user a very rigid programming model? 

This makes a system more robust out-of-the-box, predictable, and easier to monitor, discover failures etc. 

**MapReduce** is such a programming paradigm

<img src="https://raw.githubusercontent.com/rokroskar/spark_workshop/master/notebooks/figs/mapreduce.png?token=ADMr8i8bUDYu28G-28pF9ivkU8whgCaTks5V2Ka6wA%3D%3D" width=850>

We all know this to some extent --> it's all around us

* Web 2.0
    * multimedia content (images, video, music/audio)
    * user activity tracking
    * recommendation engines (shopping, movies, ads. etc.)
* Sensors
    * smartphone
    * real-world, internet of things
* Public infrastructure
    * telecom
    * transportation (trains, traffic)
* Science
    * CERN 
    * astronomy sky surveys
    * medicine + genomics --> translational science
    * high-content screening, lightsheet microscopy
    * social science

Many of these "production" systems based on MapReduce combined with efficient "data stores" (distributed databases etc)

Most common is the open source Apache **Hadoop**

* Java-based MR implementation
* used together with the Hadoop Distributed File System (HDFS)
* important feature: "bringing computation *to the data*"



```python

# THE LINES BELOW ARE JUST FOR STYLING THE CONTENT ABOVE !

from IPython import utils
from IPython.core.display import HTML
import os
def css_styling():
    """Load default custom.css file from ipython profile"""
    base = utils.path.get_ipython_dir()
    styles = """<style>
    
    @import url('http://fonts.googleapis.com/css?family=Source+Code+Pro');
    
    @import url('http://fonts.googleapis.com/css?family=Kameron');
    @import url('http://fonts.googleapis.com/css?family=Crimson+Text');
    
    @import url('http://fonts.googleapis.com/css?family=Lato');
    @import url('http://fonts.googleapis.com/css?family=Source+Sans+Pro');
    
    @import url('http://fonts.googleapis.com/css?family=Lora'); 
    @import url(https://fonts.googleapis.com/css?family=Ubuntu:300,700,300italic,700italic);
    
    body {
        font-family: Ubuntu, sans-serif;
    }
    .rendered_html code
    {
        color: black;
        background: #eaf0ff;
        padding: 1pt;
        font-family:  'Source Code Pro', Consolas, monocco, monospace;
    }
    
    .CodeMirror pre {
    font-family: 'Source Code Pro', monocco, Consolas, monocco, monospace;
    }
    
    .cm-s-ipython span.cm-keyword {
        font-weight: normal;
     }
        
    div #notebook {
        font-size: 12pt; 
        line-height: 145%;
        }
        
    li {
        line-heigt: 175%;
    }

    div.output_area pre {
        background: #fffdf0;
        padding: 3pt;
    }
    
    h1, h2, h3, h4 {
        font-family: Kameron, arial;
    }
    
    div#maintoolbar {display: none !important;}
    </style>"""
    return HTML(styles)
css_styling()
```




<style>
    
    @import url('http://fonts.googleapis.com/css?family=Source+Code+Pro');
    
    @import url('http://fonts.googleapis.com/css?family=Kameron');
    @import url('http://fonts.googleapis.com/css?family=Crimson+Text');
    
    @import url('http://fonts.googleapis.com/css?family=Lato');
    @import url('http://fonts.googleapis.com/css?family=Source+Sans+Pro');
    
    @import url('http://fonts.googleapis.com/css?family=Lora'); 
    @import url(https://fonts.googleapis.com/css?family=Ubuntu:300,700,300italic,700italic);
    
    body {
        font-family: Ubuntu, sans-serif;
    }
    .rendered_html code
    {
        color: black;
        background: #eaf0ff;
        padding: 1pt;
        font-family:  'Source Code Pro', Consolas, monocco, monospace;
    }
    
    .CodeMirror pre {
    font-family: 'Source Code Pro', monocco, Consolas, monocco, monospace;
    }
    
    .cm-s-ipython span.cm-keyword {
        font-weight: normal;
     }
        
    div #notebook {
        font-size: 12pt; 
        line-height: 145%;
        }
        
    li {
        line-heigt: 175%;
    }

    div.output_area pre {
        background: #fffdf0;
        padding: 3pt;
    }
    
    h1, h2, h3, h4 {
        font-family: Kameron, arial;
    }
    
    div#maintoolbar {display: none !important;}
    </style>




```python

```
