import time

def timer(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"{func.__name__} : {time.time() - start_time:.3f}s")
        return result
    return wrapper