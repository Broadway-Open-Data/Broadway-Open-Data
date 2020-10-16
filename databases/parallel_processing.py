import time
import multiprocessing
from joblib import Parallel, delayed, parallel_backend




def my_function(myList):
    for x in myList:
        time.sleep(0.01)
        res = len(x)
    return res



if __name__ == "__main__":

    num_cores = multiprocessing.cpu_count()
    pool = multiprocessing.Pool(processes=num_cores)

    my_list = [str(x) for x in range(1,10)]



    # Currently isn't faster...
    
    print("With parallel")
    start = time.time()
    results = pool.map(my_function, my_list)

    #
    # with parallel_backend("loky", inner_max_num_threads=4):
    #     results = Parallel(n_jobs=4)(delayed(my_function)(x) for x in my_list)



    end = time.time()
    print(end-start)

    print("Without parallel")
    start = time.time()
    results = [my_function(x) for x in my_list]

    end = time.time()
    print(end-start)


    # processed_list = Parallel(n_jobs=num_cores)(delayed(myfunction)(i,parameters) for i in inputs)








#
