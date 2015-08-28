#!/bin/sh

echo "setting up cluster python environment"
echo "prepending /cluster/apps/spark/miniconda/bin to PATH"
export PATH=/cluster/apps/spark/miniconda/bin:$PATH
source activate spark_workshop
echo "removing everything from the PYTHONPATH"
unset PYTHONPATH

