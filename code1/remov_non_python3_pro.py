import sys, os,shutil
import traceback

sys.path.append("/mnt/zejun/smp/code1/")
import util
new_pro_1000_info_python_list= util.load_json(util.data_root, "python3_star_10000_repos_info")
print("num of python3: ",len(new_pro_1000_info_python_list))
dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
print("num of python3: ",len(list(dict_repo_file_python.keys())))

dict_repo_name_info=dict()
for e in new_pro_1000_info_python_list:
        dict_repo_name_info[e["name"]] = e
repos_sort_by_star = sorted(dict_repo_name_info.items(), key=lambda x: x[1]["stargazers_count"])
print("num of python3: ",len(repos_sort_by_star),repos_sort_by_star[0])
pro_path= util.data_root + "python_star_2000repo/"

remove_pro_infor=[]
count=0
for repo_name,info in repos_sort_by_star:
    try:
        if repo_name not in dict_repo_file_python:
            if count>=3200:
                break
            print("repo_name: ",repo_name,pro_path+repo_name)
            remove_pro_infor.append(info)
            if os.path.exists(pro_path+repo_name):
                shutil.rmtree(pro_path+repo_name)  # Removes all the subdirectories!
                print("has removed the repo ",repo_name)
            count+=1
            # break
    except:
        traceback.print_exc(repo_name,info)
        continue
print(len(remove_pro_infor))
# util.save_pkl(util.data_root,"remove_non_python3_pro_inf",remove_pro_infor)
# util.save_pkl(util.data_root,"remove_non_python3_pro_inf_add_200",remove_pro_infor)
# util.save_pkl(util.data_root,"remove_non_python3_pro_inf_add_400",remove_pro_infor)
# util.save_pkl(util.data_root,"remove_non_python3_pro_inf_add_2600",remove_pro_infor)
util.save_pkl(util.data_root,"remove_non_python3_pro_inf_add_3000",remove_pro_infor)




