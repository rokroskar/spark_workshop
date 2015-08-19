# -*- mode: ruby -*-
# vi: set ft=ruby :

#####################################
# VAGRANT FILE FOR SPARK WORKSHOP VM
#####################################

Vagrant.configure(2) do |config|
  config.vm.define "spark-wkshp" do |master|
    # use basic centos 6.5
    master.vm.box = "rrrrrok/centos-6.6-VBGuest4.3.28"

    # enable X11 forwarding
    master.ssh.forward_x11 = true

    # enable SSH key forwarding
    master.ssh.forward_agent = true

    # provision necessary packages
    master.vm.provision "shell", path: "scripts/provision_pyspark.sh"

    master.vm.hostname = "spark-wkshp"

    master.vm.synced_folder "./notebooks", "/home/vagrant/notebooks"
    
    # set up port forwarding
    master.vm.network :forwarded_port, host: 8889, guest: 8889, auto_correct: true
    master.vm.network :forwarded_port, host: 4040, guest: 4040, auto_correct: true
    master.vm.usable_port_range = 4040..4090

    # change the name of the VM
    config.vm.provider "virtualbox" do |v|
      v.name = master.vm.hostname.to_s
    end
  end
  config.vm.post_up_message = "VM for Spark workshop is running -- login in with 'vagrant ssh' "

end
