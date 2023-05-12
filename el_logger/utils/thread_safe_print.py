from threading import Lock

print_lock = Lock()


# Quick and dirty implementation of a lock on the console, so that multithreaded print are not interleaving
# In real life situations the logger should acquire a lock/mutex on the resource
def sync_print(message):
    with print_lock:
        print(message)
