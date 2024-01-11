
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
if __name__ == '__main__':

    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_set_acc_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/var_unpack_call_star_complicated_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/var_unpack_for_target_complicated_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_dict_acc_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_list_acc_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/chain_comparison_acc_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/multip_assign_complicated_acc_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/truth_value_test_complicated_remove_is_is_not_acc_dir_copy/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_else_acc_dir/"
    save_test_acc_dir = util.data_root + "test_case_benchmark_dir/truth_value_test_complicated_remove_len_dir/"

    # save_test_acc_dir = util.data_root + "acc_res_compli_test_case/for_compre_list_acc_dir/"
    #
    # #save_test_case_benchmark_dir
    # save_test_acc_dir = util.data_root + "test_case_benchmark_dir/for_compre_dict_acc_dir/"
    save_test_case_benchmark_dir=util.data_root + "test_case_benchmark_dir_csv/"
    result_csv=[]

    '''
    for file in os.listdir(save_test_acc_dir):
        repo_name = file[:-4]
        complicate_code = util.load_pkl(save_test_acc_dir, repo_name)
        res=complicate_code['record_res']
        result_csv.extend(res)
    '''



    save_test_acc_dir_list=[util.data_root + "test_case_benchmark_dir/for_compre_set_acc_dir/",
                            util.data_root + "test_case_benchmark_dir/var_unpack_call_star_complicated_dir/",
                            util.data_root + "test_case_benchmark_dir/var_unpack_for_target_complicated_dir/",
                            util.data_root + "test_case_benchmark_dir/for_compre_dict_acc_dir/",
                            util.data_root + "test_case_benchmark_dir/for_compre_list_acc_dir/",
                            util.data_root + "test_case_benchmark_dir/chain_comparison_acc_dir/",
                            util.data_root + "test_case_benchmark_dir/multip_assign_complicated_acc_dir/",

                            util.data_root + "test_case_benchmark_dir/for_else_acc_dir/",
                            util.data_root + "test_case_benchmark_dir/truth_value_test_complicated_remove_len_dir/" ]
    repos = set([])
    all_test_case_list=set([])
    all_many_test_case_list=[]
    filter_for_target = [
        "https://github.com/flennerhag/mlens/tree/master/mlens/config.py" + "test_check_cache" + "227",
        "https://github.com/coursera-dl/coursera-dl/tree/master/coursera/filtering.py" + "test_collect_all_resources" + "107",
        "https://github.com/novoid/Memacs/tree/master/memacs/lib/mailparser.py" + "TestMailParser" + "test_parse_mail_without_body" + "94"]
    fileter_star_call = [
        "https://github.com/NaturalHistoryMuseum/pyzbar/tree/master/pyzbar/locations.py" + "TestLocations" + "test_convex_square" + "53",
        "https://github.com/flennerhag/mlens/tree/master/mlens/utils/id_train.py" + "test_id_train" + "94"]
    filter_chain_compare = ["https://github.com/PyCQA/pydocstyle/tree/master/src/pydocstyle/checker.py",
                            "https://github.com/Diaoul/subliminal/tree/master/subliminal/refiners/tvdb.py"]
    filter_multi_ass = [
        "https://github.com/Erotemic/ubelt/tree/master/ubelt/util_hash.py" + "test_numpy_object_array" + "1022",
        "https://github.com/JinnLynn/genpac/tree/master/tests/util.py" + "test_config_env" + "43",
        "https://github.com/JinnLynn/genpac/tree/master/tests/util.py" + "test_config_env" + "32",
        "https://github.com/cloud-custodian/cloud-custodian/tree/master/c7n/schema.py" + "SchemaTest" + "test_element_resolve" + "531",
        "https://github.com/cloud-custodian/cloud-custodian/tree/master/c7n/schema.py" + "SchemaTest" + "test_element_resolve" + "540",
        "https://github.com/EducationalTestingService/skll/tree/master/tests/utils.py" + "test_config_parsing_automatic_output_directory_creation" + "159",
        "https://github.com/Diaoul/subliminal/tree/master/subliminal/refiners/tvdb.py" + "test_refine_episode_no_year" + "355",
        "https://github.com/Diaoul/subliminal/tree/master/subliminal/refiners/tvdb.py" + "test_refine_episode_no_year" + "370",
        "https://github.com/Diaoul/subliminal/tree/master/subliminal/refiners/tvdb.py" + "test_refine_episode_no_year" + "284",
        "https://github.com/Diaoul/subliminal/tree/master/subliminal/refiners/tvdb.py" + "test_refine_episode_no_year" + "291",
        "https://github.com/Neuraxio/Neuraxle/tree/master/examples/sklearn/plot_boston_housing_regression_with_model_stacking.py" + "test_auto_ml_value_caching" + "75"]

    for ind_idiom,save_test_acc_dir in enumerate(save_test_acc_dir_list[:]):
        test_case_list = set([])
        many_test_case_list=[]
        result_csv = []
        for file in os.listdir(save_test_acc_dir):
            repo_name = file[:-4]
            complicate_code = util.load_pkl(save_test_acc_dir, repo_name)
            res=complicate_code['record_res']
            result_csv.extend(res)
            for code_test_cases in res:
                # print("".join(code_test_cases[1:4])+str(code_test_cases[4]))
                # break
                if ind_idiom==1 and "".join(code_test_cases[1:4])+str(code_test_cases[4]) in fileter_star_call:
                    print("come fileter_star_call")
                    continue
                    pass
                elif ind_idiom == 2 and "".join(code_test_cases[1:4]) + str(code_test_cases[4]) in filter_for_target:
                    print("come filter_for_target")
                    continue
                    pass
                elif ind_idiom == 5 and "".join(code_test_cases[1:4]) + str(code_test_cases[4]) in filter_chain_compare:
                    print("come filter_for_target")
                    continue
                    pass
                elif ind_idiom == 6 and "".join(code_test_cases[1:4]) + str(code_test_cases[4]) in filter_multi_ass:
                    print("come filter_for_target")
                    continue
                    pass
                test_case_list |= {"".join(e) for e in code_test_cases[-1]}
                many_test_case_list+=["".join(e) for e in code_test_cases[-1]]
            for e in res:
                repos.add(e[0])
    # print(result_csv[0])
        print(len(result_csv))
        print("number of test_cases: ",len(result_csv),len(test_case_list),list(test_case_list)[0])
        all_test_case_list|=test_case_list
        all_many_test_case_list+=many_test_case_list
    print("total number of test_cases: ",  len(all_test_case_list),len(all_many_test_case_list))
    dcit_test_me_map_num=dict()
    for e in all_many_test_case_list:
        if e not in dcit_test_me_map_num:
            dcit_test_me_map_num[e]=0
        dcit_test_me_map_num[e]+=1
    count=0
    values=[]
    for key in dcit_test_me_map_num:
        if dcit_test_me_map_num[key]>1:
            count+=1
        values.append(dcit_test_me_map_num[key])
    print("count: ",count,max(values))




    # util.save_csv(save_test_case_benchmark_dir+"for_compre_set.csv",
    #                   result_csv,
    #                   ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code","remove_ass_flag",'success','test_case_info'])
    #
    # util.save_csv(save_test_case_benchmark_dir+"call_star.csv",
    #                   result_csv,
    #                   ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code",'success','test_case_info'])
    #
    # util.save_csv(save_test_case_benchmark_dir+"for_compre_dict.csv",
    #                   result_csv,
    #                   ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code","remove_ass_flag",'success','test_case_info'])
    #
    # util.save_csv(save_test_case_benchmark_dir+"for_compre_list.csv",
    #                   result_csv,
    #                   ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code","remove_ass_flag",'success','test_case_info'])

    # util.save_csv(save_test_case_benchmark_dir+"chain_compare.csv",
    #               result_csv,
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code",
    #               'success','test_case_info'])
    # util.save_csv(save_test_case_benchmark_dir+ "multiple_assign.csv",
    #               result_csv,
    #               ["repo_name", "file_html", "class_name", "me_name","line_no", "old_code", "new_code",
    #                'success','test_case_info'])
    # util.save_csv(save_test_case_benchmark_dir+ "truth_value_test_remove_len.csv",
    #               result_csv,
    #               ["repo_name", "file_html", "class_name", "me_name","line_no", "old_code", "new_code",
    #                'success','test_case_info'])

    # util.save_csv(save_test_case_benchmark_dir + "for_else.csv",
    #               result_csv,
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code","init_ass_remove_flag",
    #                'success', 'test_case_info'])

   # util.save_csv(save_test_case_benchmark_dir+"for_compre_dict.csv",
    #                   result_csv,
    #                   ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code","remove_ass_flag",'success','test_case_info'])
    # util.save_csv(save_test_case_benchmark_dir+"for_compre_list.csv",
    #                   result_csv,
    #                   ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code","remove_ass_flag",'success','test_case_info'])
    # util.save_csv(save_test_case_benchmark_dir+"var_unpack_call_star_complicated.csv", result_csv,
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code",'success','test_case_info'])
    # util.save_csv(save_test_case_benchmark_dir+"var_unpack_for_target_complicated.csv",
    #               result_csv,
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code"
    #                   ,'success','test_case_info'])
    # util.save_csv(save_test_case_benchmark_dir+ "for_else.csv",
    #               result_csv,
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code"
    #                   ,'success','test_case_info'])
    #

    #
    # util.save_csv(save_test_case_benchmark_dir+"truth_value_test.csv", result_csv,
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code",
    #                'success','test_case_info'])




