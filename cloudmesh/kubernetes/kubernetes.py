from cloudmesh.common.console import Console
from cloudmesh.common.parameter import Parameter
import textwrap
import os
from cloudmesh.common.Shell import Shell

class Kubernetes(object):

    scripts = {
        "info": "hostname && uname -a",
        "update": Shell.oneline(""" 
            sudo apt-get update 
            sudo apt-get upgrade
            """),
        "swap": Shell.oneline("""              
            sudo dphys-swapfile swapoff
            sudo dphys-swapfile uninstall
            sudo update-rc.d dphys-swapfile remove
            sudo swapon --summary
            """),
        "cgroups": Shell.oneline("""
            sudo echo "cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory" >> /boot/cmdline.txt
            """),
        "reboot": "sudo reboot",
        "ip": "if a | fgrep inet | fgrep . | fgrep -v 127 | cut -d ' ' -f 2",
        'install': "curl -sfL https://get.k3s.io | sh -",
        "master.token": "sudo cat /var/lib/rancher/k3s/server/node-token",
        "master.nodes": "sudo kubectl get nodes",
        "worker.register": 'sudo k3s agent --server https://{url}:6443 --token {key}'
    }

    # TO BE INTEGRATED
    """
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
    
    """
    @staticmethod
    def get_node_token():
        token = Kuberenetes.sudo("cat /var/lib/rancher/k3s/server/node-token")
        return token


    @staticmethod
    def set_master_endpoint(ip=None):
        if not ip:
            ip = Kuberenetes.do("ip")
        os.environ["KUBERNETES_MASTER"] = "http://{ip}:8080"
        return os.environ["KUBERNETES_MASTER"]

    @staticmethod
    def do(command, hosts, ssh=False, oneline=True, dryrun=False):
        """
        executes the script on the given host

        :param kind:
        :param command:
        :param hosts:
        :param ssh:
        :param oneline:
        :return:
        """
        script = Kuberenetes.scripts[command]
        if command in ["worker.register"]:
            url = Kubernetes.get_url()  # is this correct
            ip = Kuberenetes.do("ip")
            script = script.format(url=url, ip=ip)

        if oneline:
            script = Kuberenetes.oneline(script)

        if dryrun:
            print (script)
            result = None
        else:
            result = Host.ssh(hosts, script)

        return result

    @staticmethod
    def install(hosts, master=False, worker=False, force=False):
        """
        installs kubernetes on the given hosts. you need to set the master or
        the worker flag to indicate if it is a master or worker. If both are
        False, the first node in hosts is assumed to be the master

        :param hosts:
        :param master:
        :param worker:
        :param force:
        :return:
        """
        nodes = Parameter.expand(hosts)

        if not master and not worker:
            master = True
            worker = True
        if master:
            Console.error("master deployment not yet implemented")
            Kuberenetes.do("update")
            Kuberenetes.do("install")
            token = Kuberenetes.do("master.token")
            ip = Kuberenetes.do("ip")
            Kuberenetes.set_master_endpoint(ip=None)
            # ...
        if worker:
            Console.error("master deployment not yet implemented")
            token = Kuberenetes.do("master.token")
            ip = Kuberenetes.do("ip")

            # TODO: check may need to be different for now we just check for none

            if not token:
                Console.error("token not specified")
                raise ValueError("token not specified")

            if not ip:
                Console.error("ip not specified")
                raise ValueError("ip not specified")

            # TODO: change this to use a workerpool wwhere we cn specify
            #       how many workers install in parallel

            worker_hosts = ["TBD"]
            master_hosts = ["TBD"]
            for host in hosts:
                Console.error("TODO")
                # install on each worker
                # register on each worker

                # TODO: invert parameters, reads better
                Kuberenetes.do("update")
                Kuberenetes.do("install")
                Kuberenetes.do("swap")

            for host in master_host:
                Console.error("TODO: steps on master")
            for host in worker_hosts:
                Console.error("TODO: steps on master")

            # ...

    @staticmethod
    def uninstall(hosts):
        pass

    @staticmethod
    def status(hosts):
        pass

    @staticmethod
    def start(hosts):
        pass

    @staticmethod
    def stop(hosts):
        pass

    @staticmethod
    def update(hosts):
        pass

    #
    # classes to be integrated in the above
    # If you do not like static methods, we can use self where needed
    #

    @staticmethod
    def get_url():
        # TODO: this is not a universal command. Works only on some OS.
        ip = os.popen("hostname -I").read()
        real_ip = ""
        for letter in ip:
            if letter != " ":
                real_ip = real_ip + letter
            else:
                break
        return real_ip

    @staticmethod
    def portal():
        """
        Opens the kubernetes Web ortal in a new browser. Only works in Desktop.
        """
        url = f"http://localhost:8080"
        Shell.brwser(url)


