
import sys, ast, os, copy
import tokenize
import sys,shutil

sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/test_case")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time
import util, github_util,get_test_case_acc_util,configure_pro_envir_util
import replace_content_by_ast,random
import confiure_pro_envior_by_requirements
import subprocess
from pathos.multiprocessing import ProcessingPool as newPool
import test_case_timeout
def count_acc(dict_success_run_test_case):
    acc_count = 0
    total_count = 0
    for e in dict_success_run_test_case:
        acc_count += e[-2]
        total_count += 1
    print("refactoring result: ", total_count, acc_count)
    return total_count,acc_count
def get_code_map_test_case_info(dict_code_map_pass_test_case_code_dir):
    total_test_cases=0
    code_count=0
    for file_name in os.listdir(dict_code_map_pass_test_case_code_dir):

        repo_name=file_name[:-4]
        dict_code_map_pass_test_case = util.load_pkl(dict_code_map_pass_test_case_code_dir, repo_name)
        for file_html in dict_code_map_pass_test_case:
            for code_cl in dict_code_map_pass_test_case[file_html]:
                for code_me in dict_code_map_pass_test_case[file_html][code_cl]:
                    for code_node in dict_code_map_pass_test_case[file_html][code_cl][code_me]:
                        if repo_name=="sympy":
                            print("file_html: ",file_html,dict_code_map_pass_test_case[file_html][code_cl][code_me][code_node])
                        code_count+=1
                        total_test_cases+=len(dict_code_map_pass_test_case[file_html][code_cl][code_me][code_node])
    print("total map test_cases: ",total_test_cases,code_count)
