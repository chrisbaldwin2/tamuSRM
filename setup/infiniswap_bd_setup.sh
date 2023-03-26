modprobe infiniswap 
mount -t configfs none /sys/kernel/config

nbdxadm -o create_host -i 0 -p $PWD/portal.list #portal.list
nbdxadm -o create_device -i 0 -d 0

ls /dev/sda4
mkswap /dev/sda4
swapon /dev/sda4

