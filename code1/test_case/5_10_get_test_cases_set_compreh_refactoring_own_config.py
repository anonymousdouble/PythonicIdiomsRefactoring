
import sys, ast, os, copy
import tokenize
import sys,shutil

sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/test_case")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time,shutil
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
def refactor_result():
    res = []
    for file_name in os.listdir(complicate_code_dir)[:]:

        repo_name = file_name[:-4]
        # repo_name="pydicom"
        repo_path = pro_path + repo_name + "/"
        # dict_success_run_test_case = util.load_pkl(save_test_methods_dir_success, repo_name)
        dict_code_map_pass_test_case = util.load_pkl(dict_code_map_pass_test_case_code_dir, repo_name)
        # complicate_code = util.load_pkl(complicate_code_dir, repo_name)
        for file_html in dict_code_map_pass_test_case:
            # if file_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/fileset.py" and file_html != "https://github.com/pydicom/pydicom/tree/master/pydicom/dataset.py":
            #     continue
            for code_cl in dict_code_map_pass_test_case[file_html]:
                for code_me in dict_code_map_pass_test_case[file_html][code_cl]:
                    for code_node in dict_code_map_pass_test_case[file_html][code_cl][code_me]:
                        for_node, assign_node, remove_ass_flag, new_tree = code_node
                        old_content, new_content, flag_same = c_replace_content_by_ast_5_10.replace_file_content_for_compre_3_category(
                            repo_name, file_html, for_node, assign_node, new_tree, remove_ass_flag)
                        print(file_html)
                        real_file_html = file_html.replace("//", "/")
                        rela_path = real_file_html.split("/")[6:]
                        old_path = repo_path + "/".join(rela_path)
                        shutil.copyfile(old_path, old_path[:-3] + "_copy_copy_zejun.py")
                        util.save_file_path(old_path, new_content)
                        rela_path[-1] = "".join([rela_path[-1][:-3], "_copy_zejun", ".py"])
                        # print(">>>>>>>>>>new_content: ", new_content)
                        rela_path = "/".join(rela_path)
                        # print(repo_path+rela_path)
                        util.save_file_path(repo_path + rela_path, old_content)  # copy 一份原来的文件防止失去
                        try:
                            for test_html, cl, me in dict_code_map_pass_test_case[file_html][code_cl][code_me][
                                code_node]:
                                fun_list = ["::".join([cl, me]) if cl else me]
                                run_test_result = configure_pro_envir_util.run_test_file(test_html, repo_path,
                                                                                         ven_name="venv_zejun_config",
                                                                                         fun_list=fun_list,
                                                                                         export_python=True)

                                if run_test_result == "TimeoutExpired":
                                    print(">>>>>>Time out run pytest, please check ", test_html)
                                    break
                                # print(">>>>>>>>>>run_test_result: ", run_test_result)
                                dict_me_re, flag_pass = configure_pro_envir_util.get_test_result(run_test_result)

                                print(">>>>>>>>>>dict_me_re: ", fun_list, dict_me_re, flag_pass)

                                if not flag_pass:
                                    res.append(
                                        [repo_name, file_html, code_cl, code_me, assign_node.lineno,
                                         ast.unparse(assign_node) + "\n" + ast.unparse(for_node),
                                         ast.unparse(new_tree), remove_ass_flag, 0,
                                         dict_code_map_pass_test_case[file_html][code_cl][code_me][code_node]])
                                    break
                            else:
                                res.append(
                                    [repo_name, file_html, code_cl, code_me, assign_node.lineno,
                                     ast.unparse(assign_node) + "\n" + ast.unparse(for_node),
                                     ast.unparse(new_tree), remove_ass_flag, 1,
                                     dict_code_map_pass_test_case[file_html][code_cl][code_me][
                                         code_node]])  # print(repo_path + rela_path)
                                # break
                            util.save_file_path(old_path, old_content)
                        except:
                            util.save_file_path(old_path, old_content)
            # break
    print(res)
    util.save_pkl(result_3215_test_case_dir, "set_compreh_own_config", res)
if __name__ == '__main__':
    pro_dir = util.data_root + "python_star_2000repo/"
    pro_path = util.data_root + "python_star_2000repo/"
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    evaluation_testing_dir=util.data_root +"5_10_all_test_cases/evaluation/"#test_case_benchmark_dir_csv/"#

    save_test_methods_dir_success = util.data_root + "5_10_all_test_cases/success_test_cases_own_config/"
    complicate_code_dir = util.data_root + "5_10_all_test_cases/code_info_3215/set_compreh_own_config/"
    dict_code_map_pass_test_case_code_dir=util.data_root + "5_10_all_test_cases/map_code_info_test_case/set_compreh_own_config/"
    result_3215_test_case_dir=util.data_root + "5_10_all_test_cases/refactor_result_test_case/set_compreh_own_config/"
    result_3215_test_case_dir=util.data_root + "5_10_all_test_cases/refactor_result_test_case/"

    dict_success_run_test_case = util.load_pkl(result_3215_test_case_dir, "set_compreh_own_config")
    acc_count=0
    total_count=0
    for e in dict_success_run_test_case:
        acc_count+=e[-2]
        total_count+=1
    print("refactoring result: ",total_count,acc_count)

    #     if flag_same:
    #         print("please check because the code1 is not changed: ", file_html)
    #         continue
    # dict_list_compreh_3215=dict()
    # evaluation_testing_dir=util.data_root +"5_10_all_test_cases/evaluation/"#test_case_benchmark_dir_csv/"#


    # print("code_info_list", code_info_list)






