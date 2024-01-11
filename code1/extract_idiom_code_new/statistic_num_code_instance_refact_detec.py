import os,sys
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
import util
save_complicated_code_feature_dir_pkl=util.data_root +"idiom_code_dir_star_1000_csv/"
dict_list_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "list_comprehension_idiom_code_shuffle")
dict_set_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "set_comprehension_idiom_code_shuffle")
dict_dict_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "dict_comprehension_idiom_code_shuffle")
dict_chain_compare=util.load_pkl(save_complicated_code_feature_dir_pkl, "chain_compare_idiom_code_shuffle")
dict_truth_test=util.load_pkl(save_complicated_code_feature_dir_pkl, "truth_value_test_idiom_code")
dict_star=util.load_pkl(save_complicated_code_feature_dir_pkl, "star_call_idiom_code_many_circumstances_cannot_explain")
dict_loop_else=util.load_pkl(save_complicated_code_feature_dir_pkl, "for_else_idiom_code_shuffle")
# util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_targets_object", dict_tar_type)
#     util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object", dict_value_type)

dict_ass_multi_tar_value=util.load_pkl(save_complicated_code_feature_dir_pkl, "multi_assign_idiom_code_shuffle")
dict_for_multi_tar=util.load_pkl(save_complicated_code_feature_dir_pkl, "for_multi_tar_idiom_code_shuffle")

total_num=len(dict_list_compre)+len(dict_set_compre)+len(dict_dict_compre)+len(dict_chain_compare)+\
    len(dict_truth_test)+len(dict_star)+len(dict_loop_else)+len(dict_ass_multi_tar_value)+\
    len(dict_for_multi_tar)+len(dict_loop_else)

print("number of refactorings: ",total_num)
result=[dict_list_compre,dict_set_compre,dict_dict_compre,dict_chain_compare,
    dict_truth_test,dict_star,dict_loop_else,dict_ass_multi_tar_value,
    dict_for_multi_tar]
save_complicated_code_feature_dir_pkl = util.data_root + "rq_1/"

repos=util.load_pkl(save_complicated_code_feature_dir_pkl, "repos_for_multi" )
file_html=util.load_pkl(save_complicated_code_feature_dir_pkl, "files_for_multi" )
total_repo_list=set([])
total_file_list=set([])
total_num=0
for ind_idiom,idiom_result in enumerate(result[:-1]):
    repo_list=set([])
    file_list=set([])
    for e in idiom_result:
        repo=e[0]
        repo_list.add(repo)
        file=e[1]
        file_list.add(file)
    code_num=len(idiom_result)
    total_num+=code_num
    total_repo_list=total_repo_list|repo_list
    total_file_list=total_file_list|file_list
    print("ind: repo, file, code: ",ind_idiom, len(repo_list),len(file_list),code_num)
print("total_repo_list,total_file_list,total_code: ",len(total_repo_list),len(total_file_list),total_num)
    # print("ind_idiom, each item: ",ind_idiom,idiom_result[0])

total_repo_list=total_repo_list|set(repos)
total_file_list=total_file_list|set(file_html)
print("for_multi: ",len(set(repos)),len(set(file_html)),len(repos))
print("total_repo_list,total_file_list,total_code: ",len(total_repo_list),len(total_file_list),total_num+len(repos))
