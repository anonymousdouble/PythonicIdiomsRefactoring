
import sys, ast, os, copy
import tokenize
import sys,shutil
import traceback

sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/test_case")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time
import util, github_util,get_test_case_acc_util,configure_pro_envir_util
import c_replace_content_by_ast_5_10
import confiure_pro_envior_by_requirements
import subprocess
from pathos.multiprocessing import ProcessingPool as newPool
import a_5_10_count_acc
selct_refactorings_dir = util.data_root + "5_10_all_test_cases/select/all_kinds/"
selct_file_name = ["list_compreh",'set_compreh',"dict_compreh",'set_compreh',
                   'mult_ass','call_star','chain_compare',
                   'for_else','for_target','truth_value_test']#
# dict_code_map_pass_test_case_code_dir=""
dict_code_map_pass_test_case_code_dir = [util.data_root + "5_10_all_test_cases/map_code_info_test_case/list_compreh/",
util.data_root + "5_10_all_test_cases/map_code_info_test_case/set_compreh/",
                                         util.data_root + "5_10_all_test_cases/select/map_code_info_test_case/dict_compreh/",
                                         util.data_root + "5_10_all_test_cases/map_code_info_test_case/set_compreh_own_config_false/",
                                         util.data_root + "5_10_all_test_cases/map_code_info_test_case/mult_ass/",
util.data_root + "5_10_all_test_cases/select/map_code_info_test_case/call_star/",
util.data_root + "5_10_all_test_cases/select/map_code_info_test_case/chain_compare/",
util.data_root + "5_10_all_test_cases/select/map_code_info_test_case/for_else/",
util.data_root + "5_10_all_test_cases/map_code_info_test_case/for_target/",
                                         util.data_root +            "5_10_all_test_cases/select/map_code_info_test_case/truth_value_test/"
                                         ]
#util.data_root + "5_10_all_test_cases/map_code_info_test_case/set_compreh_own_config_false/"

save_test_acc_dir_list=[util.data_root + "test_case_benchmark_dir/for_compre_list_acc_dir/",
                        util.data_root + "test_case_benchmark_dir/for_compre_set_acc_dir/",
                        util.data_root + "test_case_benchmark_dir/for_compre_dict_acc_dir/",
util.data_root + "test_case_benchmark_dir/for_compre_set_acc_dir/",
util.data_root + "test_case_benchmark_dir/multip_assign_complicated_acc_dir/",
                        util.data_root + "test_case_benchmark_dir/var_unpack_call_star_complicated_dir/",
util.data_root + "test_case_benchmark_dir/chain_comparison_acc_dir/",
                        util.data_root + "test_case_benchmark_dir/for_else_acc_dir/",
                        util.data_root + "test_case_benchmark_dir/var_unpack_for_target_complicated_dir/",

                            util.data_root + "test_case_benchmark_dir/truth_value_test_complicated_remove_len_dir/" ]
d=util.data_root + "5_10_all_test_cases/refactor_result_test_case/set_compreh/"



beg=0
all_count = 0
all_old_test_case = 0
all_count_test_case = 0
repo_list=[]
test_case_list=[]
old_test_case_list=[]
for ind,sele in enumerate(selct_file_name[:]):
    # if ind!=9:
    #     continue
    count = 0
    old_test_case = 0
    count_test_case = 0
    ind_other=beg+ind
    dict_test_case_inf_selct = util.load_pkl(selct_refactorings_dir, sele)
    for repo_name in dict_test_case_inf_selct:
        save_test_acc_dir = save_test_acc_dir_list[ind_other]
        complicate_code = util.load_pkl(save_test_acc_dir, repo_name)
        if not os.path.exists(dict_code_map_pass_test_case_code_dir[ind_other]+ repo_name+".pkl"):
            # print("")
            continue
        dict_code_map_pass_test_case = util.load_pkl(dict_code_map_pass_test_case_code_dir[ind_other], repo_name)
        for file_html, code_cl, code_me, code in dict_test_case_inf_selct[
            repo_name]:
            if repo_name=="Axelrod" and ind==8:
                continue
            count+=1
            repo_list.append(repo_name)

            # print(file_html)
            res = complicate_code['record_res']
            if ind<=3:
                (for_node, assign_node, remove_ass_flag, new_tree)=code
                old_code=file_html+ast.unparse(assign_node) + "\n" + ast.unparse(for_node)
            elif ind==4:
                old_node_str = "\n".join([ast.unparse(e) for e in code[0]])
                old_code = file_html + old_node_str
            elif ind==5:
                arg_seq = code[0][0]
                arg_str_list = [ast.unparse(arg) for arg in arg_seq]

                old_code = file_html + str(arg_str_list)
            elif ind==6 or ind==8 or ind==9:
                old_code = file_html+ast.unparse(code[0])
            elif ind == 7:
                old_code = file_html + ast.unparse(code[4])


            # print(old_code)
            #    # ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code", 'success', 'test_case_info']
            if file_html not in dict_code_map_pass_test_case:
                continue

            for e in res:
                if old_code==e[1] + str(e[5]) if ind!=7 else e[1] + e[6]:
                    # print("last")
                    # print(e[-1])
                    old_test_case+=len(e[-1])
                    old_test_case_list+=["".join(e_e) for e_e in e[-1]]
                    break


                # if "".join(e[1:4]) + e[5]==
                # print("".join(e[1:4])+e[5])
                # if "$".join(["".join(e[1:4]),e[4]])=="".join([file_html, code_cl, code_me]):
                #     print(e[0])
            # print("code_node", file_html, code_cl, code_me, str((for_node, assign_node, remove_ass_flag, new_tree)))
            if 1:
                try:
                    for code_node in dict_code_map_pass_test_case[file_html][code_cl][code_me]:
                        if ind <= 3:
                            (for_node, assign_node, remove_ass_flag, new_tree) = code
                            code_node_str=file_html+ast.unparse(assign_node) + "\n" + ast.unparse(for_node)
                        elif ind == 4:
                           code_node_str= file_html+"\n".join([ast.unparse(e) for e in code_node[0]])
                        elif ind==5:
                            arg_seq = code_node[0]
                            arg_str_list = [ast.unparse(arg) for arg in arg_seq]
                            code_node_str =file_html + str(arg_str_list)
                        elif ind == 6 or ind == 8 or ind == 9:
                            code_node_str = file_html + ast.unparse(code_node[0])
                        elif ind == 7:
                            code_node_str = file_html + ast.unparse(code_node[1])
                        if old_code ==code_node_str:

                            count_test_case+=len(dict_code_map_pass_test_case[file_html][code_cl][code_me][code_node])
                            test_case_list+=["".join(e) for e in dict_code_map_pass_test_case[file_html][code_cl][code_me][code_node]]
                            break
                except:
                    # traceback.print_exc()
                    continue
    all_count+=count
    all_old_test_case+=old_test_case
    all_count_test_case+=count_test_case
    print("cout_test_case: ",count_test_case,old_test_case,count)
    print("unique cout_test_case: ", len(set(old_test_case_list)), len(set(test_case_list)))
result_csv = []
print("total cout_test_case: ",all_old_test_case/all_count_test_case,len(repo_list),all_count_test_case,all_old_test_case,all_count,len(repo_list),len(set(repo_list)))
save_test_methods_dir_success = util.data_root + "5_10_all_test_cases/success_test_cases/"
# save_test_methods_dir_simplify = util.data_root + "5_10_all_test_cases/"
# dict_test_case_inf = util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
save_test_methods_dir_simplify = util.data_root + "5_10_all_test_cases/"
dict_test_case_inf_all_tcs = util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
# print(dict_test_case_inf)
total_tcs=0
total_suc_tcs=0
dict_repo_num=dict()
for repo in list(set(repo_list)):
    if repo not in dict_test_case_inf_all_tcs:
        print("miss ",repo)
        continue
    for test_html in dict_test_case_inf_all_tcs[repo]:
        test_case_name = test_html.split("/")[-1]
        # for cl, me in dict_test_case_inf[repo][test_html]:
        total_tcs+=len(dict_test_case_inf_all_tcs[repo][test_html])
    dict_test_case_inf = util.load_pkl(save_test_methods_dir_success, repo)
    for test_html in dict_test_case_inf:

        total_suc_tcs+=len(dict_test_case_inf[test_html])
        if repo not in dict_repo_num:
            dict_repo_num[repo]=0
        dict_repo_num[repo]+=len(dict_test_case_inf[test_html])
print(total_tcs,total_suc_tcs)
print(dict_repo_num)
total_tcs_all_refactoring=0
for e in repo_list:
    total_tcs_all_refactoring+=dict_repo_num[e]
print(total_tcs_all_refactoring)




'''
for file in os.listdir(save_test_acc_dir):
    repo_name = file[:-4]
    print("repo_name: ",repo_name)
    complicate_code = util.load_pkl(save_test_acc_dir, repo_name)
    res = complicate_code['record_res']
    # print(complicate_code)
    for e in res:
        print("come here")
        print(e)
        break
    else:
        continue
    break
'''
    # ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code", 'success', 'test_case_info']
'''
all_total_count, all_acc_count = 0, 0
count_test = 0
code_count = 0
repo_test = []
for repo in os.listdir(result_3215_test_case_dir):
    repo_name = repo[:-4]
    if repo_name not in repo_name_list:
        print("repo_name: ", repo_name)
    repo_test.append(repo_name)
    dict_test_case_inf_selct_result = util.load_pkl(result_3215_test_case_dir, repo_name)
    for file_html, code_cl, code_me, (for_node, assign_node, remove_ass_flag, new_tree) in dict_test_case_inf_selct[
        repo_name]:
        for e in dict_test_case_inf_selct_result:
            if ast.unparse(new_tree) == e[-4]:
                count_test += 1
                break
        else:
            print("the code has not be tested! ", file_html)
        code_count += 1

    total_count, acc_count = a_5_10_count_acc.count_acc(dict_test_case_inf_selct_result)
    all_total_count += total_count
    all_acc_count += acc_count
print("count: ", len(os.listdir(result_3215_test_case_dir)), all_total_count, all_acc_count, code_count, count_test)
print("repo no test: ", set(repo_name_list) - set(repo_test))  # def count_acc(dict_success_run_test_case):
'''