#!/bin/sh

echo "setting up cluster python environment"
	# install python
	if [ ! -d ~/miniconda ]; then
		cd ~
		echo "installing python"
		wget -nv https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
		chmod u+x Miniconda-latest-Linux-x86_64.sh
		./Miniconda-latest-Linux-x86_64.sh -b -p ~/miniconda
		rm Miniconda-latest-Linux-x86_64.sh
		echo "prepending ~/miniconda/bin to PATH"
		export PATH=~/miniconda/bin:$PATH
		conda update -y conda
		conda create -y -n spark_workshop numpy pip ipython jupyter matplotlib
		source activate spark_workshop
		pip install findspark
	fi
	
	echo "removing everything from the PYTHONPATH"
	unset PYTHONPATH

	export PATH=~/miniconda/bin:$PATH	
	source activate spark_workshop

