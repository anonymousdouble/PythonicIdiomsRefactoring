
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
    for repo_name in dict_test_case_inf:
        for file_html in dict_test_case_inf[repo_name]:
            count_test_case+=len(dict_test_case_inf[repo_name][file_html])
            count_test_file+=1
    print("count_test_case,count_test_file: ",count_test_case,count_test_file)

def save_code_map_test_cases(repo_name):
    # repo_name = file_name[:-4]
    # repo_name = "pydicom"
    #repo_name = file_html.split("/")[]
    repo_path = pro_path + repo_name + "/"
    dict_success_run_test_case = util.load_pkl(save_test_methods_dir_success_own_config, repo_name)
    complicate_code = util.load_pkl(complicate_code_dir, repo_name)
    dict_code_map_pass_test_case = dict()
    for file_html in complicate_code:
        # if file_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/fileset.py" and file_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/dataset.py":
        #     continue
        print(file_html)
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
                    # util.save_file_path(old_path, new_content)
                    print(">>>>>>>>>>old_content: ", old_content)
                    rela_path[-1] = "".join([rela_path[-1][:-3], "_copy_zejun", ".py"])
                    print(">>>>>>>>>>new_content: ", new_content)
                    rela_path = "/".join(rela_path)
                    # print(repo_path+rela_path)
                    util.save_file_path(repo_path + rela_path, old_content)  # copy 一份原来的文件防止失去
                    try:
                        for test_html in dict_success_run_test_case:
                            # if test_html != 'https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_dataset.py' and test_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/tests/test_fileset.py":
                            #     continue
                            for cl, me in dict_success_run_test_case[test_html]:
                                # if me != "test_validate_and_correct_file_meta" and me != "test_bad_file_id":
                                #     continue
                                fun_list = ["::".join([cl, me]) if cl else me]
                                run_test_result = configure_pro_envir_util.run_test_file_capture_output_each_fun(
                                    test_html, repo_path,ven_name="venv_zejun_config",
                                    fun_list=fun_list,
                                    export_python=True)
                                # run_test_result = configure_pro_envir_util.run_test_file_capture_output_each_fun(
                                #     test_html, repo_path,
                                #     fun_list=fun_list)
                                if run_test_result == "TimeoutExpired":
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
                    break
        break
    # util.save_pkl(dict_code_map_pass_test_case_code_dir, repo_name, dict_code_map_pass_test_case)
    print("save successufully")
    # dict_success_run_test_case = util.load_pkl(dict_code_map_pass_test_case_code_dir, repo_name)
    # print(dict_success_run_test_case)
def get_repo_name_list_one_idiom():
    repo_name_list = []
    one_repo_name_list = []
    own_config_repo_name_list = []
    unique_repo_name_list = set([])
    code_list = []
    for ind, file in enumerate(set_compre_dir_list):
        print(">>file: ",file)
        for repo in os.listdir(code_info_dir + file):

            repo_name = repo[:-4]
            if "config" in file:
                own_config_repo_name_list.append(repo_name)
            else:
                one_repo_name_list.append(repo_name)
            repo_name_list.append(repo_name)
            unique_repo_name_list.add(repo_name)
            dict_test_case_inf = util.load_pkl(code_info_dir + file + "/", repo[:-4])
            for file_html in dict_test_case_inf:
                for cl in dict_test_case_inf[file_html]:
                    for me in dict_test_case_inf[file_html][cl]:
                        for code in dict_test_case_inf[file_html][cl][me]:
                            code_list.append(tuple(code))
    print("repo num: ", len(repo_name_list), len(set(repo_name_list)), "code num: ", len(code_list),
          len(set(code_list)))
    return one_repo_name_list,own_config_repo_name_list
def get_code_map_test_case_info():
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
if __name__ == '__main__':
    pro_dir = util.data_root + "python_star_2000repo/"
    pro_path = util.data_root + "python_star_2000repo/"
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    evaluation_testing_dir=util.data_root +"5_10_all_test_cases/evaluation/"#test_case_benchmark_dir_csv/"#
    code_info_dir = util.data_root + "5_10_all_test_cases/code_info_3215/"  # set_compreh  # test_case_benchmark_dir_csv/"#
    save_test_methods_dir_success = util.data_root + "5_10_all_test_cases/success_test_cases_own_config/"
    save_test_methods_dir_success_own_config = util.data_root + "5_10_all_test_cases/success_test_cases_own_config/"
    complicate_code_dir = util.data_root + "5_10_all_test_cases/code_info_3215/set_compreh_own_config/"
    dict_code_map_pass_test_case_code_dir=util.data_root + "5_10_all_test_cases/map_code_info_test_case/set_compreh_own_config/"
    set_compre_dir_list=["set_compreh","set_compreh_own_config"]
    repo_name_list = [file[:-4] for file in os.listdir(complicate_code_dir)]
    one_repo_name_list, own_config_repo_name_list=get_repo_name_list_one_idiom()
    print(own_config_repo_name_list)
    code_num=0
    total_test_cases = 0
    success_run_test_cases = 0
    repo_num = 0
    start = time.time()
    save_test_methods_dir_simplify = util.data_root + "5_10_all_test_cases/"
    dict_test_case_inf = util.load_pkl(save_test_methods_dir_simplify, "all_test_case")
    for file_name in os.listdir(save_test_methods_dir_success_own_config):
        repo_name = file_name[:-4]
        if repo_name not in repo_name_list:
            continue
        code_infor_dict = util.load_pkl(complicate_code_dir, repo_name)
        for file_html in code_infor_dict:
            for cl in code_infor_dict[file_html]:
                for me in code_infor_dict[file_html][cl]:
                    if repo_name=="sympy":
                        print("file_html: ", file_html,code_infor_dict[file_html][cl][me])
                    code_num+=len(code_infor_dict[file_html][cl][me])
        repo_num += 1

        dict_success_run_test_case = util.load_pkl(save_test_methods_dir_success_own_config, repo_name)
        for test_html in dict_success_run_test_case:
            success_run_test_cases += len(dict_success_run_test_case[test_html])
        if repo_name in dict_test_case_inf:
            for file_html in dict_test_case_inf[repo_name]:
                total_test_cases += len(dict_test_case_inf[repo_name][file_html])

    print("total success run test cases: ", repo_num, code_num,total_test_cases, success_run_test_cases)
    print("own_config_independent: ",len(set(own_config_repo_name_list)-set(one_repo_name_list)),len(set(own_config_repo_name_list)))
    '''
    own_config_repo_name_list=["sympy"]
    pool = newPool(nodes=30)
    pool.map(save_code_map_test_cases, own_config_repo_name_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    '''
    get_code_map_test_case_info()
    print("total time: ", time.time() - start)
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






