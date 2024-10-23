Vagrant.configure("2") do |config|
  # Specify the base image
  config.vm.box = "ubuntu/jammy64"
  config.vm.network "forwarded_port", guest: 22, host: 2202, auto_correct: false
  config.vm.provider 'virtualbox'
  # Define VM settings
  config.vm.define "monitoring-server" do |server|
    server.vm.hostname = "monitoring-server"

    # Optional: Customize VM resources
    server.vm.provider "virtualbox" do |vb|
      vb.memory = "2048"
      vb.cpus = 2
    end

    # Provision the VM with Ansible
    server.vm.provision "ansible" do |ansible|
      ansible.playbook = "playbooks/site.yml"
      ansible.inventory_path = "inventory/vagrant_inventory.yml"
      ansible.limit = "all"
      ansible.verbose = "vvv"
      ansible.extra_vars = {
        ansible_user: "vagrant"
      }
    end
  end
end
