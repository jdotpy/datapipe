import unittest

from . import core
from . import components as cs

class CoreTest(unittest.TestCase):
    def test_basic(self):
        pipe = core.DataPipe([
           cs.NetworkProducer('net1', config={
               'protocol': 'tcp',
               'port': 5000
            }),
           cs.ConsoleConsumer('logger')
        ])
        pipe.run()
