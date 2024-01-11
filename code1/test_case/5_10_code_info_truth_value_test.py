import sys, ast, os, csv, time

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + "test_case/")
import util, get_test_case_acc_util


'''
1. reading csv to determine all code refactoring pairs
2. integrate information
'''


# deprecated
def cp_test_file_res_dir_to_for_compre_dict_all(one_test_file, another_test_file, csv_testcase, new_test_file):
    one_save_test_file_res_dir = util.data_root + "save_test_file_res_dir/" + one_test_file
    another_test_file_res_dir = util.data_root + "save_test_file_res_dir/" + another_test_file  # "for_compre_dict_own_config/"
    file_path = util.data_root + "testing/" + csv_testcase  # "for_compre_dict.csv"
    csvFile = open(file_path, "r", errors='ignore')

    reader = csv.reader(csvFile)

    # reader = csv.reader((line.replace('\0','') for line in reader), delimiter=",")
    # print(list(str(reader)))
    all_test_case_list = list(reader)
    code_info_list = {e[0] + ".pkl" for e in all_test_case_list[1:]}
    print("num of repos in benchmark of test cases: ", len(code_info_list))
    for e in code_info_list:
        dict_test_html_each_me_res = dict()
        dict_test_html_each_me_res_2 = dict()
        totalres = dict()
        if e in os.listdir(one_save_test_file_res_dir):
            dict_test_html_each_me_res = util.load_pkl(one_save_test_file_res_dir, e[:-4])
            # util.save_pkl(util.data_root+"save_test_file_res_dir/for_compre_dict_all/", e[:-4], dict_test_html_each_me_res)
        if e in os.listdir(another_test_file_res_dir):
            dict_test_html_each_me_res_2 = util.load_pkl(another_test_file_res_dir, e[:-4])
            # util.save_pkl(util.data_root + "save_test_file_res_dir/for_compre_dict_all/", e[:-4], dict_test_html_each_me_res)
        for key in dict_test_html_each_me_res:
            if key in dict_test_html_each_me_res_2:
                totalres[key] = {**dict_test_html_each_me_res_2[key], **dict_test_html_each_me_res[key]}
            else:
                totalres[key] = dict_test_html_each_me_res[key]
        for key in dict_test_html_each_me_res_2:
            if key not in dict_test_html_each_me_res:
                totalres[key] = dict_test_html_each_me_res_2[key]

        # totalres = {**dict_test_html_each_me_res, **dict_test_html_each_me_res_2}
        util.save_pkl(util.data_root + "save_test_file_res_dir/" + new_test_file, e[:-4], totalres)

    print("num of new repos after merged: ",
          len(os.listdir(util.data_root + "save_test_file_res_dir/" + new_test_file)))

    all_file_list = []
    another_file_list = []
    for file in os.listdir(one_save_test_file_res_dir):
        if file in code_info_list:
            all_file_list.append(file)
    print(f"len in {one_test_file}: ", len(all_file_list))
    print(code_info_list - set(all_file_list))
    for file in os.listdir(another_test_file_res_dir):
        if file in code_info_list:
            another_file_list.append(file)
    print(f"len in {another_test_file}: ", len(another_file_list))
    print(len(set(all_file_list) | set(another_file_list)))
    print(code_info_list - set(another_file_list))


if __name__ == '__main__':
    file_path = util.data_root + "testing/truth_value_test.csv"
    save_me_test_me_dir_list = ["truth_value_test_complicated_remove_is_is_not/"]
    save_test_file_res_dir_list = ["truth_value_test_complicated_remove_is_is_not/"]
    complicated_code_dir_pkl_list = ["truth_value_test_complicated_remove_is_is_not_no_len/"]
    save_test_acc_dir_list = ["truth_value_test_complicated_remove_len_dir/"]
    list_code_info_list = []
    code_count = 0
    csvFile = open(file_path, "r", errors='ignore')
    reader = csv.reader(csvFile)
    all_test_case_list = list(reader)
    csvFile.close()
    repo_list = {e[0] for e in all_test_case_list[1:]}
    code_info_list = ["".join([e[1], e[4]]) for e in all_test_case_list[1:]]
    print("len: ", len(code_info_list), code_info_list[0])
    code_list = []
    dict_list_compreh_3215=dict()
    for i in range(len(save_test_file_res_dir_list)):
        save_me_test_me_dir = util.data_root + "methods_test_method_pair/" + save_me_test_me_dir_list[i]
        save_test_file_res_dir = util.data_root + "save_test_file_res_dir/" + save_test_file_res_dir_list[i]
        complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/" + \
                                   complicated_code_dir_pkl_list[i]
        save_test_acc_dir = util.data_root + "test_case_benchmark_dir/" + save_test_acc_dir_list[i]
        # file_path = util.data_root + "testing/for_compre_list.csv"
        print(save_me_test_me_dir)
        print(save_test_file_res_dir)
        print(complicated_code_dir_pkl)
        print(save_test_acc_dir)
        pro_path = util.data_root + "python_star_2000repo/"
        a_file_html_list = []
        pro_time_start = time.time()
        total_num = 0
        for repo_name in repo_list:
            # repo_name = file[:-4]
            acc_code = util.load_pkl(save_test_acc_dir, repo_name)
            res = acc_code['record_res']
            if not res:
                continue
            complicate_code = util.load_pkl(complicated_code_dir_pkl, repo_name)
            dict_complica_me_list = get_test_case_acc_util.get_comp_code_can_test_me(repo_name, save_test_file_res_dir,
                                                                                     save_me_test_me_dir)
            repo_path = pro_path + repo_name + "/"
            for repo_name, file_html, *other in res:
                total_num += 1
                flag_file = 0
                if file_html in dict_complica_me_list:
                    a_file_html_list.append(file_html)
                    for cl in complicate_code[file_html]:

                        for me in complicate_code[file_html][cl]:
                            me_name = me.split("$")[0]
                            if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
                                continue
                            total_name = get_test_case_acc_util.get_total_name(file_html, cl, me_name)

                            if total_name in dict_complica_me_list[file_html]:
                                test_me_inf_list = dict_complica_me_list[file_html][total_name]
                                # print(len(test_me_inf_list))
                                if complicate_code[file_html][cl][me] and test_me_inf_list:
                                    # print("come here")

                                    for ind, (old_tree, new_tree) in enumerate(
                                            complicate_code[file_html][cl][me]):
                                        # print("cl,me,lineno: ",cl,me_name,str(assign_node.lineno))
                                        str_info = "".join([file_html, str(old_tree.lineno)])
                                        # print("str_info: ",str_info)
                                        if str_info in code_info_list:
                                            if repo_name not in dict_list_compreh_3215:
                                                dict_list_compreh_3215[repo_name] = dict()
                                            if file_html not in dict_list_compreh_3215[repo_name]:
                                                dict_list_compreh_3215[repo_name][file_html] = dict()
                                            if cl not in dict_list_compreh_3215[repo_name][file_html]:
                                                dict_list_compreh_3215[repo_name][file_html][cl] = dict()
                                            if me not in dict_list_compreh_3215[repo_name][file_html][cl]:
                                                dict_list_compreh_3215[repo_name][file_html][cl][me] = []
                                            dict_list_compreh_3215[repo_name][file_html][cl][me].append(
                                                [old_tree, new_tree])

                                            code_count += 1
                                            # code_info_cla = code_info.CodeInfo(repo_name, file_html, cl, me,
                                            #                                    [old_tree, new_tree], test_me_inf_list)
                                            #
                                            # if code_info_cla not in list_code_info_list:
                                            #     list_code_info_list.append(code_info_cla)

                                        # print("code count: ", code_count, len(list_code_info_list))
                                        #
                                        # # util.save
                                        #
                                        #     code_count += 1
                                        #     code_info_cla = code_info.CodeInfo(repo_name, file_html, cl, me,
                                        #                                        [old_tree, new_tree], test_me_inf_list)
                                        #
                                        #     if [old_tree, new_tree] not in code_list:
                                        #         list_code_info_list.append(code_info_cla)
                                        #         code_list.append([old_tree, new_tree])

        print("code count: ", code_count, len(list_code_info_list))
    evaluation_testing_dir = util.data_root + "5_10_all_test_cases/code_info_3215/truth_value_test/"  # test_case_benchmark_dir_csv/"#
    for repo_name in dict_list_compreh_3215:
            util.save_pkl(evaluation_testing_dir, repo_name,
                          dict_list_compreh_3215[repo_name])
        # util.save
        # util.save_pkl(util.data_root+"format_code_info/", "dict_compre", list_code_info_list)
        # util.save_pkl(util.data_root+"format_code_info/", "for_target", list_code_info_list)

    # '''
