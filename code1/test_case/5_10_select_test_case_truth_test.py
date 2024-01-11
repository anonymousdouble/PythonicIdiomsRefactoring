import sys, ast, os, copy
import tokenize
import sys, shutil
import traceback

sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/test_case")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time
import util, github_util, get_test_case_acc_util, configure_pro_envir_util
import c_replace_content_by_ast_5_10,a_5_10_count_acc
import confiure_pro_envior_by_requirements
import subprocess
from pathos.multiprocessing import ProcessingPool as newPool


def save_code_map_test_cases(repo_name):
    # repo_name = file_name[:-4]
    # repo_name = "pydicom"
    repo_path = pro_path + repo_name + "/"
    dict_success_run_test_case = util.load_pkl(save_test_methods_dir_success, repo_name)
    dict_code_map_pass_test_case = dict()
    slow_test_html_list = []
    for file_html,code_cl,code_me, (old_tree, new_tree) in dict_test_case_inf_selct[repo_name]:

        old_content, new_content, flag_same = \
            c_replace_content_by_ast_5_10.replace_content_truth_value_test_insert_comehere(repo_name,file_html,old_tree,new_tree)
        if flag_same:
            continue
        print(file_html,flag_same)
        print(ast.unparse(old_tree))
        # print("------------------")
        print(new_content)
        #break
        #'''
        real_file_html = file_html.replace("//", "/")
        rela_path = real_file_html.split("/")[6:]
        old_path = repo_path + "/".join(rela_path)
        shutil.copyfile(old_path, old_path[:-3] + "_copy_copy_zejun.py")
        util.save_file_path(old_path, new_content)

        rela_path[-1] = "".join([rela_path[-1][:-3], "_copy_zejun", ".py"])
        # print(">>>>>>>>>>new_content: ", old_content)
        rela_path = "/".join(rela_path)
        # print(repo_path+rela_path)
        util.save_file_path(repo_path + rela_path, old_content)  # copy 一份原来的文件防止失去

        try:
            for test_html in dict_success_run_test_case:
                if test_html in slow_test_html_list:
                    continue
                # if test_html != "https://github.com/dpkp/kafka-python/tree/master/test/test_cluster.py":#"https://github.com/idealo/imagededup/tree/master/tests/test_evaluator.py":#"https://github.com/google/pinject/tree/master/tests/decorators_test.py":#"https://github.com/wannesm/dtaidistance/tree/master/tests/test_dtw.py":#"https://github.com/wannesm/dtaidistance/tree/master/tests/test_dtw.py":#"https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/transforms/opconversions/bksf_test.py":#"https://github.com/quantumlib/OpenFermion/tree/master/src/openfermion/transforms/opconversions/bksf_test.py":#"https://github.com/inducer/pudb/tree/master/test/test_settings.py":#"https://github.com/threat9/routersploit/tree/master/tests/creds/routers/3com/test_3com_ftp_default_creds.py":#"https://github.com/threat9/routersploit/tree/master/tests/creds/routers/3com/test_3com_ssh_default_creds.py":#"https://github.com/threat9/routersploit/tree/master/tests/creds/routers/2wire/test_ssh_default_creds.py":#"https://github.com/threat9/routersploit/tree/master/tests/creds/routers/2wire/test_ftp_default_creds.py":#"https://github.com/threat9/routersploit/tree/master/tests/creds/routers/2wire/test_telnet_default_creds.py":#"https://github.com/threat9/routersploit/tree/master/tests/exploits/routers/technicolor/test_tg784_authbypass.py":#"https://github.com/threat9/routersploit/tree/master/tests/exploits/routers/3com/test_officeconnect_rce.py":#"https://github.com/threat9/routersploit/tree/master/tests/exploits/routers/shuttle/test_915wm_dns_change.py":#"https://github.com/threat9/routersploit/tree/master/tests/creds/routers/2wire/test_ssh_default_creds.py":#"https://github.com/threat9/routersploit/tree/master/tests/exploits/routers/shuttle/test_915wm_dns_change.py":#'https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_dataset.py' and test_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_fileset.py":
                #     continue
                #     print("come here")
                for cl, me in dict_success_run_test_case[test_html]:
                    # if me != "test_validate_and_correct_file_meta" and me != "test_bad_file_id":
                    #     continue
                    fun_list = ["::".join([cl, me]) if cl else me]
                    run_test_result = configure_pro_envir_util.run_test_file_capture_output_each_fun(
                        test_html, repo_path,
                        fun_list=fun_list,
                        export_python=True)

                    if run_test_result == "TimeoutExpired":
                        slow_test_html_list.append(test_html)
                        print(">>>>>>Time out run pytest, please check ", test_html)
                        break
                    print(">>>>>>>>>>run_test_result: ", run_test_result)
                    through_flag = configure_pro_envir_util.test_result_through_code(run_test_result)
                    dict_me_re, flag_pass = configure_pro_envir_util.get_test_result(run_test_result)
                    if flag_pass and through_flag:

                        if file_html not in dict_code_map_pass_test_case:
                            dict_code_map_pass_test_case[file_html] = dict()
                        if code_cl not in dict_code_map_pass_test_case[file_html]:
                            dict_code_map_pass_test_case[file_html][code_cl] = dict()
                        if code_me not in dict_code_map_pass_test_case[file_html][code_cl]:
                            dict_code_map_pass_test_case[file_html][code_cl][code_me] = dict()
                            # (arg_list, new_tree)
                        if (old_tree, new_tree) not in \
                                dict_code_map_pass_test_case[file_html][code_cl][code_me]:
                            dict_code_map_pass_test_case[file_html][code_cl][code_me][
                                (old_tree, new_tree)] = []
                        dict_code_map_pass_test_case[file_html][code_cl][code_me][
                            (old_tree, new_tree)].append([test_html, cl, me])
                    print(">>>>>>>>>>dict_me_re: ", fun_list, dict_me_re, flag_pass, through_flag)
                #     break
                # break
            util.save_file_path(old_path, old_content)
        except:
            util.save_file_path(old_path, old_content)
            # print("save successufully")
            traceback.print_exc()
        #'''
    util.save_pkl(dict_code_map_pass_test_case_code_dir, repo_name, dict_code_map_pass_test_case)
    print("save successufully code infor")
    # for file_html in complicate_code:
    #     # if file_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/fileset.py" and file_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/dataset.py":
    #     #     continue
    #     for code_cl in complicate_code[file_html]:
    #         for code_me in complicate_code[file_html][code_cl]:
    #             for ind, (for_node, assign_node, remove_ass_flag, new_tree) in enumerate(
    #                     complicate_code[file_html][code_cl][code_me]):
    #                 old_content, new_content, flag_same = c_replace_content_by_ast_5_10.replace_file_content_for_compre_3_category_insert_comehere(
    #                     repo_name, file_html, for_node, assign_node, new_tree, remove_ass_flag)
    #                 # print(file_html)
    #                 # '''
    #
    #                 real_file_html = file_html.replace("//", "/")
    #                 rela_path = real_file_html.split("/")[6:]
    #                 old_path = repo_path + "/".join(rela_path)
    #                 shutil.copyfile(old_path, old_path[:-3] + "_copy_copy_zejun.py")
    #                 util.save_file_path(old_path, new_content)
    #
    #                 rela_path[-1] = "".join([rela_path[-1][:-3], "_copy_zejun", ".py"])
    #                 # print(">>>>>>>>>>new_content: ", old_content)
    #                 rela_path = "/".join(rela_path)
    #                 # print(repo_path+rela_path)
    #                 util.save_file_path(repo_path + rela_path, old_content)  # copy 一份原来的文件防止失去
    #                 try:
    #                     for test_html in dict_success_run_test_case:
    #                         if test_html in slow_test_html_list:
    #                             continue
    #                         # if test_html != 'https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_dataset.py' and test_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_fileset.py":
    #                         #     continue
    #                         for cl, me in dict_success_run_test_case[test_html]:
    #                             # if me != "test_validate_and_correct_file_meta" and me != "test_bad_file_id":
    #                             #     continue
    #                             fun_list = ["::".join([cl, me]) if cl else me]
    #                             run_test_result = configure_pro_envir_util.run_test_file_capture_output_each_fun(
    #                                 test_html, repo_path,
    #                                 fun_list=fun_list,
    #                                 export_python=True)
    #                             if run_test_result == "TimeoutExpired":
    #                                 slow_test_html_list.append(test_html)
    #                                 print(">>>>>>Time out run pytest, please check ", test_html)
    #                                 break
    #                             # print(">>>>>>>>>>run_test_result: ", run_test_result)
    #                             through_flag = configure_pro_envir_util.test_result_through_code(run_test_result)
    #                             dict_me_re, flag_pass = configure_pro_envir_util.get_test_result(run_test_result)
    #                             if flag_pass and through_flag:
    #
    #                                 if file_html not in dict_code_map_pass_test_case:
    #                                     dict_code_map_pass_test_case[file_html] = dict()
    #                                 if code_cl not in dict_code_map_pass_test_case[file_html]:
    #                                     dict_code_map_pass_test_case[file_html][code_cl] = dict()
    #                                 if code_me not in dict_code_map_pass_test_case[file_html][code_cl]:
    #                                     dict_code_map_pass_test_case[file_html][code_cl][code_me] = dict()
    #                                 if (for_node, assign_node, remove_ass_flag, new_tree) not in \
    #                                         dict_code_map_pass_test_case[file_html][code_cl][code_me]:
    #                                     dict_code_map_pass_test_case[file_html][code_cl][code_me][
    #                                         (for_node, assign_node, remove_ass_flag, new_tree)] = []
    #                                 dict_code_map_pass_test_case[file_html][code_cl][code_me][
    #                                     (for_node, assign_node, remove_ass_flag, new_tree)].append([test_html, cl, me])
    #                             print(">>>>>>>>>>dict_me_re: ", fun_list, dict_me_re, flag_pass, through_flag)
    #                         #     break
    #                         # break
    #                     util.save_file_path(old_path, old_content)
    #                 except:
    #                     util.save_file_path(old_path, old_content)
    #                     print("save successufully")
    # util.save_pkl(dict_code_map_pass_test_case_code_dir, repo_name, dict_code_map_pass_test_case)
    # # dict_success_run_test_case = util.load_pkl(dict_code_map_pass_test_case_code_dir, repo_name)
    # # print(dict_success_run_test_case)


if __name__ == '__main__':
    pro_dir = util.data_root + "python_star_2000repo/"
    pro_path = util.data_root + "python_star_2000repo/"
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    evaluation_testing_dir = util.data_root + "5_10_all_test_cases/evaluation/"  # test_case_benchmark_dir_csv/"#

    save_test_methods_dir_success = util.data_root + "5_10_all_test_cases/success_test_cases/"
    dict_code_map_pass_test_case_code_dir = util.data_root + "5_10_all_test_cases/select/map_code_info_test_case/truth_value_test/"
    # util.save_pkl(dict_code_map_pass_test_case_code_dir, "test", dict())

    save_test_methods_dir_simplify = util.data_root + "5_10_all_test_cases/"
    dict_test_case_inf = util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    selct_refactorings_dir=util.data_root + "5_10_all_test_cases/select/selct_code_info_3/"

    selct_file_name="truth_value_test"

    dict_test_case_inf_selct = util.load_pkl(selct_refactorings_dir, selct_file_name)

    # repo_name_list = [file[:-4] for file in os.listdir(complicate_code_dir)]
    selct_repo_list = list(dict_test_case_inf_selct.keys())
    repo_name_list=selct_repo_list
    print("repo_name_list: ",len(repo_name_list),repo_name_list)
    # a_5_10_count_acc.get_code_map_test_case_info(dict_code_map_pass_test_case_code_dir)

    total_test_cases = 0
    success_run_test_cases = 0
    repo_num = 0
    repo_exist_test_case = []
    for file_name in os.listdir(save_test_methods_dir_success):
        repo_name = file_name[:-4]
        if repo_name not in repo_name_list:
            # print(f"{repo_name} not in ",repo_name_list)
            continue
        repo_num += 1
        repo_exist_test_case.append(repo_name)
        dict_success_run_test_case = util.load_pkl(save_test_methods_dir_success, repo_name)
        for test_html in dict_success_run_test_case:
            success_run_test_cases += len(dict_success_run_test_case[test_html])
        if repo_name in dict_test_case_inf:
            for file_html in dict_test_case_inf[repo_name]:
                total_test_cases += len(dict_test_case_inf[repo_name][file_html])

    print("total success run test cases: ",repo_exist_test_case, len(repo_exist_test_case), len(repo_name_list), repo_num, total_test_cases,
          success_run_test_cases)

    # print("intersect repo: ",selct_repo_list-set(repo_name_list))
    remain_list=list(set(selct_repo_list[:])&set(repo_exist_test_case))
    print("remain_list: ",remain_list)
    for e in os.listdir(dict_code_map_pass_test_case_code_dir):
        print(e)
        if e[:-4] in remain_list:
            remain_list.remove(e[:-4])
    print("remain_list: ",remain_list)
    '''
    pool = newPool(nodes=30)
    pool.map(save_code_map_test_cases, remain_list[:])  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    '''
    #'''
    old_test_case=0
    count_test_case=0
    for repo_name in list(set(selct_repo_list[:])&set(repo_exist_test_case)):
        print(repo_name)
        # save_test_acc_dir=util.data_root + "test_case_benchmark_dir/var_unpack_for_target_complicated_dir/"
        save_test_acc_dir=util.data_root + "test_case_benchmark_dir/chain_comparison_acc_dir/"
        save_test_acc_dir=util.data_root + "test_case_benchmark_dir/truth_value_test_complicated_remove_len_dir/"
        # save_test_acc_dir=util.data_root + "test_case_benchmark_dir/multip_assign_complicated_acc_dir/"
        complicate_code = util.load_pkl(save_test_acc_dir, repo_name)
        res = complicate_code['record_res']
        try:
            dict_code_map_pass_test_case = util.load_pkl(dict_code_map_pass_test_case_code_dir, repo_name)
        #sprint(dict_code_map_pass_test_case)
        except:
            traceback.print_exc()
            continue

        for file_html, code_cl, code_me, code in dict_test_case_inf_selct[
            repo_name]:
            if file_html not in dict_code_map_pass_test_case:
                continue
            print(code)
            code_str = ast.unparse(code[0])
            # arg_str_list = [ast.unparse(arg) for arg in arg_seq]

            old_code=file_html+code_str

            for e in res:
                if old_code == e[1] + str(e[5]):
                    # print("last")
                    print(e[-1])
                    old_test_case += len(e[-1])
                    break

            for code_node in dict_code_map_pass_test_case[file_html][code_cl][code_me]:
                print(code_node)
                if code_str == ast.unparse(code_node[0]):
                    count_test_case += len(dict_code_map_pass_test_case[file_html][code_cl][code_me][code_node])
                    break
    print("count: ",old_test_case,count_test_case)

    #'''

