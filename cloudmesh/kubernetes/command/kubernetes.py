from cloudmesh.shell.command import command
from cloudmesh.shell.command import PluginCommand
from cloudmesh.common.console import Console
from pprint import pprint
from cloudmesh.common.debug import VERBOSE
from cloudmesh.shell.command import map_parameters
import oyaml as yaml


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

        VERBOSE(arguments)

        map_parameters(arguments,
                       'file',
                       'host')

        from cloudmesh.kubernetes.kubernetes import Kubernetes

        if arguments.scripts:

            pprint(Kubernetes.scripts)
            print(yaml.dump(Kubernetes.scripts))

        elif arguments.deploy and arguments.file:

            Console.error("not implemented")
            return ""

        elif arguments.deploy:

            hostnames = arguments['--host']
            hostnames = Parameter.expand(hostnames)
            self.deploy_kubernetes(hostnames)

            Console.error("not implemented")
            return ""

        elif arguments.list:

            Console.error("not implemented")
            return ""

        elif arguments.status:

            Console.error("not implemented")
            return ""

        Console.error("Command options wrong")
        return ""
