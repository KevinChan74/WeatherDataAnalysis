from gui import run_gui
from scheduler import run_scheduler
import threading

# Use Thread to ensure two python files could run simultaneously
scheduler_thread = threading.Thread(target=run_scheduler)

scheduler_thread.start()

run_gui()