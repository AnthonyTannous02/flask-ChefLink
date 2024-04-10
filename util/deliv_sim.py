from time import sleep
import threading
from util.context_manager import ContextManager
from flask import current_app

class DelivSim(ContextManager):
    def __init__(self, time=5, callback=None, args=None, app=None):
        self.time = time
        self.callback = callback
        self.args = args
        self.app = app
        self.thread_event = threading.Event()

    def simulate(self):
        try:
            self.thread_event.set()
            thread = threading.Thread(target=self.endTask)
            thread.start()
            print("Background task started!")
        except Exception as error:
            print(str(error))

    def endTask(self):
        from cart.mg_interface import Mongo
        if self.thread_event.is_set():
            sleep(self.time)
        try:
            self.thread_event.clear()
            if None not in [self.args]:
                with self.app.app_context():
                    mg = Mongo()
                    mg.deliver_order(self.args)
            print("Background task stopped!")
        except Exception as error:
            print(str(error))