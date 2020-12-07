from cloudmesh.common.Console import Console
from cloudmesh.common.parameter import Parameter
import os

class Kuberenetes:

    scripts = {
        'all': {
            "update": textwrap.dedent(
                """ 
                sudo apt-get update && sudo apt-get upgrade
                """),
            "swap": textwrap.dedent(
                """              
                sudo dphys-swapfile swapoff
                sudo dphys-swapfile uninstall
                sudo update-rc.d dphys-swapfile remove
                sudo swapon --summary
                """),
            "cgroups": textwrap.dedent("""
                sudo echo "cgroup_enable=cpuset cgroup_memory=1 cgroup_enable=memory" >> /boot/cmdline.txt
                """),
            "reboot": "sudo reboot",
            "ip": "if a | fgrep inet | fgrep . | fgrep -v 127 | cut -d ' ' -f 2",
        }
        master:{
            "install": "curl -sfL https://get.k3s.io | sh -",
            "token": "sudo cat /var/lib/rancher/k3s/server/node-token",
            "nodes": "sudo kubectl get nodes",
        }
        worker:{

        }

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
    def oneline(script):
        """
        converts a script to one line command.
        THis is useful to run a single ssh command and pass a one line script.

        :param script:
        :return:
        """
        return " && ".join(script.strip().splitline())

    @staticmethod
    def set_master_endpoint(ip=None):
        if not ip:
            ip = Kuberenetes.do("all","ip")
        os.environ["KUBERNETES_MASTER"] = "http://{ip}:8080"
        return os.environ["KUBERNETES_MASTER"]

    @staticmethod
    def do(kind, command, host, ssh=False):
        """
        executes the script on the given host

        :param kind:
        :param command:
        :return:
        """
        script = Kuberenetes.scripts[kind][command]
        if ssh:
            script = f'ssh {host} "{script}"'
        Console.msg(script)
        # TODO: we should be using a command tt returns results so we can
        #       parse for errors Shell.live seems good option. For now we just
        #       do os.system in testing phase
        os.system(script)

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
            Kuberenetes.do("all", "update")
            Kuberenetes.do("all", "install")
            token = Kuberenetes.do("all", "token")
            ip = Kuberenetes.do("all", "ip")
            Kuberenetes.set_master_endpoint(ip=None)
            # ...
        if worker:
            Console.error("master deployment not yet implemented")
            token = Kuberenetes.do("all", "token")
            ip = Kuberenetes.do("all", "ip")

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

                Kuberenetes.do("all", "update")
                Kuberenetes.do("all", "install")
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