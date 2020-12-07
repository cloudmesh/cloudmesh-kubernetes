# Cluster Network Setup
1. Connected ethernet switch to the router
2. Connected all RPi's directly to the Ethernet Network Switch
3. Enabled port forwarding to the Master Pi on port 22 for SSH experimentation

Through the master, you can SSH into any of worker nodes if necessary by simply doing
```
ssh pi@WORKER_HOSTNAME.local
```
This seems unlikely however, as you are most likely to do most of your container orchestration on the master directly