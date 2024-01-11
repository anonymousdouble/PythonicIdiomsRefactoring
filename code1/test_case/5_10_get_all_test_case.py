
import sys, ast, os, copy
import tokenize
import sys,shutil

sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/test_case")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
from extract_simp_cmpl_data import  ast_util

import time
import format_api_call
import util, github_util,get_test_case_acc_util,configure_pro_envir_util
import replace_content_by_ast
import confiure_pro_envior_by_requirements
import subprocess
from pathos.multiprocessing import ProcessingPool as newPool
import test_case_timeout
def set_dict_class_code_list(tree, dict_class, class_name, api_list):
    if hasattr(tree, "name"):
        me_name = tree.name

        if me_name.startswith("test_") or me_name.endswith("_test"):

            me_lineno = tree.lineno
            me_id = "".join([me_name, "$", str(me_lineno)])

            if class_name not in dict_class:
                dict_class[class_name] = dict()

                dict_class[class_name][me_name] = api_list
            else:

                dict_class[class_name][me_name] = api_list

def save_repo(repo_name):
    dict_file = dict()
    for ind, file_info in enumerate(dict_repo_file_python[repo_name]):
        file_path = file_info["file_path"]
        file_name = file_path.split("/")[-1][:-3]
        map_file_name = ""
        if file_name.startswith("test_"):
            map_file_name = file_name[5:]
        elif file_name.endswith("_test"):
            map_file_name = file_name[:-8]
        else:
            continue

        if map_file_name not in dict_file:
            dict_file[map_file_name] = dict()

        # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
        #     continue
        file_html = file_info["file_html"]
        # print("file_html: ", file_html)
        # dict_file[map_file_name][file_html]=dict()
        try:
            content = util.load_file_path(file_path)
        except:
            print(f"{file_path} is not existed!")
            continue
        try:
            file_tree = ast.parse(content)
            ana_py = ast_util.Fun_Analyzer()
            ana_py.visit(file_tree)
            dict_class = dict()
            for tree, class_name in ana_py.func_def_list:
                if hasattr(tree, "name"):
                    me_name = tree.name
                    if me_name.startswith("test_") or me_name.endswith("_test"):
                        dict_file[file_html]=[class_name,me_name]
                        api_list = format_api_call.get_call(file_tree, tree)
                        set_dict_class_code_list(tree, dict_class, class_name, api_list)
            # print("dict_class: ",dict_class)
            dict_file[map_file_name][file_html] = dict_class



        except SyntaxError:
            print("the file has syntax error")
            continue
        except ValueError:
            print("the file has value error: ", content, file_html)
            continue
    util.save_pkl(save_test_methods_dir, repo_name, dict_file)
def save_all_test_cases_simplify():
    count_test_case = 0
    count_test_file = 0
    dict_test_case_inf = dict()
    for file in os.listdir(save_test_methods_dir):
        repo_name = file[:-4]
        if repo_name not in dict_test_case_inf:
            dict_test_case_inf[repo_name] = dict()
        complicate_code = util.load_pkl(save_test_methods_dir, repo_name)
        # for repo_name in complicate_code:
        for map_file_name in complicate_code:
            for file_html in complicate_code[map_file_name]:
                if file_html not in dict_test_case_inf[repo_name]:
                    dict_test_case_inf[repo_name][file_html] = []
                    count_test_file += 1
                for class_name in complicate_code[map_file_name][file_html]:
                    for me_name in complicate_code[map_file_name][file_html][class_name]:
                        if [class_name, me_name] not in dict_test_case_inf[repo_name][file_html]:
                            dict_test_case_inf[repo_name][file_html].append([class_name, me_name])
                            count_test_case += 1
    util.save_pkl(save_test_methods_dir_simplify, "all_test_case", dict_test_case_inf)
    print("count_test_case,count_test_file: ", count_test_case, count_test_file)
def get_test_case_inf():
    dict_test_case_inf=util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    count_test_case = 0
    count_test_file = 0
    repo_num=0
    for repo_name in dict_test_case_inf:
        for file_html in dict_test_case_inf[repo_name]:
            count_test_case+=len(dict_test_case_inf[repo_name][file_html])
            count_test_file+=1
            repo_num+=1
    print("count_test_case,count_test_file: ",repo_num,count_test_case,count_test_file)

if __name__ == '__main__':
    pro_dir = util.data_root + "python_star_2000repo/"
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    evaluation_testing_dir=util.data_root +"5_10_all_test_cases/evaluation/"#test_case_benchmark_dir_csv/"#
    repo_name_list=set([])
    for file in os.listdir(evaluation_testing_dir)[:1]:
        print(file)
        path=evaluation_testing_dir+file
        data=util.load_csv(path)
        for i,e in enumerate(data):
            if i==0:
                continue
            repo_name_list.add(e[0])
            # print(repo_name_list)
        # print("repo_num: ",len(repo_name_list))
        # break
    print(len(repo_name_list))
    print(len(dict_repo_file_python.keys()))
    save_test_methods_dir = util.data_root + "5_10_all_test_cases/test_cases/"
    save_test_methods_dir_simplify = util.data_root + "5_10_all_test_cases/"
    save_test_methods_dir_success = util.data_root + "5_10_all_test_cases/success_test_cases/"

    #'''
    util.mkdirs(save_test_methods_dir)
    pool = newPool(nodes=30)
    pool.map(save_repo, list(dict_repo_file_python.keys()))  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    save_all_test_cases_simplify()
    #'''
    get_test_case_inf()
    def get_test_case_success_inf(repo):
        dict_success_run_test_case = dict()
        repo_path = pro_path + repo + "/"
        for test_html in dict_test_case_inf[repo]:
            test_case_name=test_html.split("/")[-1]
            if test_case_name in test_case_timeout.time_out_test_cases_list:
                continue
            if test_html not in dict_success_run_test_case:
                dict_success_run_test_case[test_html] = []
            for cl, me in dict_test_case_inf[repo][test_html]:
                fun_list = ["::".join([cl, me]) if cl else me]
                run_test_result = configure_pro_envir_util.run_test_file(test_html, repo_path, fun_list=fun_list,
                                                                         export_python=True)
                if run_test_result == "TimeoutExpired":
                    print(">>>>>>Time out run pytest, please check ", test_html)
                    break
                # print(">>>>>>>>>>run_test_result: ", run_test_result)
                dict_me_re, flag_pass = configure_pro_envir_util.get_test_result(run_test_result)
                if flag_pass:
                    dict_success_run_test_case[test_html].append([cl, me])
                    # print("success test case: ", repo, test_html, [cl, me])
        util.save_pkl(save_test_methods_dir_success, repo, dict_success_run_test_case)
        print("save successfully! ",repo)

    test_case_name_check="test_labels.py"
    dict_test_case_inf=util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    pro_path = util.data_root + "python_star_2000repo/"
    dict_success_run_test_case=dict()
    selct_refactorings_dir = util.data_root + "5_10_all_test_cases/select/"


    # remain_repo_list=[]
    # for repo in list(repo_name_list):
    #     if os.path.exists(save_test_methods_dir_success+repo+".pkl"):
    #         dict_test_case_success = util.load_pkl(save_test_methods_dir_success, repo)
    #     else:
    #         remain_repo_list.append(repo)
    #         print("repo is not existed! ",repo)
    '''
    dict_success_run_test_case=dict()
    pool = newPool(nodes=30)
    pool.map(get_test_case_success_inf,remain_repo_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    '''
    '''
    for repo in repo_name_list:
        if repo not in dict_success_run_test_case:
            dict_success_run_test_case[repo]=dict()
        repo_path = pro_path + repo + "/"
        for test_html in dict_test_case_inf[repo]:
            if test_html not in dict_success_run_test_case[repo]:
                dict_success_run_test_case[repo][test_html]=[]
            for cl,me in dict_test_case_inf[repo][test_html]:
                fun_list = ["::".join([cl, me]) if cl else me ]
                run_test_result = configure_pro_envir_util.run_test_file(test_html, repo_path, fun_list=fun_list,
                                                                         export_python=True)
                if run_test_result == "TimeoutExpired":
                    print(">>>>>>Time out run pytest, please check ", test_html)
                    continue
                # print(">>>>>>>>>>run_test_result: ", run_test_result)
                dict_me_re, flag_pass = configure_pro_envir_util.get_test_result(run_test_result)
                if flag_pass:
                    dict_success_run_test_case[repo][test_html].append([cl,me])
                    print("success test case: ",repo,test_html,[cl,me])
                    break
            else:
                continue
            break
        else:
            continue
        break
    '''








