# import multiprocessing

bind = "127.0.0.1:8000"

workers = 2
threads = 2

timeout = 30
backlog = 2048

# worker_class = 'sync'
# worker_connections = 1000
# keepalive = 2
#
# spew = False

# workers = multiprocessing.cpu_count() * 2 + 1
# threads = multiprocessing.cpu_count() * 2
#
# print("bind", bind)
# print("workers", workers)
# print("threads", threads)