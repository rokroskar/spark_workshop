# -*- mode: ruby -*-
# vi: set ft=ruby :

#####################################
# VAGRANT FILE FOR SPARK WORKSHOP VM
#####################################

Vagrant.configure(2) do |config|
  # use basic centos 6.5
  config.vm.box = "chef/centos-6.5"

  # enable X11 forwarding
  config.ssh.forward_x11 = true

  # enable SSH key forwarding
  config.ssh.forward_agent = true

  #
  # provision necessary packages
  #

  config.vm.provision "shell", inline: <<-SHELL
    echo "updating and installing linux packages"
    sudo yum -y update
    sudo yum -y install xauth
    sudo yum -y install firefox

    # install java
    echo "installing java"
    sudo yum -y install java-1.7.0-openjdk-devel
    echo " " >> .bashrc
    echo "export JAVA_HOME=/usr/lib/jvm/java-openjdk" >> ~/.bashrc

    # install spark
    if [ ! -d spark ]; then
      echo "installing spark"
      wget -nv http://d3kbcqa49mib13.cloudfront.net/spark-1.4.0-bin-hadoop2.6.tgz
      tar -zxf spark-1.4.0-bin-hadoop2.6.tgz -C /
      ln -s /spark-1.4.0-bin-hadoop2.6 spark
      rm spark-1.4.0-bin-hadoop2.6.tgz
    else
      echo "spark already installed"
    fi

    # install python
    if [ ! -d /miniconda ]; then
      echo "installing python"
      wget -nv https://repo.continuum.io/miniconda/Miniconda-latest-Linux-x86_64.sh
      chmod u+x Miniconda-latest-Linux-x86_64.sh
      ./Miniconda-latest-Linux-x86_64.sh -b -p /miniconda
      /miniconda/bin/conda update -y conda
      /miniconda/bin/conda install -y numpy scipy scikit-learn pip ipython ipython-notebook matplotlib
      rm Miniconda-latest-Linux-x86_64.sh
    else
      /miniconda/bin/conda update -y conda
      /miniconda/bin/conda install -y numpy scipy scikit-learn pip ipython ipython-notebook matplotlib
    fi

    # clean up
    echo "cleaning up"

    echo "setting PATH for miniconda..."
    echo "export PATH=/miniconda/bin:$PATH" >> .bashrc
    
    echo "setting SPARK_HOME..."
    echo "export SPARK_HOME=~/spark" >> .bashrc
  
    # fix weird bug that causes X11 forwarding to not work properly
    dbus-uuidgen > tmp_dbus
    sudo cp tmp_dbus /var/lib/dbus/machine-id
    rm tmp_dbus

    # link to start_notebook.py
    ln -s /vagrant/start_notebook.py
  SHELL


  config.vm.hostname = "sparkws"

  config.vm.post_up_message = "VM for Spark workshop is running -- login in with 'vagrant ssh' "

  config.vm.synced_folder "./notebooks", "/home/vagrant/notebooks"

  # set up port forwarding
  config.vm.network :forwarded_port, host: 8889, guest: 8889, auto_correct: true
  config.vm.network :forwarded_port, host: 4040, guest: 4040, auto_correct: true
  config.vm.usable_port_range = 4040..4090
end
