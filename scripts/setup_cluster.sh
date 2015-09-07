#!/bin/sh

echo "setting up cluster python environment"
echo "prepending /cluster/apps/spark/miniconda/bin to PATH"
export PATH=/cluster/apps/spark/miniconda/bin:$PATH
source activate spark_workshop
echo "removing everything from the PYTHONPATH"
unset PYTHONPATH
echo "loading hadoop and spark modules"
module load spark
module load hadoop
export _JAVA_OPTIONS="-Xmx1024m -Xms256m -XX:ParallelGCThreads=1"

