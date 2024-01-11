import sys, ast, os
import tokenize
import traceback
import random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
sys.path.append(code_dir)
sys.path.append(code_dir + 'extract_transform_complicate_code_new/')
sys.path.append(code_dir + 'extract_transform_complicate_code_new/comprehension/')
import util
from wrap_refactoring import refactor_list_comprehension_add_data_flow
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
'''
all_methods=util.load_pkl(save_complicated_code_dir_pkl, "methods_sample_percent_5")
# ['ParlAI', 'https://github.com/facebookresearch/ParlAI/tree/master/parlai/tasks/personachat/agents.py',
#
# '/data1/zhangzejun/mnt/zejun/smp/data/python_star_2000repo/ParlAI/parlai/tasks/personachat/agents.py',
# 'OtherRevisedTeacher',
# "def __init__(self, opt, shared=None):\n        opt = copy.deepcopy(opt)\n        opt['datafile'] = _path(opt, 'other_revised')\n        super().__init__(opt, shared)"]

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
method_dir=util.data_root+"make_benchmark_idiomatic/"
import shutil
# dict_info = util.load_pkl(save_complicated_code_dir_pkl, "dict_info_methods_sample_percent_5")
list_comprehension_method_dir=util.data_root+"make_benchmark_idiomatic_list_comprehension_new/"
files_dir=list_comprehension_method_dir+"need_to_check_files_list_comprehension/"
# maybe_info_for_manual_check_method_dir=util.data_root+"make_benchmark_idiomatic/list_comprehension_ridiom/"
if os.path.exists(files_dir):
    shutil.rmtree(files_dir)
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
    # if i !=55: #3277 3673 1054
    #     continue
    file_name=f"_{i}.py"
    print(">>>>>file_name: ",file_name)

    file_path=method_dir+file_name
    new_code_list=refactor_list_comprehension_add_data_flow.refactor_list_comprehension(file_path)

    # print("dict_info: ",dict_info[i])
    for e in new_code_list:
        print("each info: ",ast.unparse(e[0]),"\n>>>>",ast.unparse(e[1]),"\n>>>>",ast.unparse(e[-1]))
    # continue
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
        if not os.path.exists(files_dir):
            os.makedirs(files_dir)#mkdir
        shutil.copy(file_path, files_dir)
        # util.save_file_path(list_comprehension_method_dir + "need_to_check_files/"+f"_{i}.py",
        #                     "\n".join(need_to_check_file_name))

        # break
    # else:
    #     pass
    #     print("len(new_code_list), len(method_info): ",len(new_code_list), len(method_info))
    # print(">>>>>current_method_num: ",current_method_num)
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

