# -*- mode: ruby -*-
# vi: set ft=ruby :

#####################################
# VAGRANT FILE FOR SPARK WORKSHOP VM
#####################################

Vagrant.configure(2) do |config|
  # use basic centos 6.5
  config.vm.box = "chef/centos-6.6"

  # enable X11 forwarding
  config.ssh.forward_x11 = true

  # enable SSH key forwarding
  config.ssh.forward_agent = true

  
  # provision necessary packages
  config.vm.provision "shell", path: "provision_pyspark.sh"

  config.vm.hostname = "sparkws"

  config.vm.post_up_message = "VM for Spark workshop is running -- login in with 'vagrant ssh' "

  config.vm.synced_folder "./notebooks", "/home/vagrant/notebooks"

  # set up port forwarding
  config.vm.network :forwarded_port, host: 8889, guest: 8889, auto_correct: true
  config.vm.network :forwarded_port, host: 4040, guest: 4040, auto_correct: true
  config.vm.usable_port_range = 4040..4090
end
