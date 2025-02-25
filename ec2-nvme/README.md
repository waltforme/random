### Overview

EC2 'Accelerated Computing' instances (i.e. with GPU) come with NVMe storage provisioned but not initialized.
Here is a (very dry) list of commands used to get the NVMe storage ready, on Ubuntu 24.04.

### Prerequisites

```shell
sudo apt install nvme-cli
```

### Commands as root

Looks like I have to do these after every start of the EC2 instance.
```shell
nvme list
ls -1 /dev/nvme*
hexdump -C -n 512 /dev/nvme1n1
mkfs.ext4 /dev/nvme1n1

mkdir -p /mnt/instance-store
mount /dev/nvme1n1 /mnt/instance-store

echo "/dev/nvme1n1 /mnt/instance-store ext4 defaults,nofail 0 2" | tee -a /etc/fstab

rm -r /mnt/instance-store/lost+found
chown ubuntu:ubuntu /mnt/instance-store
```

### Commands as ubuntu

```shell
mkdir /mnt/instance-store/hf
vllm serve ibm-granite/granite-3.0-2b-base --download-dir /mnt/instance-store/hf/
```

### Speed tests

```shell
dd if=/dev/zero of=/mnt/instance-store/testfile bs=1G count=5 oflag=direct
dd if=/mnt/instance-store/testfile of=/dev/null bs=1G count=5 iflag=direct
rm /mnt/instance-store/testfile
dd if=/dev/zero of=/home/ubuntu/.cache/my-testfile bs=1G count=5 oflag=direct
dd if=/home/ubuntu/.cache/my-testfile of=/dev/null bs=1G count=5 iflag=direct
rm /home/ubuntu/.cache/my-testfile
```

Or use `fio`.
```shell
fio --name=write_test --filename=/mnt/instance-store/testfile --size=5G --bs=1M --rw=write --direct=1 --numjobs=1 --iodepth=1
fio --name=read_test --filename=/mnt/instance-store/testfile --size=5G --bs=1M --rw=read --direct=1 --numjobs=1 --iodepth=1
```
