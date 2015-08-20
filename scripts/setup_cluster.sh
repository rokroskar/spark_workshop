#!/bin/sh

echo "installing miniconda python"
	# install python
	if [ ! -d ~/miniconda ]; then
		cd ~
		echo "installing python"
		wget -nv https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
		chmod u+x Miniconda-latest-Linux-x86_64.sh
		./Miniconda-latest-Linux-x86_64.sh -b -p ~/miniconda
	fi
	echo "prepending ~/miniconda/bin to PATH"
	export PATH=~/miniconda/bin:$PATH
	conda update -y conda
	conda install -y numpy pip ipython jupyter matplotlib
	rm Miniconda-latest-Linux-x86_64.sh
	pip install findspark

	conda update -y conda
	conda install -y numpy scipy scikit-learn pip ipython jupyter matplotlib
	pip install findspark
	
