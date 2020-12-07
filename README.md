# cloudmeesh-kubernetes


[![image](https://img.shields.io/travis/TankerHQ/cloudmesh-kubernetes.svg?branch=main)](https://travis-ci.org/TankerHQ/cloudmesn-kubernetes)

[![image](https://img.shields.io/pypi/pyversions/cloudmesh-kubernetes.svg)](https://pypi.org/project/cloudmesh-kubernetes)

[![image](https://img.shields.io/pypi/v/cloudmesh-kubernetes.svg)](https://pypi.org/project/cloudmesh-kubernetes/)

[![image](https://img.shields.io/github/license/TankerHQ/python-cloudmesh-kubernetes.svg)](https://github.com/TankerHQ/python-cloudmesh-kubernetes/blob/main/LICENSE)

see cloudmesh.cmd5

* https://github.com/cloudmesh/cloudmesh.cmd5

TEST COMMAND: k3 deploy --host=HOSTS


## Deploy a kubernetes cluster by hand

We augmented each steo with

* **All:** to indicate steps to be executed on all PIs
* **Master:** to indicate steps to be executed on the master only
* **Workers:** to indicate steps to be executed on the workers only

Do the steps 1-4 on EACH Pi (Master & Workers)

1. **All:** Update and upgrade and Disable swap (Interfers with Kubernetes)

   ```
   sudo apt-get update && sudo apt-get upgrade
   sudo dphys-swapfile swapoff
   sudo dphys-swapfile uninstall
   sudo update-rc.d dphys-swapfile remove
   sudo swapon --summary
   ```

   Double Check That Swap Was Disabled: If there is no output,
   then this has been done correctly

2. **All:** Edit `/boot/cmdline.txt`. Add this to the end of the line (put a SPACE
   after whatever exists and then add this)

   ```
   sudo echo "cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory" >> /boot/cmdline.txt
   ```

3. **All:** Reboot the Pi

   ```
   sudo reboot
   ```

4. **Master:** Next we set up kubernetes on the Master

   SSH into the master Pi and run this command and get a kubernetes token

   ```
   curl -sfL https://get.k3s.io | sh -
   sudo cat /var/lib/rancher/k3s/server/node-token
   ```

5. **Master:** Register the mater address by running this command and replacing
   `MASTER_IP_ADDRESS` with the IP address of the master Pi

   ```
   export KUBERNETES_MASTER=http://MASTER_IP_ADDRESS:8080
   ```

   Q: can we use localhost?

   Something like this may help

   ```
   ifconfig | fgrep inet | fgrep . | fgrep -v 127 | cut -d ' ' -f 2
   ```

   ifconfig may be `if a` on newe osses, please check

6. **Workers:** On each worker register the master. SSH into each of the
   worker Pi's and run this command, replacing the
   `MASTER_IP_ADDRESS` with the IP address of the master Pi and
   `NODE_TOKEN_HERE` with the node token from above

   ```
   curl -sfL https://get.k3s.io | K3S_URL=https://MASTER_IP_ADDRESS:6443 K3S_TOKEN=NODE_TOKEN_HERE sh -
   export KUBERNETES_MASTER=http://MASTER_IP_ADDRESS:8080
   ```

7. **Master:** Confirm Setup in the master

   ```
   sudo kubectl get nodes
   ```

   This will list out all the worker Pi's connected to the master Pi.
   If you have setup everything correctly, you will see the hostname of
   the master and each worker Pi listed with `Ready` status. Note, that it
   will take some time for the nodes to show up, so you need to repeat
   that command  for some time. To automatically watch it every 5 seconds
   you can use

   ```
   watch -n 5 sudo kubectl get nodes
   ```





