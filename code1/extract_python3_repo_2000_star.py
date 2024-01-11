import sys, os

sys.path.append("/mnt/zejun/smp/code1/")
import util
'''
存储repo中file 信息
一个文件信息是 html_url, file_path, repo_name 
'''
pro_path= util.data_root + "python_star_2000repo/"

new_pro_1000_info_python_list= util.load_json(util.data_root, "python3_star_10000_repos_info")
print("len repo info: ",len(new_pro_1000_info_python_list),new_pro_1000_info_python_list[0])
dict_repo_name_html_url=dict()
for e in new_pro_1000_info_python_list:
    dict_repo_name_html_url[e["name"]]=e['html_url']
# code1="'''\nprint(1)\n'''\nprint(1)"
# normal_code=ast.unparse(ast.parse(code1))
# print("normal code1: ",normal_code)

#'''
def get_top_1000_repo_info():
    # top_1000_star_repo_info=dict()
    # new_pro_1000_info_python_list = util.load_json(util.data_root, "python3_star_2000_repos_info")
    # dict_repo_name_info=dict()
    # for e in new_pro_1000_info_python_list:
    #     dict_repo_name_info[e["name"]] = e
    # repos_sort_by_star = sorted(dict_repo_name_info.items(), key=lambda x: x[1]["stargazers_count"], reverse=True)
    # for repo_name,repo_info in repos_sort_by_star[:1000]:
    #     top_1000_star_repo_info[repo_name]=repo_info
    # util.save_json(util.data_root, "top_1000_star_repo_name_repoinfo", top_1000_star_repo_info)

    dict_top_1000_repo_file_python = dict()
    dict_repo_file_python = util.load_json(util.data_root, "python3_star_10000_repos_info")
    for repo_name in dict_repo_file_python:
        # if repo_name in top_1000_star_repo_info:
            dict_top_1000_repo_file_python[repo_name] = dict_repo_file_python[repo_name]
    print(f"top_1000_star_repo_info has {len(list(dict_top_1000_repo_file_python.keys()))} repos")
    util.save_json(util.data_root, "python3_1000repos_files_info", dict_top_1000_repo_file_python)
    pass
# get_top_1000_repo_info()
# top_1000_star_repo_info= util.load_json(util.data_root, "top_1000_star_repo_name_repoinfo")
# print("len: ",len(list(top_1000_star_repo_info.keys())))


def save_all_python3_files():

    dict_repo_file_python=dict()
    for repo_name in os.listdir(pro_path):
        # if repo_name!="matplotlib":#"pandas":
        #     continue
        # else:
        #     print("come here: ",repo_name)
        repo_html = dict_repo_name_html_url[repo_name]
        repo_path_dir = pro_path + repo_name + "/"
        flag, count = util.get_python3_repos(repo_path_dir)
        # print(flag, count)
        if flag:
            dict_repo_file_python[repo_name] = []
            for root,dirs,files in os.walk(repo_path_dir):
                #print(root)
                for file in files:
                    if file.endswith(".py") and ("__init__" in file or "setup.py" in file):
                        continue
                    if file.endswith(".py"):
                        # print("file: ",dirs,file)
                        # break
                        file_path=root+"/"+file
                        file_html =repo_html+ "/tree/master/" +"/".join(file_path.split("/")[7:])
                        dict_repo_file_python[repo_name].append({"file_path":file_path,"file_html":file_html})
            #             print("file_html: ",file_html)
            #             #     break
            #             break
            #     break
            # break
    print("number of python3 repos: ",len(list(dict_repo_file_python.keys())))
    #'''
    util.save_json(util.data_root, "python3_1000repos_files_info", dict_repo_file_python)
save_all_python3_files()
# file_html = "https://github.com/" + "/".join(
#                             file_path.split("/")[4:6]) + "/tree/master/" + "/".join(file_path.split("/")[6:])




