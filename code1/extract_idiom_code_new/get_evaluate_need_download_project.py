import sys, ast, os, copy
import tokenize
import sys, shutil

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir + "extract_idiom_code_new/")
sys.path.append(code_dir + "transform_s_c/")

import time
import util, github_util
import subprocess
from pathos.multiprocessing import ProcessingPool as newPool
if __name__ == '__main__':
    file_path="/Users/zhangzejunzhangzejun/PycharmProjects/pythonProjectLocal/code1/extract_idiom_code_new/idiom_repo_evaluate_test_case.txt"
    evaluate_repo_list = []
    with open(file_path,"r") as file:
        content=file.readlines()
        # content = util.load_file_path(file_path)
        for e in content:
            print(e)
            if e and e!="repo_name" and e!="\n":
                evaluate_repo_list.append(e.strip())

    print("content: ",evaluate_repo_list[0])
    dir_path="/Volumes/GoogleDrive/My Drive/python_star_2000repo/"

    exist_repo_list=[]
    for e in os.listdir(dir_path):
        if e.endswith(".tar.gz"):
            exist_repo_list.append(e[:-7])
        elif e.endswith(".zip"):
            exist_repo_list.append(e[:-4])
    print("len exist_repo_list: ",len(exist_repo_list),exist_repo_list[0])
    # for
    print("need download: ",set(evaluate_repo_list)-set(exist_repo_list))
