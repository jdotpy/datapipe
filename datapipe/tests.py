import unittest

from . import core
from . import net
from . import components as cs

import time

class CoreTest(unittest.TestCase):
    def test_basic(self):
        pipe = core.DataPipe([
           cs.NetworkProducer('net1', config={
               'protocol': 'tcp',
               'port': 5000
            }),
           cs.ConsoleConsumer('logger')
        ])
        pipe.run(block=False)

        time.sleep(2)

        c = net.TCPNetworkClient(
            host='127.0.0.1',
            port=5000
        )
        for i in range(10):
            msg = 'test ' + str(i)
            c.send(msg.encode('utf-8'))
            time.sleep(1)
        c.close()
