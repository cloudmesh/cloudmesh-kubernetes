# Do the following on EACH Pi (Master & Workers)
### Update and upgrade
```
sudo apt-get update && sudo apt-get upgrade
```

### Disable swap (Interfers with Kubernetes)
```
sudo dphys-swapfile swapoff \
&& sudo dphys-swapfile uninstall \
&& sudo update-rc.d dphys-swapfile remove
```

### Double Check That Swap Was Disabled:
```
sudo swapon --summary
```
If there is no output, then this has been done correctly

### Edit /boot/cmdline.txt:

```
sudo nano /boot/cmdline.txt
```
Add this to the end of the line (put a SPACE after whatever exists and then add this)
```
cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory
```

Reboot the Pi
```
sudo reboot
```
Repeat until the above commands have been run on each Pi, master and worker alike

# Specific Master Pi Setup Instructions
SSH into the master Pi and run this command
```
curl -sfL https://get.k3s.io | sh -
```

Now get the node token
```
sudo cat /var/lib/rancher/k3s/server/node-token
```

Finally, run this command, replacing `MASTER_IP_ADDRESS` with the IP address of the master Pi
```
export KUBERNETES_MASTER=http://MASTER_IP_ADDRESS:8080
```

You can now disconnect from the master node
# Specific Worker Pi Setup Instructions
SSH into each of the worker Pi's and run this command, replacing the `MASTER_IP_ADDRESS` with the IP address of the master Pi and `NODE_TOKEN_HERE` with the node token from above
```
curl -sfL https://get.k3s.io | K3S_URL=https://MASTER_IP_ADDRESS:6443 K3S_TOKEN=NODE_TOKEN_HERE sh -
```

Then, run this command, replacing `MASTER_IP_ADDRESS` with the IP address of the master Pi
```
export KUBERNETES_MASTER=http://MASTER_IP_ADDRESS:8080
```

Repeat this on each of your worker nodes

# Confirm Setup
Login to the master Pi again, and run this command
```
sudo kubectl get nodes
```
This will list out all the worker Pi's connected to the master Pi. If you have setup everything correctly, you will see the hostname of the master and each worker Pi listed with `Ready` status
