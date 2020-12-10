import multiprocessing

bind = "127.0.0.1:8000"
# workers = multiprocessing.cpu_count() * 2 + 1
# threads = multiprocessing.cpu_count() * 2 + 1
workers = multiprocessing.cpu_count()
threads = 2

print("bind", bind)
print("workers", workers)
print("threads", threads)