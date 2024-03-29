import sys, ast, os, copy
import tokenize
import sys
sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time
import util,github_util,complicated_code_util
from extract_simp_cmpl_data import ast_util
from extract_simp_cmpl_data.extract_compli_truth_value_test_code import decide_compare_complicate_truth_value
from pathos.multiprocessing import ProcessingPool as newPool
from transform_c_s.transform_truth_value_test_compli_to_simple import transform_c_s_truth_value_test
import format_api_call

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

if __name__ == '__main__':
    # save_for_else_complicated_code_dir = util.data_root + "transform_complicate_to_simple/for_else_improve_5/"
    # save_list_compre_complicated_code_dir = util.data_root + "complicated_code_dir/for_comrephension_list_complicated_only_one_stmt/"
    # save_dict_compre_complicated_code_dir = util.data_root + "complicated_code_dir/for_comrephension_dict_complicated_only_one_stmt/"
    # save_set_compre_complicated_code_dir = util.data_root + "complicated_code_dir/for_comrephension_set_complicated_only_one_stmt/"
    # save_chained_compare_complicated_code_dir = util.data_root + "complicated_code_dir/chained_comparison_complicated/"
    # save_truth_value_test_complicated_code_dir = util.data_root + "complicated_code_dir/truth_value_test_complicated/"
    # save_call_fun_var_unpack_complicated_code_dir = util.data_root +  "complicated_code_dir/var_unpack_func_call_only_same_dengcha_subscript_complicated_pkl/"
    # save_for_multi_targets_complicated_code_dir = util.data_root + "complicated_code_dir/var_unpack_for_target_complicated/"
    # save_multi_assign_complicated_code_dir = util.data_root +  "complicated_code_dir/multip_assign_complicated_json/"
    # complica_code_dir_list = [save_for_else_complicated_code_dir, save_list_compre_complicated_code_dir,
    #                           save_dict_compre_complicated_code_dir, save_set_compre_complicated_code_dir,
    #                           save_chained_compare_complicated_code_dir,
    #                           save_for_multi_targets_complicated_code_dir,
    #                           save_call_fun_var_unpack_complicated_code_dir,
    #                           save_multi_assign_complicated_code_dir, save_truth_value_test_complicated_code_dir]
    #

    pro_dir = util.data_root + "python_star_2000repo/"
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    save_test_methods_dir =  util.data_root +"test_case/"
    '''
    pool = newPool(nodes=30)
    pool.map(save_repo, list(dict_repo_file_python.keys()) ) # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    '''
    #get intersect methods file相交的数目, 方法相交的数目
    save_for_else_complicated_code_dir = util.data_root + "transform_complicate_to_simple/for_else_improve_5/"
    save_for_else_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_else/"
    save_for_else_methods_dir = util.data_root + "methods/for_else/"

    count_repo, file_count, me_count, code_count = 0, 0, 0, 0
    all_count_repo, all_file_count, all_me_count = 0, 0, 0

    for file_name in os.listdir(save_for_else_complicated_code_dir_pkl):
        repo_name = file_name[:-4]
        dict_comp_file = dict()
        test_case_complicate_code = util.load_pkl(save_test_methods_dir, repo_name)
        # files_num_list.append(repo_files_info[repo_name])
        # star_num_list.append(repo_star_info[repo_name])
        # contributor_num_list.append(repo_contributor_info[repo_name])

        complicate_code = util.load_pkl(save_for_else_complicated_code_dir_pkl, repo_name)

        repo_file_count,repo_me_count,repo_code_count,repo_all_file_count,repo_all_me_count= complicated_code_util.get_code_count(complicate_code)

        repo_exist=0
        repo_file_count, repo_me_count, repo_code_count, repo_all_file_count, repo_all_me_count = complicated_code_util.get_code_count(
            complicate_code)
        code_count += repo_code_count
        file_count += repo_file_count
        me_count += repo_me_count
        all_file_count += repo_all_file_count
        all_me_count += repo_all_me_count
        for file_html in complicate_code:

            map_file_name=file_html.split("/")[-1][:-3]
            # filter out test files
            if map_file_name.startswith("test_") or  map_file_name.endswith("_test"):
                continue
            if map_file_name not in dict_comp_file:
                dict_comp_file[map_file_name] = dict()
            dict_class=dict()
            real_file_html=file_html.replace("//","/")
            rela_path = ".".join(real_file_html.split("/")[6:-1])
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if not complicate_code[file_html][cl][me]:
                        continue
                    repo_exist = 1
                    me_name=me.split("$")[0]
                    if me_name=="if_main_my":# it is impossible for the main code1 have test cases
                        continue
                    total_name=".".join([rela_path,map_file_name,cl,me_name])
                    total_name = total_name.replace("..", ".")
                    if total_name in dict_class:
                        print("it is possible! because the same file define two same functions", total_name,dict_class[total_name],file_html)
                        dict_class[total_name]+=dict_class[total_name]
                        #dict_class[total_name].append([len(complicate_code[file_html][cl][me]),file_html])

                    else:
                        dict_class[total_name] =len(complicate_code[file_html][cl][me])#,file_html]
                        # dict_class[total_name] =[len(complicate_code[file_html][cl][me]),file_html]


            dict_comp_file[map_file_name][file_html] = dict_class
        util.save_pkl(save_for_else_methods_dir, repo_name, dict_comp_file)
        count_repo+=repo_exist
            # complicate_code = util.load_pkl(save_for_else_complicated_code_dir_pkl, repo_name)
    print("count: ", count_repo, code_count, file_count, me_count, all_count_repo, all_file_count, all_me_count)


    dict_intersect_test_methods=dict()
    count_code=0
    count_me=0
    count_repo=0
    for repo_name in dict_repo_file_python:
        flag_repo=0

        test_case_complicate_code = util.load_pkl(save_test_methods_dir, repo_name)
        dict_comp_file = util.load_pkl(save_for_else_methods_dir, repo_name)
        for file_name in dict_comp_file:
            if file_name in test_case_complicate_code:
                # print("存在相同的文件名存在test case 需要进一步确定 多个相同的文件名时, 到底测试文件测试的是哪一个文件: ",file_name)
                for file_html in dict_comp_file[file_name]:

                    dict_me_test_me_pair= dict()#{"complica_num":0,"test_pair":[]}

                    # print("code1 file_html: ",file_html)
                    com_dict_me = dict_comp_file[file_name][file_html]
                    all_full_me_list = list(com_dict_me.keys())
                    if not all_full_me_list:
                        continue
                    # print("all code1 methods: ",all_full_me_list)
                    for test_case_html in test_case_complicate_code[file_name]:
                        # print("test case code1 file_html: ", test_case_html)
                        dict_class=test_case_complicate_code[file_name][test_case_html]
                        for cl in dict_class:
                            for me in dict_class[cl]:
                                # print("test_method: ",cl, me)
                                api_list = dict_class[cl][me]
                                # print("all apis: ", api_list)
                                # it shows whether the me is be tested by the  api_list
                                def get_intersect(all_full_me_list,api_list):
                                    intersect_methods=[]
                                    all_new_full_me_list = copy.deepcopy(all_full_me_list)
                                    for ind in range(len(all_full_me_list[0].split("."))):
                                        for ind_me,full_me in enumerate(all_new_full_me_list):
                                            if ind_me in intersect_methods:
                                                continue
                                            if full_me in api_list:
                                                intersect_methods.append(ind_me)
                                                print(">>>>>>>>>>yes intersect: ",full_me,all_full_me_list,api_list)
                                        # if intersect_methods:
                                        #     break
                                        all_new_full_me_list=[".".join(full_me.split(".")[ind]) for full_me in all_full_me_list ]
                                    return intersect_methods


                                intersect=get_intersect(all_full_me_list, api_list)


                                if intersect:#set(all_full_me_list) & set(api_list):
                                    flag_repo=1
                                    for ind in intersect:
                                        full_me=all_full_me_list[ind]

                                        if full_me in dict_me_test_me_pair:

                                            dict_me_test_me_pair[full_me]["test_pair"].append([test_case_html,cl,me])
                                        else:
                                            dict_me_test_me_pair[full_me] = dict()
                                            dict_me_test_me_pair[full_me]["complica_num"] = com_dict_me[full_me]
                                            dict_me_test_me_pair[full_me]["test_pair"] = [[test_case_html,cl,me]]
                                        # count_code+=com_dict_me[full_me]
                                        # count_me+=1

                                        print(
                                            f"method {full_me}  of {file_html} exist test case {me} in {test_case_html}")
                                        #             b
                            #         for intersect_me in set(all_full_me_list) & set(api_list):
                            #             print(
                            #                 f"method {intersect_me}  of {file_html} exist test case {me} in {test_case_html}")
                            # #             break
                            #         else:
                            #             continue
                            #         break
                            # else:
                            #     continue
                            # break
                        # else:
                        #     continue
                        # break
                    if dict_me_test_me_pair:
                        if repo_name not in dict_intersect_test_methods:
                            dict_intersect_test_methods[repo_name]=dict()
                            dict_intersect_test_methods[repo_name][file_html] = dict_me_test_me_pair
                        else:
                            dict_intersect_test_methods[repo_name][file_html] = dict_me_test_me_pair
                        # dict_intersect_test_methods[repo_name][file_html]=dict_me_test_me_pair
                    # else:
                    #     continue
                    # break
                # else:
                #     continue
                # break
        # count_repo+=flag_repo
    count_file=0
    for repo_name in dict_intersect_test_methods:
        for file_html in dict_intersect_test_methods[repo_name]:
            count_file+=1
            for full_me in dict_intersect_test_methods[repo_name][file_html]:
                count_code+=dict_intersect_test_methods[repo_name][file_html][full_me]["complica_num"]
                count_me += 1
        count_repo+=1



        # else:
        #     continue
        # break
    print("has test case number: ",count_repo, count_file,count_me,count_code)
    '''
        # complicate_code = util.load_pkl(save_for_else_complicated_code_dir_pkl, repo_name)
        for file_name in test_case_complicate_code:
            if file_name in dict_comp_file:
                for file_html in test_case_complicate_code[file_name]:
                    test_case_dict_class=test_case_complicate_code[file_name][file_html]
                    for com_file_html in dict_comp_file:
                        com_dict_me=dict_comp_file[file_name][com_file_html]
                        all_full_me_list=list(com_dict_me.keys())
                        print("all_full_me_list: ",all_full_me_list)
                        for cl in dict_class:
                            for me in dict_class[cl]:
                                api_list=dict_class[cl][me]
                                if set(all_full_me_list)&set(api_list):
                                    for intersect_me in set(all_full_me_list)&set(api_list):
                                        print(f"method {intersect_me}  of {file_html} exist test case {me} in {com_file_html}")
                                        break
                                    else:
                                        continue
                                    break
                            else:
                                continue
                            break
                        else:
                            continue
                        break
                    else:
                        continue
                    break
                else:
                    continue
                break
        else:
            continue
        break
    '''
    # for repo_name in dict_repo_file_python:
    #     if repo_name!='salt':
    #         continue
        # dict_file=dict()
        # for ind, file_info in enumerate(dict_repo_file_python[repo_name]):
        #     file_path = file_info["file_path"]
        #     file_name=file_path.split("/")[-1][:-3]
        #     map_file_name=""
        #     if file_name.startswith("test_"):
        #         map_file_name=file_name[5:]
        #     elif file_name.endswith("_test"):
        #         map_file_name = file_name[:-8]
        #     else:
        #         continue
        #
        #
        #     if map_file_name not in dict_file:
        #         dict_file[map_file_name]=dict()
        #
        #
        #     # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
        #     #     continue
        #     file_html = file_info["file_html"]
        #     print("file_html: ",file_html)
        #     # dict_file[map_file_name][file_html]=dict()
        #     try:
        #         content = util.load_file_path(file_path)
        #     except:
        #         print(f"{file_path} is not existed!")
        #         continue
        #     try:
        #         file_tree = ast.parse(content)
        #         ana_py = ast_util.Fun_Analyzer()
        #         ana_py.visit(file_tree)
        #         dict_class = dict()
        #         for tree, class_name in ana_py.func_def_list:
        #             if hasattr(tree, "name"):
        #                 me_name = tree.name
        #                 if me_name.startswith("test_") or me_name.endswith("_test"):
        #                     api_list=format_api_call.get_call(file_tree,tree)
        #                     set_dict_class_code_list(tree, dict_class, class_name, api_list)
        #         # print("dict_class: ",dict_class)
        #         dict_file[map_file_name][file_html]=dict_class
        #
        #
        #
        #     except SyntaxError:
        #         print("the file has syntax error")
        #         continue
        #     except ValueError:
        #         print("the file has value error: ", content, file_html)
        #         continue
        # util.save_pkl(save_test_methods_dir,repo_name,dict_file)
