###############################################################
# pytest -v --capture=no tests/test_example.py
# pytest -v  tests/test_example.py
# pytest -v --capture=no  tests/test_example.py::TestExample::<METHODNAME>
###############################################################
import pytest
from cloudmesh.common.Benchmark import Benchmark
from cloudmesh.common.Shell import Shell
from cloudmesh.common.debug import VERBOSE
from cloudmesh.common.util import HEADING

Benchmark.debug()

cloud = "local"


@pytest.mark.incremental
class TestExample:

    def test_help(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_vm(self):
        HEADING()
        Benchmark.Start()
        result = Shell.execute("cms help vm", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "['sample1', 'sample2', 'sample3', 'sample18']" in result

    def test_help_again(self):
        HEADING()

        Benchmark.Start()
        result = Shell.execute("cms help", shell=True)
        Benchmark.Stop()
        VERBOSE(result)

        assert "quit" in result
        assert "clear" in result

    def test_benchmark(self):
        HEADING()
        Benchmark.print(csv=True, tag=cloud)
