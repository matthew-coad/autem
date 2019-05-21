from .runner import Runner
from .run_query import RunQuery
from .run_state import RunState

import time
import msvcrt

from multiprocessing import Process, Queue, current_process, freeze_support

def run_worker(input):
    simulation = input.get()
    simulation._run_internal()

class LocalRunner(Runner):
    """
    Run the simulation in a seperate process on the local machine.

    Some sklearn algorithms seem to leak resources so this runner is useful when running a large number 
    of jobs. It ensure that all resources are cleaned up with the simulation completes.
    """

    def __init__(self, simulation, max_time = None):
        Runner.__init__(self, simulation, max_time)

    def should_terminate(self, process):
        if msvcrt.kbhit() and msvcrt.getch() == chr(27).encode():
            RunState.get(self.get_simulation()).escaped = True
            self.get_feedback().report("Esc - aborting simulation")
            return True

        if not process.is_alive():
            self.get_feedback().report("Simulation complete")
            return True

        if RunQuery(self.get_simulation()).is_timedout():
            self.get_feedback().report("Simulation timedout")
            return True

        return False

    def _run_internal(self):

        # Create a task queue
        task_queue = Queue()
        task_queue.put(self.get_simulation())

        # Start worker
        process = Process(target=run_worker, args=(task_queue,))
        process.start()

        while not self.should_terminate(process):
            time.sleep(.1)

        if process.is_alive():
            process.terminate()
        process.join()
