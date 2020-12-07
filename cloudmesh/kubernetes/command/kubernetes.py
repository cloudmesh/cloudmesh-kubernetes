from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
import oyaml as yaml
from cloudmesh.common.Shell import Shell
import os
from cloudmesh.common.util import banner
from cloudmesh.common.parameter import Parameter
from cloudmesh.common.Host import Host
from cloudmesh.common.Printer import Printer

class KubernetesCommand(PluginCommand):

    # noinspection PyUnusedLocal
    @command
    def do_kubernetes(self, args, arguments):
        """
        ::

          Usage:
                kubernetes deploy [--workers] --host=HOSTS
                kubernetes deploy --file=FILE
                kubernetes list
                kubernetes status
                kubernetes scripts
                kubernetes run [--host=HOSTS] [KEY...]

          This command deloys kubernetes on remote hosts.

          Arguments:
              FILE   a file that contains the specification
              HOSTS  a list of hosts for deployment.
              KEY    the key to identify the script

          Options:
              -f      specify the file

          Description:
              kubernetes deploy [--workers] --host=HOSTS
                deploys kubernetes on the specified hosts. No master is used
                if the flag --workers is specified. Otherwise the fisrt host in
                the hostlist is the master. Hosts can be used with our
                parameterized format such as "red-master,red[00-03]"

              kubernetes deploy --file=FILE
                just as the deploy command, but each host is defined on each
                line in the FILE. Each line can use a parametersized
                specification.

              kubernetes scripts
                lists the available scripts

              kubernetes run [KEY...]
                executes the script with the given keys

                Example kubernetes run any test
        """


        map_parameters(arguments,
                       'file',
                       'host')

        arguments.host = Parameter.expand(arguments.host) or ["localhost"]
        hosts = arguments.host

        VERBOSE(arguments)


        from cloudmesh.kubernetes.kubernetes import Kubernetes

        if arguments.scripts:

            print(yaml.dump(Kubernetes.scripts))

        elif arguments.run:

            keys = arguments.KEY

            command = Shell.oneline(
                Kubernetes.scripts[keys[0]][keys[1]]
            )

            result = Host.ssh(hosts, command)
            # pprint (result)
            # table = Printer.write(result)
            # print(table)
            
            table = Printer.write(result, order=['host', 'success','stderr'])
            print(table)


            return ""

        elif arguments.deploy and arguments.file:

            Console.error("not implemented")
            return ""

        elif arguments.deploy:

            print (hostnames)
            # self.deploy_kubernetes(hostnames)

            Console.error("not implemented")
            return ""

        elif arguments.list:

            print(hostnames)

            Console.error("not implemented")
            return ""

        elif arguments.status:

            Console.error("not implemented")
            return ""

        return ""
