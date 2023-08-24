from mdp_worker import MajorDomoWorker

if __name__ == "__main__":
    verbose = True
    worker = MajorDomoWorker("tcp://localhost:5555", b"bruh", verbose)
    reply = None
    while True:
        request = worker.recv(reply)
        if request is None:
            break  # Worker was interrupted
        reply = request  # Echo is complex... :-)