import sys, ast, os
import tokenize
import traceback
import random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + 'extract_transform_complicate_code_new/')
sys.path.append(code_dir + 'extract_transform_complicate_code_new/comprehension/')
import util
from wrap_refactoring import refactor_list_comprehension
from extract_transform_complicate_code_new.comprehension import extract_compli_for_comprehension_only_one_stmt_improve
save_complicated_code_dir_pkl = util.data_root + "chatgpt/"
'''
# util.save_pkl(save_complicated_code_dir_pkl_prefix, "all_methods_2000", all_methods)
# util.save_pkl(save_complicated_code_dir_pkl_prefix, "all_methods_2000_to_4000", all_methods)
# util.save_pkl(save_complicated_code_dir_pkl_prefix, "all_methods_4000_to_6000", all_methods)
# util.save_pkl(save_complicated_code_dir_pkl_prefix, "all_methods_6000_after", all_methods)
# save_complicated_code_dir_pkl_prefix = util.data_root + "chatgpt/"

# method_list = util.load_json(save_complicated_code_dir_pkl, "all_methods_2000")
# method_list = util.load_json(save_complicated_code_dir_pkl, "all_methods_2000_to_4000")

# method_list = util.load_json(save_complicated_code_dir_pkl, "all_methods_4000_to_6000")
method_list = util.load_json(save_complicated_code_dir_pkl, "all_methods_6000_after")

# list.extend(util.load_pkl(save_complicated_code_dir_pkl, "all_methods_2000_to_4000"))
# method_list.extend( util.load_pkl(save_complicated_code_dir_pkl, "all_methods_4000_to_6000"))
# method_list.extend(util.load_pkl(save_complicated_code_dir_pkl, "all_methods_6000_after"))
# for e in method_list:
#     print("len(method_list): ",method_list[0])
#     break
print("len(method_list): ",len(method_list))
n=int(len(method_list)*0.05)#len(method_list):  622539 1399039 1265903 974960
random.seed(2023)
random.shuffle(method_list)
samples = random.sample(method_list, n)
# #
# util.save_pkl(save_complicated_code_dir_pkl, f"methods_sample_1_{n}", method_list)
# util.save_pkl(save_complicated_code_dir_pkl, f"methods_sample_2_{n}", method_list)
# util.save_pkl(save_complicated_code_dir_pkl, f"methods_sample_3_{n}", method_list)
util.save_pkl(save_complicated_code_dir_pkl, f"methods_sample_4_{n}", method_list)
'''
# util.save_pkl(save_complicated_code_dir_pkl, f"methods_sample_4_{n}", method_list)

'''
all_methods=util.load_pkl(save_complicated_code_dir_pkl, "methods_sample_4_48748")
all_methods.extend(util.load_pkl(save_complicated_code_dir_pkl, "methods_sample_3_63295"))
all_methods.extend(util.load_pkl(save_complicated_code_dir_pkl, "methods_sample_2_69951"))
all_methods.extend(util.load_pkl(save_complicated_code_dir_pkl, "methods_sample_1_{n}"))
random.seed(2024)
random.shuffle(all_methods)
util.save_pkl(save_complicated_code_dir_pkl, "methods_sample_percent_5", all_methods)

# util.save_json(save_complicated_code_dir_pkl, "methods_sample_4_48748", all_methods)
util.save_json(save_complicated_code_dir_pkl, "methods_sample_percent_5", all_methods)
'''
from pathos.multiprocessing import ProcessingPool as newPool
# def save_file():
# '''
# ['ParlAI', 'https://github.com/facebookresearch/ParlAI/tree/master/parlai/tasks/personachat/agents.py',
#
# '/data1/zhangzejun/mnt/zejun/smp/data/python_star_2000repo/ParlAI/parlai/tasks/personachat/agents.py',
# 'OtherRevisedTeacher',
# "def __init__(self, opt, shared=None):\n        opt = copy.deepcopy(opt)\n        opt['datafile'] = _path(opt, 'other_revised')\n        super().__init__(opt, shared)"]

list_files_name = util.load_json(util.data_root, "benchmark_filenames")
list_ind_files=[int(e[1:-3]) for e in list_files_name ]
print(">>>list_files_name: ",list_files_name[0],list_ind_files[0])
all_methods=util.load_pkl(save_complicated_code_dir_pkl, "methods_sample_percent_5")
# print("368: ",all_methods[368][-1])#381
# print("381: ",all_methods[381][-1])
# print("387: ",all_methods[387][-1])
# print("16122: ",all_methods[16122])
# print("122412: ",all_methods[122412])
# print("122412: ",all_methods[122412][-1])
# print("123063: ",all_methods[123063])
# print("123063: ",all_methods[123063][-1])
# print("123791: ",all_methods[123791])
# print("123791: ",all_methods[123791][-1])
# print("125435: ",all_methods[125435])
# print("125435: ",all_methods[125435][-1])
# print("123063: ",all_methods[123063])
# print("123063: ",all_methods[123063][-1])
# print("126485: ",all_methods[126485])
# print("126485: ",all_methods[126485][-1])
# print("14933: ",all_methods[14933])
# print("14933: ",all_methods[14933][-1])
# print("15501: ",all_methods[15501])
# print("15501: ",all_methods[15501][-1])
# print("15544: ",all_methods[15544])
# print("15544: ",all_methods[15544][-1])
# print("15617: ",all_methods[15617])
# print("15617: ",all_methods[15617][-1])
# print("15784: ",all_methods[15784])
# print("15784: ",all_methods[15784][-1])
# print("155701: ",all_methods[155701])
# print("155701: ",all_methods[155701][-1])
# print("156465: ",all_methods[156465])
# print("156465: ",all_methods[156465][-1])
# print("161291: ",all_methods[161291])
# print("161291: ",all_methods[161291][-1])
# print("5684: ",all_methods[5684])
# print("5684: ",all_methods[5684][-1])
# print("5723: ",all_methods[5723])
# print("5723: ",all_methods[5723][-1])
# print("5899: ",all_methods[5899])
# print("5899: ",all_methods[5899][-1])
# print("5800: ",all_methods[5800])
# print("5800: ",all_methods[5800][-1])
# print("5908: ",all_methods[5908])
# print("5908: ",all_methods[5908][-1])
# print("5989: ",all_methods[5989])
# print("5989: ",all_methods[5989][-1])
print("5960: ",all_methods[5960])
print("5960: ",all_methods[5960][-1])


'''
list_file_content_repo=dict()
for ind in list_ind_files:
    list_file_content_repo[ind]=all_methods[ind]
    print("all_methods[ind]: ",all_methods[ind])
    # (repo, file_html, file_path, class_name, method_body)=e
util.save_pkl(util.data_root, "list_file_content_repo_benchmark", list_file_content_repo)
'''

'''
list_method_content=[]
method_dir=util.data_root+"make_benchmark_idiomatic/"
dict_info=dict()
for ind, e in enumerate(all_methods):
    (repo, file_html, file_path, class_name, method_body)=e
    dict_info[ind]=e[:-1]
    # print(all_methods[0])
    # for e in all_methods:
    util.save_file_path("_".join([method_dir,f'{ind}.py']),method_body)
util.save_pkl(save_complicated_code_dir_pkl, "dict_info_methods_sample_percent_5", dict_info)
'''
# new_dict=dict()
# all_methods=util.load_pkl(save_complicated_code_dir_pkl, "dict_info_methods_sample_percent_5")
# for key in all_methods:
#     new_dict[key]=all_methods[key][1]
#     # print("all_methods[key][1]: ",all_methods[key][1])
#     # break
# util.save_pkl(save_complicated_code_dir_pkl, "dict_info_methods_sample_percent_5_html", new_dict)
part_dict=dict()
all_methods=util.load_pkl(save_complicated_code_dir_pkl, "dict_info_methods_sample_percent_5_html")
print("len: ",len(all_methods.keys()))
for i in range(199610):
    part_dict[i]=all_methods[i]
    print(">>>>>: ",part_dict[i])
    break
# util.save_pkl(save_complicated_code_dir_pkl, "dict_info_methods_sample_percent_5_html_part", part_dict)

'''
method_dir=util.data_root+"make_benchmark_idiomatic/"

# dict_info = util.load_pkl(save_complicated_code_dir_pkl, "dict_info_methods_sample_percent_5")
list_comprehension_method_dir=util.data_root+"make_benchmark_idiomatic_list_comprehension/"
maybe_info_for_manual_check_method_dir=util.data_root+"make_benchmark_idiomatic/list_comprehension_ridiom/"

need_to_check_file_name=[]
need_to_check_file_name_excel=[]
tool_res=[]
k=0
ridiom_info=dict()# file_name method_num
ridiom_info_excel=[]
may_loss_num=0
current_method_num=0
import shutil

for i in range(4262441):
    file_name=f"_{i}.py"
    file_path=method_dir+file_name
    new_code_list=refactor_list_comprehension.refactor_list_comprehension(file_path)

    # print("dict_info: ",dict_info[i])
    # for e in new_code_list:
    #     print("each info: ",ast.unparse(e[0]),ast.unparse(e[1]),ast.unparse(e[-1]))
    #
    # print("new_code_list: ", new_code_list)
    lineno_list=[e[0].lineno for e in new_code_list]
    all_info=[[file_name,e[0].lineno,ast.unparse(e[0]),ast.unparse(e[-1])] for e in new_code_list]
    if new_code_list:
        ridiom_info[file_name]=lineno_list

        ridiom_info_excel.extend(all_info)
        current_method_num+=1
    k+=len(new_code_list)
    method_info=[]
    content = util.load_file_path(file_path)
    for node in ast.walk(ast.parse(content)):# 可能的non-idiomatic code
        if isinstance(node,(ast.For,ast.AsyncFor)):
            for e in node.body:
                if extract_compli_for_comprehension_only_one_stmt_improve.whether_fun_is_append(e, []):
                    if node.lineno not in lineno_list:
                        method_info.append(str(node.lineno))#node.lineno ast.unparse(node)
                        need_to_check_file_name_excel.append([file_name,node.lineno,ast.unparse(node)])
                    break
                # break
    if len(method_info):
        may_loss_num+=len(method_info)-len(new_code_list)
        print(f"it may loss {len(method_info)-len(new_code_list)} possible non-idiomatic code")
        need_to_check_file_name.append(", ".join([file_name]+method_info))

        shutil.copy(file_path, list_comprehension_method_dir + "need_to_check_files_list_comprehension/")
        # util.save_file_path(list_comprehension_method_dir + "need_to_check_files/"+f"_{i}.py",
        #                     "\n".join(need_to_check_file_name))

        # break
    # else:
    #     pass
    #     print("len(new_code_list), len(method_info): ",len(new_code_list), len(method_info))
    if current_method_num>=100:
        break
    # if k>100:
    #     break
    # if k>100:
    #     break
    # if new_code_list:
    #     break
    # print("method_info: ",method_info)
print("may_loss_num: ",may_loss_num,len(need_to_check_file_name),i,current_method_num)#may_loss_num:  628 517 22922 100
#这里是含有list comprehension的methods的数目大于100个
util.save_file_path(list_comprehension_method_dir+"need_to_check_info_list_comprehension_100.py","\n".join(need_to_check_file_name))
util.save_json(list_comprehension_method_dir, "ridiom_info_list_comprehension_100", ridiom_info)

util.save_csv(list_comprehension_method_dir+ "need_to_check_info_list_comprehension_100_methods.csv",
                  need_to_check_file_name_excel, ["file_name", "lineno"])
util.save_csv(list_comprehension_method_dir+ "ridiom_info_list_comprehension_100_methods.csv",
                  ridiom_info_excel, ["file_name", "lineno"])

# 这里是list comprehension 大于200个
# util.save_file_path(list_comprehension_method_dir+"need_to_check_info_list_comprehension.py","\n".join(need_to_check_file_name))
# util.save_json(list_comprehension_method_dir, "ridiom_info_list_comprehension", ridiom_info)
'''
