
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
def selct_500_refactorings():
    code_info_dir = util.data_root + "5_10_all_test_cases/code_info_3215/"
    repo_name_list = set([])
    totoal_code = 0
    dict_total_code = []
    for file in os.listdir(code_info_dir):
        if "config" in file:
            continue
        for repo in os.listdir(code_info_dir + file + "/"):
            repo_name = repo[:-4]
            if repo_name == "sympy":
                continue
            repo_name_list.add(repo_name)

            dict_test_case_inf = util.load_pkl(code_info_dir + file + "/", repo_name)
            for file_html in dict_test_case_inf:
                for cl in dict_test_case_inf[file_html]:
                    for me in dict_test_case_inf[file_html][cl]:
                        for code in dict_test_case_inf[file_html][cl][me]:
                            dict_total_code.append([repo_name, file, file_html, cl, me, code])
                            totoal_code += 1
    print("without config: ", len(repo_name_list), totoal_code, len(dict_total_code))
    repo_name_list = list(repo_name_list)
    random.seed(2022)
    random.shuffle(repo_name_list)
    random.shuffle(dict_total_code)
    dict_repo_map_num = dict()
    dict_file_map_num=dict()
    for repo_name, file, file_html, cl, me, code in dict_total_code[:200]:
        if file not in dict_file_map_num:
            dict_file_map_num[file] = 0
        dict_file_map_num[file] += 1
        if repo_name not in dict_repo_map_num:
            dict_repo_map_num[repo_name] = 0
        dict_repo_map_num[repo_name] += 1
    print("random 500: ", dict_file_map_num, "\n", len(dict_repo_map_num.keys()))
    dict_test_case_inf = util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    count_test_case = 0
    count_test_file = 0
    repo_num = 0
    # dict_repo_num[e[0]]
    dict_repo_map_test_case = dict()
    for repo_name in dict_repo_map_num:
        dict_repo_map_test_case[repo_name] = 0
        repo_num += 1
        for file_html in dict_test_case_inf[repo_name]:
            count_test_case += len(dict_test_case_inf[repo_name][file_html])
            count_test_file += 1
            dict_repo_map_test_case[repo_name] += len(dict_test_case_inf[repo_name][file_html])
    print("count_test_case,count_test_file: ", repo_num, count_test_case, count_test_file)
    total_test_cases = 0
    for repo in dict_repo_map_test_case:
        total_test_cases += dict_repo_num[repo] * dict_repo_map_test_case[repo]
    print("total_test_cases: ", total_test_cases)
    pass
def selct_20_each_kind_refactorings():
    code_info_dir = util.data_root + "5_10_all_test_cases/code_info_3215/"
    repo_name_list = set([])
    totoal_code = 0
    dict_total_code = []
    dict_file_map_code = dict()
    dict_file_map_code_selct=dict()
    for file in os.listdir(code_info_dir):
        if "config" in file:
            continue
        for repo in os.listdir(code_info_dir + file + "/"):
            repo_name = repo[:-4]
            if repo_name == "sympy":
                continue
            repo_name_list.add(repo_name)
            if file not in dict_file_map_code:
                dict_file_map_code[file]=[]
            dict_test_case_inf = util.load_pkl(code_info_dir + file + "/", repo_name)
            for file_html in dict_test_case_inf:
                for cl in dict_test_case_inf[file_html]:
                    for me in dict_test_case_inf[file_html][cl]:
                        for code in dict_test_case_inf[file_html][cl][me]:
                            dict_total_code.append([repo_name, file, file_html, cl, me, code])
                            totoal_code += 1
                            dict_file_map_code[file].append([repo_name, file, file_html, cl, me, code])

    print("without config: ", len(repo_name_list), totoal_code, len(dict_total_code))
    repo_name_list = set([])#list(repo_name_list)
    random.seed(2019)#2019 110984
    threshold=20
    dict_repo_num=dict()
    for key in dict_file_map_code:
        # print(">>>>>>>>>>>>>>>>>",key)
        print(dict_file_map_code[key][0])
        random.shuffle(dict_file_map_code[key])
        print(dict_file_map_code[key][0])
        dict_file_map_code[key]=dict_file_map_code[key]
        dict_file_map_code_selct[key]=dict_file_map_code[key][:threshold]
        # print(key,": ",dict_file_map_code[key][0])
        # print(">>>>>>>>>>>>>>>>>", key)
        print("len: ",len(dict_file_map_code[key][:threshold]))
        for e in dict_file_map_code[key][:threshold]:
            repo_name=e[0]
            repo_name_list.add(repo_name)
            if repo_name not in dict_repo_num:
                dict_repo_num[repo_name]=0
            # else:
            dict_repo_num[repo_name] += 1
    print("dict_repo_num: ", dict_repo_num)
    repo_name_list = list(repo_name_list)
    dict_test_case_inf = util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    count_test_case = 0
    count_test_file = 0
    repo_num = 0

    dict_repo_map_test_case = dict()
    for repo_name in repo_name_list:
        dict_repo_map_test_case[repo_name] = 0
        repo_num += 1
        for file_html in dict_test_case_inf[repo_name]:
            # print("come here")
            count_test_case += len(dict_test_case_inf[repo_name][file_html])
            count_test_file += 1
            dict_repo_map_test_case[repo_name] += len(dict_test_case_inf[repo_name][file_html])
        # else:
        #     print("dont cover")
    print("count_test_case,count_test_file: ", repo_num, count_test_case, count_test_file)

    total_test_cases = 0
    for repo in repo_name_list:
        total_test_cases += dict_repo_num[repo] * dict_repo_map_test_case[repo]
    print("total_test_cases: ", total_test_cases)
    util.save_pkl(selct_refactorings_dir, "selct_code_info_2", dict_file_map_code_selct)


def selct_50_repos():
    code_info_dir = util.data_root + "5_10_all_test_cases/code_info_3215/"
    repo_name_list = set([])
    totoal_code = 0
    dict_total_code = []
    for file in os.listdir(code_info_dir):
        if "config" in file:
            continue
        for repo in os.listdir(code_info_dir + file + "/"):
            repo_name = repo[:-4]
            if repo_name == "sympy":
                continue
            repo_name_list.add(repo_name)

            dict_test_case_inf = util.load_pkl(code_info_dir + file + "/", repo_name)
            for file_html in dict_test_case_inf:
                for cl in dict_test_case_inf[file_html]:
                    for me in dict_test_case_inf[file_html][cl]:
                        for code in dict_test_case_inf[file_html][cl][me]:
                            dict_total_code.append([repo_name, file, file_html, cl, me, code])
                            totoal_code += 1
    print("without config: ", len(repo_name_list), totoal_code, len(dict_total_code))
    repo_name_list = list(repo_name_list)
    random.seed(2022)
    random.shuffle(repo_name_list)
    # print("random repo_name_list: ", repo_name_list[:50])
    dict_test_case_inf = util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    count_test_case = 0
    count_test_file = 0
    repo_num = 0

    dict_repo_map_test_case = dict()
    for repo_name in repo_name_list[:50]:
        dict_repo_map_test_case[repo_name] = 0
        repo_num += 1
        for file_html in dict_test_case_inf[repo_name]:
            count_test_case += len(dict_test_case_inf[repo_name][file_html])
            count_test_file += 1
            dict_repo_map_test_case[repo_name] += len(dict_test_case_inf[repo_name][file_html])
    print("count_test_case,count_test_file: ", repo_num, count_test_case, count_test_file)

    total_test_cases = 0
    for repo in repo_name_list[:50]:
        total_test_cases += dict_repo_num[repo] * dict_repo_map_test_case[repo]
    print("total_test_cases: ", total_test_cases)
    dict_file_map_num = dict()
    for repo_name, file, file_html, cl, me, code in dict_total_code:
        if repo_name in repo_name_list[:50]:
            if file not in dict_file_map_num:
                dict_file_map_num[file]=0
            dict_file_map_num[file]+=1

    print("total_test_cases: ", dict_file_map_num)

def selct_top_50_repos():
    code_info_dir = util.data_root + "5_10_all_test_cases/code_info_3215/"
    repo_name_list = set([])
    totoal_code = 0
    dict_total_code = []
    dict_repo_num_kind=dict()
    for file in os.listdir(code_info_dir):
        if "config" in file:
            continue


        for repo in os.listdir(code_info_dir + file + "/"):
            repo_name = repo[:-4]

            if repo_name == "sympy":
                continue
            if repo_name not in dict_repo_num_kind:
                dict_repo_num_kind[repo_name]=set([])
            dict_repo_num_kind[repo_name].add(file)
            repo_name_list.add(repo_name)

            dict_test_case_inf = util.load_pkl(code_info_dir + file + "/", repo_name)
            for file_html in dict_test_case_inf:
                for cl in dict_test_case_inf[file_html]:
                    for me in dict_test_case_inf[file_html][cl]:
                        for code in dict_test_case_inf[file_html][cl][me]:
                            dict_total_code.append([repo_name, file, file_html, cl, me, code])
                            totoal_code += 1
    dict_repo_list=sorted(dict_repo_num_kind, key=lambda k: len(dict_repo_num_kind[k]), reverse=True)
    dict_repo_num_kind = [ {item:list(dict_repo_num_kind[item])} for item in dict_repo_list]
    print(dict_repo_num_kind)
    #'''
    refactor=0
    dict_kind_num=dict()
    for e in dict_repo_num_kind[:10]:
        for key in e:
            if e not in dict_kind_num:
                dict_kind_num[key]=0
            dict_kind_num[key]+=1
    # print(dict_kind_num)

    repo_name_list=[ key for e in dict_repo_num_kind[:30] for key in e]
    print(len(repo_name_list),repo_name_list[0])

    print("without config: ", len(repo_name_list), totoal_code, len(dict_total_code))
    # repo_name_list = list(repo_name_list)
    # random.seed(2022)
    # random.shuffle(repo_name_list)
    # print("random repo_name_list: ", repo_name_list[:50])
    dict_test_case_inf = util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    count_test_case = 0
    count_test_file = 0
    repo_num = 0

    dict_repo_map_test_case = dict()
    for repo_name in repo_name_list:
        dict_repo_map_test_case[repo_name] = 0
        repo_num += 1
        for file_html in dict_test_case_inf[repo_name]:
            count_test_case += len(dict_test_case_inf[repo_name][file_html])
            count_test_file += 1
            dict_repo_map_test_case[repo_name] += len(dict_test_case_inf[repo_name][file_html])
    print("count_test_case,count_test_file: ", repo_num, count_test_case, count_test_file)

    total_test_cases = 0
    for repo in repo_name_list:
        total_test_cases += dict_repo_num[repo] * dict_repo_map_test_case[repo]
    print("total_test_cases: ", total_test_cases)
    dict_file_map_num = dict()
    for repo_name, file, file_html, cl, me, code in dict_total_code:
        if repo_name in repo_name_list[:50]:
            if file not in dict_file_map_num:
                dict_file_map_num[file]=0
            dict_file_map_num[file]+=1

    print("total_test_cases: ", dict_file_map_num/3600/24)
    #'''

if __name__ == '__main__':
    save_test_methods_dir_simplify = util.data_root + "5_10_all_test_cases/"
    evaluation_testing_dir = util.data_root + "5_10_all_test_cases/evaluation/"  # test_case_benchmark_dir_csv/"#
    repo_name_list = set([])
    dict_repo_num=dict()
    totoal_code=0
    for file in os.listdir(evaluation_testing_dir)[:]:
        print(file)
        path = evaluation_testing_dir + file
        data = util.load_csv(path)
        for i, e in enumerate(data):
            if i == 0:
                continue
            repo_name_list.add(e[0])
            if e[0] not in dict_repo_num:
                dict_repo_num[e[0]]=0
            dict_repo_num[e[0]]+=1
            totoal_code+=1
            # print(repo_name_list)
        # print("repo_num: ",len(repo_name_list))
        # break
    print(len(repo_name_list),totoal_code)
    # selct_500_refactorings()
    # print("-------------------------------")
    # selct_50_repos()
    # print("-------------------------------")
    selct_refactorings_dir=util.data_root + "5_10_all_test_cases/select/"
    selct_20_each_kind_refactorings()
    dict_test_case_inf = util.load_pkl(selct_refactorings_dir, "selct_code_info")
    # dict_test_case_inf = util.load_pkl(selct_refactorings_dir, "selct_code_info_2")
    total_repo_list=set([])
    for key in dict_test_case_inf:
        if "compr" in key:
            continue
        dict_key_num=dict()
        repo_list=set([])
        count=0
        for repo_name, file, file_html, cl, me, code in dict_test_case_inf[key][:]:

            if repo_name in total_repo_list:
                continue
            if "target" not in key and "truth" not in key:

                if count==3:
                    break
            if repo_name not in dict_key_num:
                dict_key_num[repo_name]=[]
            dict_key_num[repo_name].append([file_html, cl, me, code])
            repo_list.add(repo_name)
            total_repo_list.add(repo_name)
            count+=1
        print("len: ",key,len(repo_list),count,dict_key_num)
        util.save_pkl(selct_refactorings_dir+"selct_code_info_3/", key, dict_key_num)

    print("num: ",len(total_repo_list))


    remain_repo_list = []
    save_test_methods_dir_success = util.data_root + "5_10_all_test_cases/success_test_cases/"
    '''
    for repo in list(total_repo_list):
        if os.path.exists(save_test_methods_dir_success + repo + ".pkl"):
            dict_test_case_success = util.load_pkl(save_test_methods_dir_success, repo)
        else:
            remain_repo_list.append(repo)
            print("repo is not existed! ", repo)
        # util.save_pkl(selct_refactorings_dir+"all_kinds/",key,dict_key_num)
    '''

    # selct_top_50_repos()
    '''
    code_info_dir=util.data_root + "5_10_all_test_cases/code_info_3215/"
    repo_name_list = set([])
    totoal_code=0
    dict_total_code=[]
    for file in os.listdir(code_info_dir):
        if "config" in file:
            continue
        for repo in os.listdir(code_info_dir+file+"/"):
            repo_name=repo[:-4]
            if repo_name=="sympy":
                continue
            repo_name_list.add(repo_name)

            dict_test_case_inf = util.load_pkl(code_info_dir+file+"/", repo_name)
            for file_html in dict_test_case_inf:
                for cl in dict_test_case_inf[file_html]:
                    for me in dict_test_case_inf[file_html][cl]:
                        for code in dict_test_case_inf[file_html][cl][me]:
                            dict_total_code.append([repo_name,file,file_html,cl,me,code])
                            totoal_code+=1
    print("without config: ",len(repo_name_list), totoal_code,len(dict_total_code))
    repo_name_list=list(repo_name_list)
    random.seed(2022)
    random.shuffle(repo_name_list)
    random.shuffle(dict_total_code)
    dict_file_map_num=dict()
    dict_repo_map_num = dict()
    for repo_name,file,file_html,cl,me,code in dict_total_code[:500]:
        if file not in dict_file_map_num:
            dict_file_map_num[file]=0
        dict_file_map_num[file] += 1
        if repo_name not in dict_repo_map_num:
            dict_repo_map_num[repo_name] = 0
        dict_repo_map_num[repo_name] += 1
    print("random 500: ",dict_file_map_num,"\n",dict_repo_map_num,len(dict_repo_map_num.keys()))
    print("random repo_name_list: ",repo_name_list[:50])
    dict_test_case_inf=util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    count_test_case = 0
    count_test_file = 0
    repo_num=0
    # dict_repo_num[e[0]]
    dict_repo_map_test_case=dict()
    for repo_name in dict_repo_map_num:
        dict_repo_map_test_case[repo_name]=0
        repo_num += 1
        for file_html in dict_test_case_inf[repo_name]:
            count_test_case+=len(dict_test_case_inf[repo_name][file_html])
            count_test_file+=1
            dict_repo_map_test_case[repo_name]+=len(dict_test_case_inf[repo_name][file_html])
    print("count_test_case,count_test_file: ",repo_num,count_test_case,count_test_file)

    total_test_cases=0
    for repo in dict_repo_map_test_case:
        total_test_cases+=dict_repo_num[repo]*dict_repo_map_test_case[repo]
    print("total_test_cases: ",total_test_cases)

    dict_repo_map_test_case = dict()
    for repo_name in repo_name_list[:50]:
        dict_repo_map_test_case[repo_name] = 0
        repo_num += 1
        for file_html in dict_test_case_inf[repo_name]:
            count_test_case += len(dict_test_case_inf[repo_name][file_html])
            count_test_file += 1
            dict_repo_map_test_case[repo_name] += len(dict_test_case_inf[repo_name][file_html])
    print("count_test_case,count_test_file: ", repo_num, count_test_case, count_test_file)

    total_test_cases = 0
    for repo in repo_name_list[:50]:
        total_test_cases += dict_repo_num[repo] * dict_repo_map_test_case[repo]
    print("total_test_cases: ", total_test_cases)
    '''



