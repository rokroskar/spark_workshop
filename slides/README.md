# Workshop presentation slides

All of the workshop slides are made with the [`reveal.js`](http://lab.hakim.se/reveal-js/#/) presentation framework. 

If you want to see the slides, you will need to do two things: 

1. get the `reveal.js` library
2. start an HTTP server

## Getting `reveal.js`

`reveal.js` is in the workshop repository as a submodule. To grab the contents of this submodule, you can run

```
spark_workshop/slides > git submodule init
Submodule 'reveal.js' (git@github.com:hakimel/reveal.js.git) registered for path 'reveal.js'

spark_workshop/slides > git submodule update
public-docking-lee-1085:spark_workshop rokstar$ git submodule update
Cloning into 'reveal.js'...
```

Once this is done, the current version of `reveal.js` will be inside the workshop repository. 

## Starting an HTTP server

Launching your own private HTTP server is very straightforward: 

```
spark_workshop/slides > python -m SimpleHTTPServer 8000
```

Now you have a server running locally on port 8000 and can connect to it by going to http://localhost:8000

If you have the server running now and the `reveal.js` library installed, you can click on the links below to access the workshop slides (assuming the port is 8000):

[Introduction to Distributed Data Analysis](http://localhost:8000/workshop_intro/Introduction.html)

[Python concepts](http://localhost:8000/python_intro/Python_concepts.slides.html)

[Introduction to the Spark Framework](http://localhost:8000/spark_intro/Spark_intro.html)

## Rebuilding slides out of a notebook

If you need to rebuild the slides in `python_intro` (or for any other notebook in this tutorial), do not use the `reveal.js` library included here (there is a [version compatibility problem](http://stackoverflow.com/questions/30125373/ipython-notebook-to-slides-reveal-is-not-defined)).

To use a specific version and load it dynamically, build the python introduction slides like so: 

```
spark_workshop/slides/python_intro > jupyter nbconvert --to slides --reveal-prefix "http://cdn.jsdelivr.net/reveal.js/2.6.2" Python_concepts.ipynb
```


