import sys,ast,os
sys.path.append("../")
sys.path.append("../..")
sys.path.append("../../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time,complicated_code_util
import util
dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
save_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl/for_else_idiom_code_fragments/"

count_repo=0
file_count=0
for repo_name in dict_repo_file_python:
    file_path=util.prefix_root+"/mnt/zejun/smp/data/python_star_2000repo/"
    if os.path.exists(file_path + repo_name):
        count_repo += 1
    for file_info in dict_repo_file_python[repo_name]:
        file_path = file_info["file_path"]
        # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
        #     continue
        file_html = file_info["file_html"]
        file_path = util.prefix_root + "/" + file_path

        try:
            content = util.load_file_path(file_path)
            file_count+=1
        except:
            print(f"{file_path} is not existed!")
            continue


        #     return None
        # if repo_name!="spiderfoot":
        #     continue
        # repo_name_list.append(repo_name)
print(">>>>count_repo: ",count_repo,file_count)
        # if os.path.exists(save_complicated_code_dir_pkl + repo_name + ".pkl"):
        #
        #     continue
        # for file_info in dict_repo_file_python[repo_name]:
        #     file_path = file_info["file_path"]
        #     print(">>>>file_path: ",file_path)
        #     break
        # break
        #     return None
        # if repo_name!="spiderfoot":
        #     continue
        # repo_name_list.append(repo_name)