Title: Deploy a MariaDB high available cluster using Ansible
Date: 2016-05-05 11:22
Category: Openstack
Tags: Ansible, Automation, Database, High availability
Slug: mariadb-ha-galera-ansible
Authors: Arun prasath
Summary: This is a write up explaining setting up a MariaDB cluster using Ansible in Ubuntu 12.04 / Ubuntu 14.04.

#Requirements
Ansible version 1.9.2 (Not tested in other versions yet)

n number of target machines (Ubuntu 12.04 / Ubuntu 14.04) for deploying MariaDB cluster

Here I am using 5 Ubuntu 14.04 VMs in an Openstack environment.

#Deploying MariaDB
From the build server clone the repository.
```
# git clone https://github.com/bingoarun/ansible-mariadb-galera-web.git
# cd ansible-mariadb-galera-web
```
Edit the inventory to include the server details and set the password.
```
# cat inventory 
[database]
192.168.1.48 ansible_ssh_user=cloud-user
192.168.1.49 ansible_ssh_user=cloud-user
192.168.1.50 ansible_ssh_user=cloud-user
192.168.1.51 ansible_ssh_user=cloud-user
192.168.1.52 ansible_ssh_user=cloud-user

[database:vars]
root_password=TomAndJerry
debian_sys_maint_password=TomAndJerry
```
Ensure that you are able to ping the VMs.
```
# ansible database -m ping -i inventory 
192.168.1.48 | success >> {
    "changed": false,
    "ping": "pong"
}

192.168.1.49 | success >> {
    "changed": false,
    "ping": "pong"
}

192.168.1.50 | success >> {
    "changed": false,
    "ping": "pong"
}

192.168.1.52 | success >> {
    "changed": false,
    "ping": "pong"
}

192.168.1.51 | success >> {
    "changed": false,
    "ping": "pong"
}
```
Now run the site.yml as below
```
# ansible-playbook site.yml -i inventory -become

PLAY [database] *************************************************************** 

GATHERING FACTS *************************************************************** 
ok: [192.168.1.52]
ok: [192.168.1.51]
ok: [192.168.1.48]
ok: [192.168.1.49]

<TRUNCATED>

TASK: [mariadb | Restart mysql on first node] ********************************* 
skipping: [192.168.1.49]
skipping: [192.168.1.50]
skipping: [192.168.1.51]
skipping: [192.168.1.52]
changed: [192.168.1.48]

PLAY RECAP ******************************************************************** 
192.168.1.48               : ok=19   changed=13   unreachable=0    failed=0   
192.168.1.49               : ok=18   changed=12   unreachable=0    failed=0   
192.168.1.50               : ok=18   changed=12   unreachable=0    failed=0   
192.168.1.51               : ok=18   changed=12   unreachable=0    failed=0   
192.168.1.52               : ok=18   changed=12   unreachable=0    failed=0 
```
This should get the MariaDB cluster up and running in master-master mode.
