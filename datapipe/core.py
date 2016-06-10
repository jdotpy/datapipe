import multiprocessing
import threading
import time
import sys

def class_path(cls):
    if not hasattr('__name__'):
        cls = cls.__class__
    return cls.__module__ + '.' + cls.__name__
        
class BaseEvent():
    __slots__ = ['creator', 'timestamp', 'payload']
    
    def __init__(self, payload, creator=None):
        self.creator = creator
        self.timestamp = time.time()
        self.payload = payload

    def size(self):
        self.size = sys.getsizeof(self.payload)

    def str(self):
        if self.creator:
            return '[{}] {} - {} ({} bytes)'.format(
                class_path(self.creator),
                creator.key,
                self.timestamp,
                self.size()
            )
        else:
            return '[Anonymous] {} ({} bytes)'.format(
                self.timestamp,
                self.size()
            )


class BaseComponent():
    consumer = False
    producer = False
    Event = BaseEvent

    def __init__(self, key, config=None, target=None, event=None):
        self.key = key
        self.Event = event or self.Event
        self.options = config or {}
        self.configure(**self.options)

        if self.consumer:
            self.queue = self._create_queue()

    def _create_queue(self):
        return multiprocessing.Queue()

    def event(self, payload):
        event = self.Event(payload, creator=self)
        self.target.put(event)

    def configure(self, **options):
        pass

    def produce(self):
        raise NotImplementedError('Please override the produce method on all producers.')

    def consume(self):
        raise NotImplementedError('Please override the consume method on all consumers.')


class ComponentWorker():
    def __init__(self, components):
        self.mp = multiprocessing.get_context('fork')
        self.components = components
        self.process = None
        self.threads = None

    def run(self):
        self.process = self.mp.Process(target=self.run_component_threads)
        self.process.start()

    def _launch_thread(self, target):
        thread = threading.Thread(target=target)
        thread.start()
        self.threads.append(thread)

    def run_component_threads(self):
        if self.threads is not None:
            raise ValueError('Worker already started')
        if len(self.components) == 0:
            return 

        self.threads = []
        for component in self.components:
            if component.consumer: 
                self._launch_thread(component.consume)
            if component.producer: 
                self._launch_thread(component.produce)
        self.threads[0].join()

class DataPipe():
    def __init__(self, components=None):
        self.components = components or []
        self.resolve_pipeline()

    def resolve_pipeline(self):
        if len(self.components) == 0:
            return False
        
        next_one = None
        for component in self.components[::-1]:
            if next_one:
                component.target = next_one.queue

    def run(self, block=True):
        if len(self.components) == 0:
            return 

        self.component_worker = ComponentWorker(self.components)
        self.component_worker.run()

        if block:
            self.component_worker.process.join()
