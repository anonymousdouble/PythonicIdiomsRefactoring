import sys,ast,os
sys.path.append("../")
sys.path.append("../..")
sys.path.append("../../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time,complicated_code_util
import util
start_time = time.time()
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_for_target_complicated/"
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_call_star_complicated/"
# save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_call_star_complicated_strict/"

save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_list/"

save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_set/"

save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_dict/"

# save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/chain_comparison/"
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_is_not_no_len/"
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_is_not_no_len/"

save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/chain_ass_same_value/"

save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/fstring/"
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/fstring_new_2/"

'''
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/with_complicated_remove_after_block_use_f/"
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_call_star_complicated/"
'''
# save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_else/"
# save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/multip_assign_complicated/"
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_else/"
'''
ave_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_is_not_no_len/"
# save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/chain_comparison/"
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/multip_assign_complicated/"
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/var_unpack_for_target_complicated/"
'''
dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
# print("num of repos: ",len(list(dict_repo_file_python.keys())))
repo_name_list=[]
repo_num_list=[]
file_num_list=[]
met_num_list=[]
file_count=0
for repo_name in dict_repo_file_python:
    if os.path.exists("/data1/zhangzejun/mnt/zejun/smp/data/python_star_2000repo/" + repo_name):
        repo_name_list.append(repo_name)
    for ind, file_info in enumerate(dict_repo_file_python[repo_name]):

        file_path = file_info["file_path"]
        file_path = util.prefix_root + "/" + file_path
        if os.path.exists(file_path):
            file_count+=1
        # print(">>>>repo: ",dict_repo_file_python[repo_name])
        # break
        # if os.path.exists("/data1/zhangzejun/mnt/zejun/smp/data/python_star_2000repo/" + repo_name):
        #     repo_name_list.append(repo_name)
        #     continue
        #     return None
        # if repo_name!="spiderfoot":
        #     continue


print("repo num: ", len(repo_name_list),file_count)
files_num_list = []
star_num_list = []
contributor_num_list = []
count_repo, file_count, me_count, code_count = 0, 0, 0, 0
file_list = set([])
repo_code_num = dict()
result_compli_for_else_list = []
all_count_repo, all_file_count, all_me_count = 0, 0, 0
for file_name in os.listdir(save_complicated_code_dir_pkl):
    all_count_repo += 1
    repo_name = file_name[:-4]
    # files_num_list.append(repo_files_info[repo_name])
    # star_num_list.append(repo_star_info[repo_name])
    # contributor_num_list.append(repo_contributor_info[repo_name])

    complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)

    repo_file_count, repo_me_count, repo_code_count, repo_all_file_count, repo_all_me_count = complicated_code_util.get_code_count(
        complicate_code)
    # for code_list, file_path, file_html in complicate_code:
    code_count += repo_code_count
    file_count += repo_file_count
    me_count += repo_me_count
    all_file_count += repo_all_file_count
    all_me_count += repo_all_me_count
    repo_exist = 0
    for file_html in complicate_code:
        for cl in complicate_code[file_html]:
            for me in complicate_code[file_html][cl]:
                if complicate_code[file_html][cl][me]:
                    repo_exist = 1
                    for code in complicate_code[file_html][cl][me]:
                        pass
                        # print("html: ",file_html,cl,me,ast.unparse(code1[0]))
                        #                code_index_start_end_list.append([node,assign_stmt,node.lineno, node.end_lineno,assign_stmt_lineno,assign_block_list_str])

                        # result_compli_for_else_list.append(
                        #     [repo_name, file_html, cl, me, ast.unparse(code1[0]), ast.unparse(code1[1])])

        # print(f"{file_html} of {repo_name} has  {len(code_list)} code1 fragments")
    count_repo += repo_exist

# a=dict(sorted(repo_code_num.items(), key=lambda item: item[1], reverse=True))
# print(a)
# print(np.median(list(a.values())), np.max(list(a.values())), np.min(list(a.values())))
# print(np.median(files_num_list), np.max(files_num_list), np.min(files_num_list))
# print(np.median(star_num_list), np.max(star_num_list), np.min(star_num_list))
# print(np.median(contributor_num_list), np.max(contributor_num_list), np.min(contributor_num_list))
print("count: ", count_repo, code_count, file_count, me_count, all_count_repo, all_file_count, all_me_count)
end_time = time.time()
print("total time: ", end_time - start_time)
'''
save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_compre_list/"
ssh://zhangzejun@115.236.22.158:9994/usr/bin/python3.9 -u /data1/zhangzejun/mnt/zejun/smp/code1/extract_transform_complicate_code_new/count_compl_count.py
num of repos:  7638
repo num:  0
count:  4752 54196 31975 47421 7638 472688 4249432
total time:  32.408362865448
'''