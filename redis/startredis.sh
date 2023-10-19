echo 1 > /proc/sys/vm/overcommit_memory
echo 'vm.overcommit_memory = 1' >> /etc/sysctl.conf

redis-server /usr/local/etc/redis/redis.conf --bind emarketredis