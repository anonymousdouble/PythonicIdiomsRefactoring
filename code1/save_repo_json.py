import os

import util
dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
pro_path = util.data_root + "python_star_2000repo/"
pro_path_2 ="/data1/zhangzejun/data/each_repo_2/each_repo/"
repo_list=list(os.listdir(pro_path))
repo_list_1=list(os.listdir(pro_path_2))
print("repo_list: ",repo_list[0],len(repo_list),len(repo_list_1),len(set(repo_list)|set(repo_list_1)))
all_repos=set(repo_list)|set(repo_list_1)
remain_repos=[]
for repo_name in dict_repo_file_python:
    if repo_name not in all_repos:
        remain_repos.append(repo_name)

    pass
print("remain repos: ",len(remain_repos))
util.save_json(util.data_root,"remain_clone",remain_repos)
