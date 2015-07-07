# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|
  # use basic centos 6.5
  config.vm.box = "chef/centos-6.5"

  # Create a forwarded port mapping which allows access to a specific port
  # within the machine from a port on the host machine. In the example below,
  # accessing "localhost:8080" will access port 80 on the guest machine.
  # config.vm.network "forwarded_port", guest: 80, host: 8080

  # Create a private network, which allows host-only access to the machine
  # using a specific IP.
  # config.vm.network "private_network", ip: "192.168.33.10"

  # Create a public network, which generally matched to bridged network.
  # Bridged networks make the machine appear as another physical device on
  # your network.
  # config.vm.network "public_network"

  # Share an additional folder to the guest VM. The first argument is
  # the path on the host to the actual folder. The second argument is
  # the path on the guest to mount the folder. And the optional third
  # argument is a set of non-required options.
  # config.vm.synced_folder "../data", "/vagrant_data"

  # enable X11 forwarding
  config.ssh.forward_x11 = true

  # Enable provisioning with a shell script. Additional provisioners such as
  # Puppet, Chef, Ansible, Salt, and Docker are also available. Please see the
  # documentation for more information about their specific syntax and use.
  # config.vm.provision "shell", inline: <<-SHELL
  #   sudo apt-get update
  #   sudo apt-get install -y apache2
  # SHELL

  config.vm.provision "shell", inline: <<-SHELL
    echo "updating and installing linux packages"
    sudo yum -y update
    sudo yum -y install xauth
    sudo yum -y install firefox

    # install java (from http://tecadmin.net/steps-to-install-java-on-centos-5-6-or-rhel-5-6/)
    echo "installing java"
    cd /opt
    sudo wget --no-cookies --no-check-certificate --header "Cookie: gpw_e24=http%3A%2F%2Fwww.oracle.com%2F; oraclelicense=accept-securebackup-cookie" "http://download.oracle.com/otn-pub/java/jdk/7u79-b15/jdk-7u79-linux-x64.tar.gz"

    sudo tar xzf jdk-7u79-linux-x64.tar.gz
    cd jdk1.7.0_79
    sudo alternatives --install /usr/bin/java java /opt/jdk1.7.0_79/bin/java 2
    sudo alternatives --config java
    echo " " >> .bashrc
    echo "export JAVA_HOME=/opt/jdk1.7.0_79" >> .bashrc

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
      /miniconda/bin/conda update conda
      /miniconda/bin/conda install -y numpy scipy scikit-learn pip ipython ipython-notebook matplotlib
      rm Miniconda-latest-Linux-x86_64.sh
    else
      /miniconda/bin/conda update conda
      /miniconda/bin/conda install -y numpy scipy scikit-learn pip ipython ipython-notebook matplotlib
    fi

    # clean up
    echo "cleaning up"

    echo "setting PATH for miniconda..."
    echo "export PATH=/miniconda/bin:$PATH" >> .bashrc
    
    echo "setting SPARK_HOME..."
    echo "export SPARK_HOME=~/spark" >> .bashrc
    SHELL


  config.vm.hostname = "sparkws"

  config.vm.post_up_message = "VM for Spark workshop is running -- login in with 'vagrant ssh' "

  config.vm.synced_folder "./notebooks", "/home/vagrant/notebooks"
end
