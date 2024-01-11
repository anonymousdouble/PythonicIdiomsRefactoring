import sys, os

sys.path.append("/mnt/zejun/smp/code1/")
import util
new_pro_1000_info_python_list = util.load_json(util.data_root, "python3_star_10000_repos_info")
dict_repo_name_info=dict()
for e in new_pro_1000_info_python_list:
    dict_repo_name_info[e["name"]] = e
repos_sort_by_star = sorted(dict_repo_name_info.items(), key=lambda x: x[1]["stargazers_count"], reverse=True)
res=[]
for repo_name,repo_info in repos_sort_by_star[:1000]:
    # print(repo_info)
    a=[repo_info['name'],repo_info['html_url'],
       repo_info['stargazers_count'],
       repo_info['language']]
    res.append(a)
util.save_csv(util.data_root+"top_1000_repo_name_star_url_info.csv",res,["repo_name","html_url","stargazers_count","language"])

