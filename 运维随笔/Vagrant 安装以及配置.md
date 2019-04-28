Vagrant 安装以及配置（需先安装virtuabox,vagrant）

1.下载centos 7 镜像，vagrant box add ceshi 镜像名
   或者是使用先前vagrant package出来的box，进行加载镜像操作

2.vagrant init
   vagrant up
3.配置网络，修改Vagrantfile   config.vm.network "private_network", type: "dhcp" ，

  config.vm.box = "test"
4.virtualbox中关闭对应虚拟机，设置网络{网卡1：NAT转换，网卡2：host-only}

5.设置Virtualbox 中工具，对应网卡开启dhcp

6.vagrant reload 重启虚拟机，vagrant ssh （bash下）连接到服务器。

7.修改 /etc/ssh/sshd_config中，PasswordAuthentication=yes.不然无法通过ssh连接

8.ip address(centos 7中不支持ifconfig) 查看centos ip地址信息，并以ip地址+22端口远程连接ssh

