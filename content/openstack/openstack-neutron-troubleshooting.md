Title: Openstack neutron troubleshooting notes
Date: 2016-08-25 06:30
Category: Openstack
Tags: Openstack, Troubleshooting
Slug: openstack-neutron-troubleshooting
Authors: Arun prasath
Summary: A bunch of troubleshooting notes for neutron troubleshooting

### Basic things to consider before starting the troubleshooting

1) Check if the network issue is for a single tenant or multiple tenant. If it is only for a single tenant, then most probably the user might be doing something wrong like messed up security group or badly configured network etc. 

2) Check if the network agents (L3 and DHCP) are working fine by giving the follwing command

```
# neutron agents-list
```

3) Identify the log locations -

Open vSwitch agent log - /var/log/neutron/openvswitch-agent.log - Available in compute node 

L3 agent log - /var/log/neutron/l3-agent.log - Available in network node where L3 agent is running, use command in previous step to check the node

DHCP agent log - /var/log/neutron/dhcp-agent.log - Available in network node where DHCP agent is running, use command in previous step to check the node

DNSMASQ logs - /var/log/messages - Available in the same node running DHCP agent

### Not able to ping the private IP or floating IP of the instance

1) Check and ensure if the ICMP ingress rule is added in any one of the security group assigned to the instance.

```
$ openstack server show 262b20a1-3b98-4ca0-b7a1-3f04f31f60bb  | grep security_groups
| security_groups                      | [{u'name': u'default'}]                                  |

$ openstack security group rule list default | grep icmp 
| e70fd066-bc29-4ab8-ba72-c4a10f3d343a | icmp        | 0.0.0.0/0 |            | None                                 |
```

2) Check from instance console if an IP address is assigned to the instance. 

```
$ openstack console log show 262b20a1-3b98-4ca0-b7a1-3f04f31f60bb

...truncated
[   17.750197] cloud-init[791]: Cloud-init v. 0.7.5 running 'init' at Tue, 16 Aug 2016 04:31:36 +0000. Up 17.57 seconds.
[   17.891523] cloud-init[791]: ci-info: +++++++++++++++++++++++++Net device info++++++++++++++++++++++++++
[   17.894429] cloud-init[791]: ci-info: +--------+------+--------------+-------------+-------------------+
[   17.899632] cloud-init[791]: ci-info: | Device |  Up  |   Address    |     Mask    |     Hw-Address    |
[   17.904601] cloud-init[791]: ci-info: +--------+------+--------------+-------------+-------------------+
[   17.910889] cloud-init[791]: ci-info: |  lo:   | True |  127.0.0.1   |  255.0.0.0  |         .         |
[   17.917099] cloud-init[791]: ci-info: | eth0:  | True | 192.168.0.20 | 255.255.0.0 | fa:16:3e:3c:75:62 |
[   17.923790] cloud-init[791]: ci-info: +--------+------+--------------+-------------+-------------------+

...
```

3) If IP address is not assigned to the instance, check if DHCP is enable for the subnet. 

Get the subnet of the instance

```
$ openstack server show 262b20a1-3b98-4ca0-b7a1-3f04f31f60bb | grep addresses

| addresses                            | private-net-01=192.168.0.20, 10.203.50.245               |

$  openstack network show private-net-01 | grep subnet

| subnets         | 9b61a815-32a0-4f18-947e-08ab512682f9 |

$  openstack subnet show 9b61a815-32a0-4f18-947e-08ab512682f9 | grep enable_dhcp

| enable_dhcp       | True                                 |

The DHCP should be enabled for the instance to get an IP, unless there are special setup to get an IP address.
```

2) Check if you are able to ping private IP of the instance from the DHCP or router namespace.	
You will be able to ping the private IP of the instance from DHCP namespace, if DHCP is enabled and from router namespace. 

To check if you can ping the private IP address -

####Checking from a DHCP namespace -

Find the network ID of the instance
```
# nova interface-list 262b20a1-3b98-4ca0-b7a1-3f04f31f60bb
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+
| Port State | Port ID                              | Net ID                               | IP addresses | MAC Addr          |
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+
| ACTIVE     | fc866e3f-83c9-4d54-82c8-27cb047b0fdf | c9da594d-1eee-45a7-805a-0575f881d266 | 192.168.0.20 | fa:16:3e:3c:75:62 |
+------------+--------------------------------------+--------------------------------------+--------------+-------------------+
```

Find the location of the DHCP agents for the network-
```
# neutron dhcp-agent-list-hosting-net c9da594d-1eee-45a7-805a-0575f881d266
+--------------------------------------+---------------------------------------------+----------------+-------+
| id                                   | host                                        | admin_state_up | alive |
+--------------------------------------+---------------------------------------------+----------------+-------+
| 399a9cc7-f8d1-4335-bf7e-38524a2459b0 | net-005.cloud.com                           | True           | :-)   |
| 89d2ebae-1eaa-454f-b7de-5ffc0ed62977 | net-003.cloud.com                           | True           | :-)   |
+--------------------------------------+---------------------------------------------+----------------+-------+
```
SSH to any one the node and execute the following command
(DHCP namespace is of format qdhcp-<NET-ID>)
```
# ssh net-005cloud.com
[root@net-005 ~]# ip netns exec qdhcp-c9da594d-1eee-45a7-805a-0575f881d266 ping 192.168.0.20
PING 192.168.0.20 (192.168.0.20) 56(84) bytes of data.
64 bytes from 192.168.0.20: icmp_seq=1 ttl=64 time=3.19 ms
64 bytes from 192.168.0.20: icmp_seq=2 ttl=64 time=0.292 ms
```

#### Checking from a router namespace

Find the router the instance is connected to. In this case the router ID is a6a6d716-df28-4eeb-9777-1bef31973b82

Find where the L3 agent for this router is hosted

```
# neutron l3-agent-list-hosting-router a6a6d716-df28-4eeb-9777-1bef31973b82
+--------------------------------------+---------------------------------------------+----------------+-------+
| id                                   | host                                        | admin_state_up | alive |
+--------------------------------------+---------------------------------------------+----------------+-------+
| 7b3bf313-07d6-43f3-b23c-015fa07844a2 | net-001.cloud.com                           | True           | :-)   |
+--------------------------------------+---------------------------------------------+----------------+-------+
```
SSH into the node and execute the following command
(Router namespace is of format qrouter-<ROUTER_ID> )

```
net-001 ~]# ip netns exec qrouter-a6a6d716-df28-4eeb-9777-1bef31973b82 ping 192.168.0.20
PING 192.168.0.20 (192.168.0.20) 56(84) bytes of data.
64 bytes from 192.168.0.20: icmp_seq=1 ttl=64 time=1.04 ms
64 bytes from 192.168.0.20: icmp_seq=2 ttl=64 time=0.208 ms

```
If you are not able to ping from any one of the namespace (DHCP or Router), check the corresponding logs. If it is some linux process level error, you will need to restart it, else a in-depth packet capture analysis is required. 






