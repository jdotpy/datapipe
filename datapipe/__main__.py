from quickconfig import Configuration
from core import Reactor, Receiver, Sender

def parse_receivers():
    return []

def parse_senders():
    return []

def main(config):
    receivers = parse_receivers(config('receivers'))
    senders = parse_senders(config('senders'))
    reactor = Reactor()
    reactor.run()

if __name__ == '__main__':
    config = Configuration('config.yaml', Configuration.Arg('config'))
    main(config)
