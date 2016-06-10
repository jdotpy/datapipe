import multiprocessing
import threading
import time

class BaseComponent():
    consumer = False
    producer = True
    targets = ['run']

    def __init__(self, key, config=None):
        self.key = key
        self.config = config or {}

    def run(self):
        pass

class BaseEvent():
    pass

class ComponentWorker():
    def __init__(self, components):
        self.mp = multiprocessing.get_context('fork')
        self.components = components
        self.process = None

    def run(self):
        self.process = self.mp.Process(target=self.run_component_threads)
        self.process.start()

    def run_component_threads(self):
        threads = []
        for component in self.components:
            for target_name in component.targets:
                target = getattr(component, target_name, None)
                if target is not None:
                    thread = threading.Thread(target=target)
                    thread.start()
                    threads.append(thread)
        threads[0].join()

class DataPipe():
    def __init__(self, components=None):
        self.components = components or []

    def run(self):
        self.component_worker = ComponentWorker(self.components)
        self.component_worker.run()
        self.component_worker.process.join()
