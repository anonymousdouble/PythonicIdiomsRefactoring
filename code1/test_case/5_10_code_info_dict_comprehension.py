import sys,ast,os,csv,time
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"test_case/")
import util,get_test_case_acc_util

'''
1. reading csv to determine all code refactoring pairs
2. integrate information
'''

#deprecated
def cp_test_file_res_dir_to_for_compre_dict_all(one_test_file,another_test_file,csv_testcase,new_test_file):
    one_save_test_file_res_dir = util.data_root + "save_test_file_res_dir/"+one_test_file
    another_test_file_res_dir = util.data_root + "save_test_file_res_dir/"+another_test_file#"for_compre_dict_own_config/"
    file_path = util.data_root + "testing/"+csv_testcase#"for_compre_dict.csv"
    csvFile = open(file_path, "r", errors='ignore')

    reader = csv.reader(csvFile)

    # reader = csv.reader((line.replace('\0','') for line in reader), delimiter=",")
    # print(list(str(reader)))
    all_test_case_list = list(reader)
    code_info_list = {e[0] + ".pkl" for e in all_test_case_list[1:]}
    print("num of repos in benchmark of test cases: ",len(code_info_list))
    for e in code_info_list:
        dict_test_html_each_me_res = dict()
        dict_test_html_each_me_res_2 = dict()
        totalres=dict()
        if e in os.listdir(one_save_test_file_res_dir):
            dict_test_html_each_me_res = util.load_pkl(one_save_test_file_res_dir, e[:-4])
            # util.save_pkl(util.data_root+"save_test_file_res_dir/for_compre_dict_all/", e[:-4], dict_test_html_each_me_res)
        if e in os.listdir(another_test_file_res_dir):
            dict_test_html_each_me_res_2 = util.load_pkl(another_test_file_res_dir, e[:-4])
            # util.save_pkl(util.data_root + "save_test_file_res_dir/for_compre_dict_all/", e[:-4], dict_test_html_each_me_res)
        for key in dict_test_html_each_me_res:
            if key in dict_test_html_each_me_res_2:
                totalres[key]={**dict_test_html_each_me_res_2[key],**dict_test_html_each_me_res[key]}
            else:
                totalres[key] =dict_test_html_each_me_res[key]
        for key in dict_test_html_each_me_res_2:
            if key not in dict_test_html_each_me_res:
                totalres[key] = dict_test_html_each_me_res_2[key]

        # totalres = {**dict_test_html_each_me_res, **dict_test_html_each_me_res_2}
        util.save_pkl(util.data_root + "save_test_file_res_dir/"+new_test_file, e[:-4], totalres)

    print("num of new repos after merged: ", len(os.listdir(util.data_root + "save_test_file_res_dir/"+new_test_file)))

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
    file_path_list=["for_compre_list.csv","for_compre_dict.csv","for_compre_dict.csv","for_compre_dict.csv","for_compre_set.csv","for_compre_set.csv","for_compre_set.csv",
                    "call_star.csv","call_star.csv","for_target.csv","for_else.csv",
                    "chain_compare.csv","truth_value_test.csv","multiple_assign.csv"]
    save_me_test_me_dir_list = ["for_compre_list/", "for_compre_dict/","for_compre_dict/","for_compre_dict/","for_compre_set/","for_compre_set/","for_compre_set/",
                                "var_unpack_call_star_complicated/","var_unpack_call_star_complicated/","var_unpack_for_target_complicated/","for_else_improve_new_modify_bugs_final/",
                                "chain_comparison/","truth_value_test_complicated_remove_is_is_not/","multip_assign_complicated/"]
    save_test_file_res_dir_list=["for_compre_list/","for_compre_dict_all/","for_compre_dict/","for_compre_dict_own_config/","for_compre_set/","for_compre_set_improve/","for_compre_set_all/"
                                 "var_unpack_call_star_complicated/","var_unpack_call_star_complicated_own_config/",
                                 "var_unpack_for_target_complicated/","var_unpack_for_target_complicated_own_config/"
                                 "for_else_improve_new_modify_bugs_final/","chain_comparison/",
                                 "truth_value_test_complicated_remove_is_is_not/","multip_assign_complicated"]
    complicated_code_dir_pkl_list=["for_compre_list/","for_compre_dict/","for_compre_dict/","for_compre_dict/","for_compre_set/","for_compre_set/","for_compre_set/",
                                   "var_unpack_call_star_complicated/","var_unpack_call_star_complicated/","var_unpack_for_target_complicated/","transform_complicate_to_simple_pkl_improve_new_modify_bugs_final/for_else/",
                                   "chain_comparison/","truth_value_test_complicated_remove_is_is_not_no_len/","multip_assign_complicated/"
                                   ]
    save_test_acc_dir_list=["for_compre_list_acc_dir/","for_compre_dict_acc_dir/","for_compre_dict_acc_dir/","for_compre_dict_acc_dir/","for_compre_set_acc_dir/","for_compre_set_acc_dir/","for_compre_set_acc_dir/",
                           "var_unpack_call_star_complicated_dir/","var_unpack_call_star_complicated_dir/","var_unpack_for_target_complicated_dir/",
                            "for_else_acc_dir/","chain_comparison_acc_dir/",
                            "truth_value_test_complicated_remove_len_dir/","multip_assign_complicated_acc_dir/"]
    '''
    save_me_test_me_dir = util.data_root + "methods_test_method_pair/for_compre_list/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/for_compre_list/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_list/"
    save_acc_res_csv_dir = util.data_root + "acc_res_compli_test_case/for_compre_list.csv"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_list_acc_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/for_compre_set/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/for_compre_set/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_set/"
    save_acc_res_csv_dir = util.data_root + "acc_res_compli_test_case/for_compre_set.csv"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_set_acc_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/for_compre_set/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/for_compre_set_improve/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_set/"
    save_acc_res_csv_dir = util.data_root + "acc_res_compli_test_case/for_compre_set.csv"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_set_acc_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/for_compre_dict/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/for_compre_dict_own_config/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_dict/"
    save_acc_res_csv_dir = util.data_root + "acc_res_compli_test_case/for_compre_dict.csv"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_dict_acc_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/for_compre_dict/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/for_compre_dict/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_dict/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_dict_acc_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/var_unpack_call_star_complicated/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/var_unpack_call_star_complicated/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_call_star_complicated/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/var_unpack_call_star_complicated_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/var_unpack_call_star_complicated/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/var_unpack_call_star_complicated_own_config/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_call_star_complicated/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/var_unpack_call_star_complicated_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/var_unpack_for_target_complicated/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/var_unpack_for_target_complicated/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_for_target_complicated/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/var_unpack_for_target_complicated_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/var_unpack_for_target_complicated/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/var_unpack_for_target_complicated_own_config//"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_for_target_complicated/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/var_unpack_for_target_complicated_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/for_else_improve_new_modify_bugs_final/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/for_else_improve_new_modify_bugs_final/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl_improve_new_modify_bugs_final/for_else/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_else_acc_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/for_else_improve_new_modify_bugs_final/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/for_else_improve_new_modify_bugs_final/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl_improve_new_modify_bugs_final/for_else/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_else_acc_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/chain_comparison/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/chain_comparison/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/chain_comparison/"
    save_acc_res_csv_dir = util.data_root + "acc_res_compli_test_case/chain_comparison.csv"
    save_test_acc_dir = util.data_root + "acc_res_compli_test_case/chain_comparison_acc_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/chain_comparison_acc_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/truth_value_test_complicated_remove_is_is_not/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/truth_value_test_complicated_remove_is_is_not/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_is_not_no_len/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/truth_value_test_complicated_remove_len_dir/"

    save_me_test_me_dir = util.data_root + "methods_test_method_pair/multip_assign_complicated/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/multip_assign_complicated/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/multip_assign_complicated/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/multip_assign_complicated_acc_dir/"
    '''



    # cp_test_file_res_dir_to_for_compre_dict_all(save_test_file_res_dir_list[4],save_test_file_res_dir_list[5],file_path_list[4],"for_compre_set_all/")
    #'''
    list_code_info_list=[]
    for i in range(len(file_path_list)):
        if i!=5:# call star
            continue
        # if i!=4 and i!=5:# set_comprehension
        #     continue
        # if i!=2 and i!=3:# dict_comprehension
        #     continue
        file_path=util.data_root + "testing/"+file_path_list[i]
        save_me_test_me_dir=util.data_root + "methods_test_method_pair/"+save_me_test_me_dir_list[i]
        save_test_file_res_dir=util.data_root + "save_test_file_res_dir/"+save_test_file_res_dir_list[i]
        complicated_code_dir_pkl=util.data_root +  "transform_complicate_to_simple_pkl/"+complicated_code_dir_pkl_list[i]
        save_test_acc_dir=util.data_root + "test_case_benchmark_dir/"+save_test_acc_dir_list[i]
    # file_path = util.data_root + "testing/for_compre_list.csv"
        csvFile = open(file_path, "r", errors='ignore')

        reader = csv.reader(csvFile)

        # reader = csv.reader((line.replace('\0','') for line in reader), delimiter=",")
        # print(list(str(reader)))
        all_test_case_list = list(reader)
        code_info_list = ["".join([e[1],e[4]]) for e in all_test_case_list[1:]]
        print("len: ",len(code_info_list),code_info_list[0])
        print("code_info_list",code_info_list)
        # save_me_test_me_dir = util.data_root + "methods_test_method_pair/for_compre_list/"
        # save_test_file_res_dir = util.data_root + "save_test_file_res_dir/for_compre_list/"
        # complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_list/"
        # save_acc_res_csv_dir = util.data_root + "acc_res_compli_test_case/for_compre_list.csv"
        # save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_list_acc_dir/"
        pro_path = util.data_root + "python_star_2000repo/"
        code_count=0
        # list_code_info_list=[]
        dict_list_compreh_3215 = dict()

        a_file_html_list = []
        pro_time_start = time.time()

        for file in os.listdir(save_test_acc_dir):
            repo_name = file[:-4]
            acc_code = util.load_pkl(save_test_acc_dir, repo_name)
            res = acc_code['record_res']
            if not res:
                continue
            complicate_code = util.load_pkl(complicated_code_dir_pkl, repo_name)
            dict_complica_me_list = get_test_case_acc_util.get_comp_code_can_test_me(repo_name, save_test_file_res_dir,
                                                                                     save_me_test_me_dir)
            repo_path = pro_path + repo_name + "/"
            for repo_name, file_html, *other in res:

                flag_file = 0
                if file_html in dict_complica_me_list and file_html not in a_file_html_list:
                    a_file_html_list.append(file_html)
                    # if file_html == "https://github.com/makepath/xarray-spatial/tree/master/xrspatial/local.py":# or file_html == "https://github.com/kellyjonbrazil/jc/tree/master/jc/parsers/csv_s.py":
                    #     continue
                    # if file_html!="https://github.com/Blockstream/satellite/tree/master/blocksatcli/api/pkt.py":#"https://github.com/sympy/sympy/tree/master/sympy/vector/functions.py":#
                    #     continue
                    # print("**********************************come the file_html: ", file_html,
                    #       " **********************************")
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
                                    for ind, (for_node, assign_node, remove_ass_flag, new_tree) in enumerate(
                                            complicate_code[file_html][cl][me]):
                                        # print("cl,me,lineno: ",cl,me_name,str(assign_node.lineno))
                                        str_info="".join([file_html,str(assign_node.lineno)])
                                        # print("str_info: ",str_info)
                                        real_file_html = file_html.replace("//", "/")
                                        rela_path = "/".join(real_file_html.split("/")[6:])
                                        file_path = "".join(
                                            [util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
                                        content = util.load_file_path(file_path)
                                        # print("content: ",content)
                                        if str_info in code_info_list:
                                            code_count+=1
                                            if repo_name not in dict_list_compreh_3215:
                                                dict_list_compreh_3215[repo_name] = dict()
                                            if file_html not in dict_list_compreh_3215[repo_name]:
                                                dict_list_compreh_3215[repo_name][file_html] = dict()
                                            if cl not in dict_list_compreh_3215[repo_name][file_html]:
                                                dict_list_compreh_3215[repo_name][file_html][cl] = dict()
                                            if me not in dict_list_compreh_3215[repo_name][file_html][cl]:
                                                dict_list_compreh_3215[repo_name][file_html][cl][me] = []
                                            dict_list_compreh_3215[repo_name][file_html][cl][me].append(
                                                [for_node, assign_node, remove_ass_flag, new_tree])
                                            # count += 1
                                            # code_info_cla=code_info.CodeInfo(repo_name,file_html,cl,me,[for_node, assign_node, remove_ass_flag, new_tree], test_me_inf_list,content)
                                            # if i==2 or i==4:
                                            #     code_info_cla.own_config=0
                                            # elif i==3 or i==5:
                                            #     code_info_cla.own_config = 1
                                            list_code_info_list.append(str_info)
            # break
        print("code count: ",code_count,len(list_code_info_list))
        # util.save
        evaluation_testing_dir = util.data_root + "5_10_all_test_cases/code_info_3215/set_compreh_own_config/"#set_compreh  # test_case_benchmark_dir_csv/"#
        for repo_name in dict_list_compreh_3215:
            util.save_pkl(evaluation_testing_dir, repo_name, dict_list_compreh_3215[repo_name])

        # util.save_pkl(util.data_root+"format_code_info/", "dict_compre", list_code_info_list)
        # util.save_pkl(util.data_root+"format_code_info/", "set_compre", list_code_info_list)

    #'''
