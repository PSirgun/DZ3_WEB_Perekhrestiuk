from multiprocessing import cpu_count, Process, Queue
import concurrent.futures
from time import time

def timer_decor(func, print_result = True):
    def inner(*args):
        start_time = time()
        result = func(*args)
        timer = time() - start_time
        if print_result:
            return timer, result
        return timer
    return inner

def factorize(number, q = None):
    intermed_list = []
    for i in range(1, number + 1):
        if number % i == 0:
            intermed_list.append(i)
    if q:
        q.put(intermed_list)
        return q
    return intermed_list

@timer_decor
def factorize_singleproc(*numbers):
    result_list = []
    for num in numbers:
        result_list.append(factorize(num))
    return result_list

@timer_decor   
def factorize_multiproc(*numbers):
    result_list = []
    processes = []
    q = Queue()

    for num in numbers:
        process = Process(target=factorize, args=(num, q))
        process.start()
        processes.append(process)

    [el.join() for el in processes]

    while not q.empty():
        result_list.append(q.get())

    return result_list

@timer_decor
def factorize_executor(numbers):
    res = []
    with concurrent.futures.ProcessPoolExecutor(4) as executor:
        for prime in executor.map(factorize, numbers):
            res.append(prime)
    return res

if __name__ == '__main__':
    
    numbers = [12345678, 12345678, 12345678, 12345678]

    print (f'SINGELPROC {factorize_singleproc(*numbers)}')
    print (f'MULTIPROC {factorize_multiproc(*numbers)}') 
    print (f'EXECUTOR {factorize_executor(numbers)}')
    
  
#перевіркa правильності роботи алгоритму самої функції 


    def factorize(*numbers):
        start_time = time()
        result_list = []
        for num in numbers:
            intermed_result = []
            for i in range(1, num + 1):
                if num % i == 0:
                    intermed_result.append(i)
            result_list.append(intermed_result)
        timer = time() - start_time
        print (timer)
        return result_list

    a, b, c, d  = factorize(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]