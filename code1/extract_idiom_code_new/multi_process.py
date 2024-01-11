from pathos.multiprocessing import ProcessingPool as newPool,cpu_count
import time
def f(x):
    print("x: ",x)
    while 1:
        time.sleep(10)
        break
    return x**2

if __name__ == '__main__':
    print("come here")
    repo_list=[i for i in range(100)]
    print("cpu_count: ",cpu_count())
    pool = newPool(cpu_count())
    pool.map(f, repo_list)
    pool.close()
    pool.join()
    # pool = newPool(nodes=3)
    # pool.map(f, repo_list)  # [:3]sample_repo_url ,token_num_list[:1]
    # pool.close()
    # print("end")
