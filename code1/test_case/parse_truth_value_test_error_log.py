import sys, ast, os, copy
import tokenize
import sys,shutil,time

sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/test_case")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import util, github_util,get_test_case_acc_util,configure_pro_envir_util
import replace_content_by_ast
import subprocess
from pathos.multiprocessing import ProcessingPool as newPool
file_path=util.code_root+"test_case/get_test_case_acc_truth_value_test_parallel.log"

# file_path=util.code_root+"test_case/get_test_case_acc_truth_value_test_parallel.log"
content_list=util.load_file_path(file_path).split("come the file_html:")
dict_repo_error_test_case_info=dict()
dict_repo_all=dict()
code_complic_count=0
fail_complic_count=0#*******************it is failed:
all_code_complic_count = 0
error_dict={"None":0,"True":0,"==":0,"len":0,"other": []}
for each_file in content_list:

    if ">>>>>>>>>>dict_me_re" in each_file and "[] 0" in each_file :

        res=each_file.split("\n")
        file_html=""
        for file_ind,each_row in enumerate(res):

            if file_ind==0:


                file_html=each_row.strip()
                print("file_html: ",file_html)
                if not file_html.startswith("https://"):
                    break
                repo_name = file_html.split("/")[4]
                if repo_name not in dict_repo_error_test_case_info:
                    dict_repo_error_test_case_info[repo_name]=dict()
                if file_html not in dict_repo_error_test_case_info[repo_name]:
                        dict_repo_error_test_case_info[repo_name][file_html]=[]
            elif each_row.startswith(">>>>>>>>>>dict_me_re:") and "[] 0" in each_row:
                func_list=each_row.split("']")[:-1]
                print("this file_html: ", file_html,func_list)
                pre_test_html="/".join(file_html.split("/")[:7])+"/"
                for ind_fun,e in enumerate(func_list):
                    beg_ind = e.find("['")

                    func_list[ind_fun]=func_list[ind_fun][beg_ind+2:].strip()
                    py_ind = func_list[ind_fun].find(".py::")
                    test_html = pre_test_html + func_list[ind_fun][:py_ind + 3]
                    func_list[ind_fun]=func_list[ind_fun][py_ind+5:]
                    dict_repo_error_test_case_info[repo_name][file_html].append([test_html,func_list])
            elif each_row.startswith("****************we save the old content to original"):
                code_complic_count+=1
            if "it is failed" in each_row:#.strip().startswith("*******************it is failed:")
                if "None" in each_row:
                    print("None each_row: ", each_row)
                    error_dict["None"]+=1
                elif "True" in each_row:
                    error_dict["True"] += 1
                elif "len" in each_row:
                    error_dict["len"]+=1
                elif "==" in each_row:
                    print("each_row: ", each_row)
                    error_dict["=="] += 1
                else:
                    error_dict["other"].append(each_row)
                fail_complic_count+=1
    if ">>>>>>>>>>dict_me_re" in each_file:

        res = each_file.split("\n")
        file_html = ""
        for file_ind, each_row in enumerate(res):

            if file_ind == 0:

                file_html = each_row.strip()
                if not file_html.startswith("https://"):
                    break
                print("file_html: ", file_html)
                repo_name = file_html.split("/")[4]
                if repo_name not in dict_repo_all:
                    dict_repo_all[repo_name] = dict()
                if file_html not in dict_repo_all[repo_name]:
                    dict_repo_all[repo_name][file_html] = []
            elif each_row.startswith(">>>>>>>>>>dict_me_re:") :
                func_list = each_row.split("']")[:-1]
                print("this file_html: ", file_html, func_list)
                pre_test_html = "/".join(file_html.split("/")[:7]) + "/"
                for ind_fun, e in enumerate(func_list):
                    beg_ind = e.find("['")

                    func_list[ind_fun] = func_list[ind_fun][beg_ind + 2:].strip()
                    py_ind = func_list[ind_fun].find(".py::")
                    test_html = pre_test_html + func_list[ind_fun][:py_ind + 3]
                    func_list[ind_fun] = func_list[ind_fun][py_ind + 5:]
                    dict_repo_all[repo_name][file_html].append([test_html, func_list])
            elif each_row.startswith("****************we save the old content to original"):
                all_code_complic_count += 1

def get_cout(dict_repo_error_test_case_info) :
    count=0
    file_count=0
    repo_count=0
    for repo_name in dict_repo_error_test_case_info:
        repo_count+=1
        for file in dict_repo_error_test_case_info[repo_name]:
            file_count+=1
            for e in dict_repo_error_test_case_info[repo_name][file]:
                count+=1
                # print("each test case: ",e)
    return repo_count,file_count,count
repo_count,file_count,count= get_cout(dict_repo_error_test_case_info)
print("total count of failing complicated code1,test_case and test files: ",repo_count,code_complic_count,count,file_count,fail_complic_count,error_dict)
repo_count,file_count,count= get_cout(dict_repo_all)
print("total count of failing complicated code1,test_case and test files: ",repo_count,all_code_complic_count,count,file_count)


def get_each_repo_test_acc(info_list,save_test_acc_dir):
    file = info_list[0]
    save_test_file_res_dir = info_list[1]
    save_me_test_me_dir = info_list[2]
    complicated_code_dir_pkl = info_list[3]
    res=[]
    # for each repo
    file_list = set([])
    me_list = set([])
    me_count=0
    file_count=0
    repo_count=0
    complic_code_count=0
    total_count=0
    total_acc_count=0
    if 1:
    # for file in os.listdir(save_test_file_res_dir):
        dict_test_acc = {'total_count': 0, 'total_acc_count': 0, 'repo_count': 0, 'file_count': 0,
                     'me_count': 0, 'complic_code_count': 0, "record_res": [], 'me_list': set([]), 'file_list': set([])}

        repo_name=file[:-4]
        repo_fla = 0
        # if repo_name != "cloud-custodian":#"spiderfoot":
        #     continue
        print("come to the repo: ", file)
        pro_path = util.data_root + "python_star_2000repo/"
        repo_path=pro_path + repo_name + "/"
        dict_complica_me_list = get_test_case_acc_util.get_comp_code_can_test_me(repo_name,save_test_file_res_dir,save_me_test_me_dir)
        # print("dict_complica_me_list: ", dict_complica_me_list)
        complicate_code = util.load_pkl(complicated_code_dir_pkl, repo_name)
        for file_html in complicate_code:
            flag_file=0
            if file_html in dict_complica_me_list and file_html in dict_repo_error_test_case_info[repo_name]:

                # if file_html!="https://github.com/pymc-devs/pymc/tree/master/pymc/sampling.py":#"https://github.com/smicallef/spiderfoot/tree/master//sflib.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#
                #     continue

                print("come the file_html: ",file_html)
                for cl in complicate_code[file_html]:

                    for me in complicate_code[file_html][cl]:
                        me_name = me.split("$")[0]
                        if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
                            continue
                        total_name=get_test_case_acc_util.get_total_name(file_html,cl,me_name)
                        # print("come total_name: ", cl,me_name,total_name)
                        if total_name in dict_complica_me_list[file_html]:
                            test_me_inf_list=dict_complica_me_list[file_html][total_name]
                            if complicate_code[file_html][cl][me] and test_me_inf_list:
                                flag_file=1
                                repo_fla=1
                                me_count+=1
                                dict_test_acc['me_count'] += 1
                                for ind, (old_tree, new_tree) in enumerate(
                                    complicate_code[file_html][cl][me]):
                                    complic_code_count += 1
                                    dict_test_acc['complic_code_count'] += 1
                                    # print("come to complicate_code: ", file_html)
                                    # print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ", new_tree.lineno, ast.unparse(new_tree))  #
                                    # print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ", old_tree.lineno,
                                    #       ast.unparse(old_tree))  # old_tree.lineno,arg_list
                                    file_list.add(file_html)
                                    me_list.add(total_name)
                                    total_count+=1
                                    dict_test_acc['total_count'] += 1
                                    old_content, new_content,flag_same = replace_content_by_ast.replace_content_truth_value_test(repo_name, file_html, old_tree,new_tree)
                                    if flag_same:
                                        print("please check because the code1 is not changed: ", file_html)
                                        continue
                                    # print(">>>>>>>>>>old_content: ", old_content)

                                    real_file_html = file_html.replace("//", "/")
                                    rela_path =  real_file_html.split("/")[6:]
                                    old_path = repo_path + "/".join(rela_path)
                                    util.save_file_path(old_path, new_content)
                                    rela_path[-1]="".join([rela_path[-1][:-3],"_copy_zejun",".py"])
                                    # print(">>>>>>>>>>new_content: ", new_content)
                                    rela_path="/".join(rela_path)
                                    # print(repo_path+rela_path)
                                    util.save_file_path(repo_path+rela_path, old_content)# copy 一份原来的文件防止失去

                                    test_info = []

                                    for test_html,each_rela_path, cl, me in test_me_inf_list:

                                        # test_html_list=test_html.split("/")
                                        # test_html_list[-1] = "".join([test_html_list[-1][:-3],"_copy_zejun",".py"])
                                        # test_html_list="/".join(test_html_list)
                                        fun_list = [ "::".join([cl,me])if cl else me]
                                        test_info.append([test_html,cl, me])
                                        # test_content=util.load_file_path(old_path)
                                        # print(">>>>>>>>>>test_content: ",test_content)
                                        run_test_result = configure_pro_envir_util.run_test_file(test_html, repo_path,fun_list=fun_list)
                                        if run_test_result== "TimeoutExpired" :
                                            print("*******************Time out run pytest, please check ",test_html,run_test_result)
                                            continue
                                        # print(">>>>>>>>>>run_test_result: ", run_test_result)
                                        dict_me_re, flag_pass = configure_pro_envir_util.get_test_result(run_test_result)

                                        print(">>>>>>>>>>dict_me_re: ",fun_list,dict_me_re,flag_pass)

                                        if not flag_pass:

                                            util.save_file_path(old_path, old_content)
                                            print("*******************it is failed: ", ast.unparse(old_tree),
                                                  ast.unparse(new_tree), run_test_result)
                                            res.append(
                                                [repo_name, file_html,test_info,str(flag_pass),ast.unparse(old_tree), ast.unparse(new_tree)])
                                            print("****************we save the old content to original file: ", old_path)

                                            break
                                    else:

                                        total_acc_count+=1
                                        dict_test_acc['total_acc_count'] +=1

                                        util.save_file_path(old_path, old_content)
                                        res.append([repo_name, file_html, test_info,str(1),ast.unparse(old_tree), ast.unparse(new_tree)])
                                        print("****************we save the old content to original file: ", old_path)
                                        # break
        #                             # util.save_file_path(old_path, old_content)
            file_count+=flag_file
            dict_test_acc['file_count']+=flag_file
        repo_count+=repo_fla
        dict_test_acc['repo_count']+=repo_fla
        dict_test_acc['record_res']=res
        dict_test_acc['me_list'] = me_list
        dict_test_acc['file_list'] = file_list

        #                         else:
        #                             continue
        #                         break
        #             else:
        #                 continue
        #             break
        #         else:
        #             continue
        #         break

        util.save_pkl(save_test_acc_dir, repo_name, dict_test_acc)
    print(total_acc_count,total_count)
    print("repo_count,file_count,me_count,complic_code_count:",repo_count,file_count,me_count,complic_code_count)
# save_test_acc_dir = util.data_root + "acc_res_compli_test_case_error_log/truth_value_test_complicated_acc_dir/"
# save_me_test_me_dir= util.data_root + "methods_test_method_pair/truth_value_test_complicated/"
# complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated/"
# save_test_file_res_dir=util.data_root + "save_test_file_res_dir/truth_value_test_complicated/"
# time_start = time.time()
# # repo_list=configure_pro_envir_util.prepare_data(save_me_test_me_dir, save_test_file_res_dir)
# repo_list = []
# if not os.path.exists(save_test_acc_dir):
#         os.makedirs(save_test_acc_dir)
# else:
#         shutil.rmtree(save_test_acc_dir)  # Removes all the subdirectories!
#         os.makedirs(save_test_acc_dir)
# for file in dict_repo_error_test_case_info:
#         repo_list.append([file+".pkl", save_test_file_res_dir, save_me_test_me_dir, complicated_code_dir_pkl])
# pool = newPool(nodes=30)
# pool.map(get_each_repo_test_acc, repo_list)  # [:3]sample_repo_url ,token_num_list[:1]
# pool.close()
# pool.join()
# time_end = time.time()
# print("total time: ", time_end - time_start)



