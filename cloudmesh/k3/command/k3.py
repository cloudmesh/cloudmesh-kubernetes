from __future__ import print_function
from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.k3.api.manager import Manager
from cloudmesh.common.console import Console
from cloudmesh.common.util import path_expand
from pprint import pprintd9
from cloudmesh.common.debug import VERBOSE
import os

class K3Command(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_k3(self, args, arguments):
        """
        ::

          Usage:
                k3 deploy [--workers] --host=HOSTS
                k3 deploy --file=FILE
                k3 list
                k3 status

          This command deloys kubernetes on remote hosts.

          Arguments:
              FILE   a file that contains the specification
              HOSTS  a list of hosts for deployment.

          Options:
              -f      specify the file

          Description:
              k3 deploy [--workers] --host=HOSTS
                deploys kubernetes on the specified hosts. No master is used
                if the flag --workers is specified. Otherwise the fisrt host in
                the hostlist is the master. Hosts can be used with our
                parameterized format such as "red-master,red[00-03]"

              k3 deploy --file=FILE
                 just as the deploy command, but each host is defined on each
                 line in the FILE. Each line can use a parametersized
                 specification.
        """
        arguments.FILE = arguments['--file'] or None

        VERBOSE(arguments)

        m = Manager()

        if arguments.FILE:
            print("option a")
            m.list(path_expand(arguments.FILE))

        elif arguments['deploy']:
                if arguments['--host']:
                        hostnames = arguments['--host']
                        hostnames = Parameter.expand(hostnames) 
                        self.deploy_kubernetes(hostnames) 

        elif arguments.list:
            print("option b")
            m.list("just calling list without parameter")

        Console.error("This is just a sample")
        return ""
    
    def deploy_kubernetes(self, hosts):
        self.upgrade(hosts)
        deploy_main()
        self.install_kubernetes(hosts)
    
    def deploy_main():
        os.system("curl -sfL https://get.k3s.io | sh -")
    
    def get_url():
        ip = os.popen("hostname -I").read()
        realIP = ""
        for letter in ip:
            if(letter!= " "):
                realIP = realIP + letter
            else:
                break
        return(realIP)


    def get_key():
        key = os.popen("sudo cat /var/lib/rancher/k3s/server/node-token").read() 
        return(key)

    def upgrade(self, hosts):
        command = "sudo apt-get update && sudo apt-get upgrade"
        self.exec_on_remote_hosts(self, hosts, command)

    def swap(self, hosts):
        command = "sudo dphys-swapfile swapoff \
            && sudo dphys-swapfile uninstall \
                && sudo update-rc.d dphys-swapfile remove"
        self.exec_on_remote_hosts(self, hosts, command)

    def editBoot(self, hosts):
        #Need to figure out how to edit the boot file with a command
        #Also reboot
        pass

    def install_kubernetes_on_master(self,hosts):
        command = 'curl -sfL https://get.k3s.io | sh -'
        self.exec_on_remote_hosts()#need to make this only on master
        get_key()
        export KUBERNETES_MASTER="http://{MASTER_IP_ADDRESS}:8080".format(get_url())
        #Incomplete




    def install_kubernetes_on_worker(self, hosts):
        url = get_url()
        key = get_key()
        command = 'sudo k3s agent --server https://{K3S_URL}:6443 --token {K3S_TOKEN}'.format(url, key)
        self.exec_on_remote_hosts(self, hosts, command)
        #Incomplete

    def exec_on_remote_hosts(self, hosts, command):
         result = Host.ssh(hosts, command)
         print(result[0]['stdout'])
