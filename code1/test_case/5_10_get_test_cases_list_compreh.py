
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
import c_replace_content_by_ast_5_10
import confiure_pro_envior_by_requirements
import subprocess
from pathos.multiprocessing import ProcessingPool as newPool
def save_code_map_test_cases(repo_name):
    # repo_name = file_name[:-4]
    # repo_name = "pydicom"
    repo_path = pro_path + repo_name + "/"
    dict_success_run_test_case = util.load_pkl(save_test_methods_dir_success, repo_name)
    complicate_code = util.load_pkl(complicate_code_dir, repo_name)
    dict_code_map_pass_test_case = dict()
    slow_test_html_list=[]
    for file_html in complicate_code:
        # if file_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/fileset.py" and file_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/dataset.py":
        #     continue
        for code_cl in complicate_code[file_html]:
            for code_me in complicate_code[file_html][code_cl]:
                for ind, (for_node, assign_node, remove_ass_flag, new_tree) in enumerate(
                        complicate_code[file_html][code_cl][code_me]):
                    old_content, new_content, flag_same = c_replace_content_by_ast_5_10.replace_file_content_for_compre_3_category_insert_comehere(
                        repo_name, file_html, for_node, assign_node, new_tree, remove_ass_flag)
                    # print(file_html)
                    # '''

                    real_file_html = file_html.replace("//", "/")
                    rela_path = real_file_html.split("/")[6:]
                    old_path = repo_path + "/".join(rela_path)
                    shutil.copyfile(old_path, old_path[:-3]+"_copy_copy_zejun.py")
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
                            # if test_html != 'https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_dataset.py' and test_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_fileset.py":
                            #     continue
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
                                # print(">>>>>>>>>>run_test_result: ", run_test_result)
                                through_flag = configure_pro_envir_util.test_result_through_code(run_test_result)
                                dict_me_re, flag_pass = configure_pro_envir_util.get_test_result(run_test_result)
                                if flag_pass and through_flag:

                                    if file_html not in dict_code_map_pass_test_case:
                                        dict_code_map_pass_test_case[file_html] = dict()
                                    if code_cl not in dict_code_map_pass_test_case[file_html]:
                                        dict_code_map_pass_test_case[file_html][code_cl] = dict()
                                    if code_me not in dict_code_map_pass_test_case[file_html][code_cl]:
                                        dict_code_map_pass_test_case[file_html][code_cl][code_me] = dict()
                                    if (for_node, assign_node, remove_ass_flag, new_tree) not in \
                                            dict_code_map_pass_test_case[file_html][code_cl][code_me]:
                                        dict_code_map_pass_test_case[file_html][code_cl][code_me][
                                            (for_node, assign_node, remove_ass_flag, new_tree)] = []
                                    dict_code_map_pass_test_case[file_html][code_cl][code_me][
                                        (for_node, assign_node, remove_ass_flag, new_tree)].append([test_html, cl, me])
                                print(">>>>>>>>>>dict_me_re: ", fun_list, dict_me_re, flag_pass, through_flag)
                            #     break
                            # break
                        util.save_file_path(old_path, old_content)
                    except:
                        util.save_file_path(old_path, old_content)
                        print("save successufully")
    util.save_pkl(dict_code_map_pass_test_case_code_dir, repo_name, dict_code_map_pass_test_case)
    # dict_success_run_test_case = util.load_pkl(dict_code_map_pass_test_case_code_dir, repo_name)
    # print(dict_success_run_test_case)
if __name__ == '__main__':
    pro_dir = util.data_root + "python_star_2000repo/"
    pro_path = util.data_root + "python_star_2000repo/"
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    evaluation_testing_dir=util.data_root +"5_10_all_test_cases/evaluation/"#test_case_benchmark_dir_csv/"#

    save_test_methods_dir_success = util.data_root + "5_10_all_test_cases/success_test_cases/"
    complicate_code_dir = util.data_root + "5_10_all_test_cases/code_info_3215/list_compreh/"
    dict_code_map_pass_test_case_code_dir=util.data_root + "5_10_all_test_cases/map_code_info_test_case/list_compreh/"
    save_test_methods_dir_simplify = util.data_root + "5_10_all_test_cases/"
    dict_test_case_inf=util.load_pkl(save_test_methods_dir_simplify, "all_test_case")

    repo_name_list=[file[:-4] for file in os.listdir(complicate_code_dir)]

    total_test_cases = 0
    success_run_test_cases = 0
    repo_num = 0
    repo_exist_test_case=[]
    for file_name in os.listdir(save_test_methods_dir_success):
        repo_name = file_name[:-4]
        if repo_name not in repo_name_list:
            continue
        repo_num += 1
        repo_exist_test_case.append(repo_name)
        dict_success_run_test_case = util.load_pkl(save_test_methods_dir_success, repo_name)
        for test_html in dict_success_run_test_case:
            success_run_test_cases += len(dict_success_run_test_case[test_html])
        if repo_name in dict_test_case_inf:
            for file_html in dict_test_case_inf[repo_name]:
                total_test_cases += len(dict_test_case_inf[repo_name][file_html])

    print("total success run test cases: ", len(repo_exist_test_case), len(repo_name_list),repo_num, total_test_cases, success_run_test_cases)

    #'''
    pool = newPool(nodes=30)
    pool.map(save_code_map_test_cases, repo_exist_test_case)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    #'''
    # for file_name in os.listdir(complicate_code_dir[:1]):
    #     save_code_map_test_cases(file_name)
    '''
        repo_name=file_name[:-4]
        repo_name="pydicom"
        repo_path=pro_path + repo_name + "/"
        dict_success_run_test_case = util.load_pkl(save_test_methods_dir_success, repo_name)
        complicate_code=util.load_pkl(complicate_code_dir, repo_name)
        dict_code_map_pass_test_case = dict()
        for file_html in complicate_code:
            if file_html!="https://github.com/pydicom/pydicom/tree/master/pydicom/fileset.py" and file_html!="https://github.com/pydicom/pydicom/tree/master/pydicom/dataset.py":
                continue
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    for ind, (for_node, assign_node, remove_ass_flag, new_tree) in enumerate(
                            complicate_code[file_html][cl][me]):
                        old_content, new_content, flag_same = c_replace_content_by_ast_5_10.replace_file_content_for_compre_3_category_insert_comehere(repo_name, file_html, for_node, assign_node, new_tree, remove_ass_flag)
                        print(file_html)
                        

                        real_file_html = file_html.replace("//", "/")
                        rela_path = real_file_html.split("/")[6:]
                        old_path = repo_path + "/".join(rela_path)
                        util.save_file_path(old_path, new_content)

                        rela_path[-1] = "".join([rela_path[-1][:-3], "_copy_zejun", ".py"])
                        print(">>>>>>>>>>new_content: ", old_content)
                        rela_path = "/".join(rela_path)
                        # print(repo_path+rela_path)
                        util.save_file_path(repo_path + rela_path, old_content)  # copy 一份原来的文件防止失去
                        try:
                            for test_html in dict_success_run_test_case:
                                if test_html!='https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_dataset.py' and test_html!="https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_fileset.py":
                                    continue
                                for cl, me in dict_success_run_test_case[test_html]:
                                    if me!="test_validate_and_correct_file_meta" and me!="test_bad_file_id":
                                        continue
                                    fun_list = ["::".join([cl, me]) if cl else me]
                                    run_test_result = configure_pro_envir_util.run_test_file_capture_output_each_fun(test_html, repo_path,
                                                                                             fun_list=fun_list,
                                                                                             export_python=True)
                                    if run_test_result == "TimeoutExpired":
                                        print(">>>>>>Time out run pytest, please check ", test_html)
                                        continue
                                    print(">>>>>>>>>>run_test_result: ", run_test_result)
                                    through_flag=configure_pro_envir_util.test_result_through_code(run_test_result)
                                    dict_me_re, flag_pass = configure_pro_envir_util.get_test_result(run_test_result)
                                    if flag_pass and through_flag:

                                        if file_html not in dict_code_map_pass_test_case:
                                            dict_code_map_pass_test_case[file_html] = dict()
                                        if cl not in dict_code_map_pass_test_case[file_html]:
                                            dict_code_map_pass_test_case[file_html][cl] = dict()
                                        if me not in dict_code_map_pass_test_case[file_html][cl]:
                                            dict_code_map_pass_test_case[file_html][cl][me] = dict()
                                        if (for_node, assign_node, remove_ass_flag, new_tree) not in dict_code_map_pass_test_case[file_html][cl][me]:
                                            dict_code_map_pass_test_case[file_html][cl][me][(for_node, assign_node, remove_ass_flag, new_tree)]=[]
                                        dict_code_map_pass_test_case[file_html][cl][me][(for_node, assign_node, remove_ass_flag, new_tree)].append([test_html,cl, me])
                                    print(">>>>>>>>>>dict_me_re: ", fun_list, dict_me_re, flag_pass,through_flag)
                                #     break
                                # break
                            util.save_file_path(old_path, old_content)
                        except:
                            util.save_file_path(old_path, old_content)

    '''
        #                 break
        #             else:
        #                 continue
        #             break
        #         else:
        #             continue
        #         break
        #     else:
        #         continue
        #     break
        #
        # else:
        #     continue
        # util.save_pkl(dict_code_map_pass_test_case_code_dir, repo_name, dict_code_map_pass_test_case)
        # dict_success_run_test_case = util.load_pkl(dict_code_map_pass_test_case_code_dir, repo_name)
        # print(dict_success_run_test_case)
        # break
    #     if flag_same:
    #         print("please check because the code1 is not changed: ", file_html)
    #         continue
    # dict_list_compreh_3215=dict()
    # evaluation_testing_dir=util.data_root +"5_10_all_test_cases/evaluation/"#test_case_benchmark_dir_csv/"#


    # print("code_info_list", code_info_list)






