import sys

sys.path.append("/mnt/zejun/smp/code1/")
import util,github_util
import time
# from code1  import util
# from code1.github_util import clone_pro
start=time.time()

# pro_path= util.data_root + "python_star_10000repo/"
pro_path = util.data_root + "python_star_2000repo/"

# pro_path=util.data_root+"jupyter_1000repo/"
data_dir = util.data_root#/data/zzj/extractAPI/data/"
#pro_info_python_list=util.load_json(data_dir,"all_crawl_python_pros")
#pro_info_python_list=util.load_json(data_dir,"python3_star_10_repos_info")
# pro_info_python_list= util.load_json(data_dir, "python3_star_10000_repos_info")
# pro_info_python_list=util.load_json(data_dir,"jupyter_star_1000_repos_info")
dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
repo_name_list = []
count = 0
exist_count = 0
repo_list = []
for repo_name in dict_repo_file_python:
    file_html=dict_repo_file_python[repo_name][0]['file_html']
    url=file_html.split("/")[:5]
    url="/".join(url)
    print("repo_name: ",repo_name,url)
    url="https://github.com/kholia/OSX-KVM"
    # count+=1
    # break
    # count = 0
    # exist_count = 0
    # repo_list = []
    # for repo_info in pro_info_python_list[:10000]:
    #     url = repo_info['html_url']
    clone_flag, repo_name = github_util.clone_pro(pro_path, url)
    if repo_name in repo_list:
        print(f"{repo_name} is existed", url)
    repo_list.append(repo_name)

    if clone_flag == 1:
        count += 1
    elif clone_flag == 2:
        exist_count += 1
    end = time.time()
    print("clone count: ", count, end - start)
    print("exist count: ", exist_count, len(repo_list), len(set(repo_list)))  # 850,1000
    break
print("count: ",count)
pool = newPool(nodes=50)
pool.map(get_each_repo_test_acc, repo_list)  # [:3]sample_repo_url ,token_num_list[:1]
pool.close()
pool.join()
#print(len(pro_info_python_list),pro_info_python_list[1]['language'])
'''
count=0
exist_count=0
repo_list=[]
for repo_info in pro_info_python_list[:10000]:
    url=repo_info['html_url']
    clone_flag,repo_name= github_util.clone_pro(pro_path, url)
    if repo_name in repo_list:
        print(f"{repo_name} is existed",url)
    repo_list.append(repo_name)

    if clone_flag==1:
        count+=1
    elif clone_flag==2:
        exist_count+=1
end=time.time()
print("clone count: ",count,end-start)
print("exist count: ",exist_count,len(repo_list),len(set(repo_list))) #850,1000
'''
# repo_name = url.split('/')[-1]
# if repo_name == "covid-19-data":
#     return 1, repo_name
# if not os.path.exists(pro_path):
#     os.makedirs(pro_path)
#
# os.chdir(pro_path)
# repo_html_url = url
# clone = "git clone " + repo_html_url
#
# if os.path.exists(pro_path + repo_name + "/"):
#     # print(pro_path + repo_name + " has existed!")
#     return 2, repo_name
#
# else:
#
#     os.system(clone)  # Cloning


