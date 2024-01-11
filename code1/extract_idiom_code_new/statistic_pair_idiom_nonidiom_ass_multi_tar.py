import copy
import sys, ast, os,random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir + "extract_idiom_code_new/")
sys.path.append(code_dir + "transform_s_c/")

from extract_idiom_for_else import get_idiom_for_else_improve
from extrac_idiom_assign_multiple import  get_idiom_assign_multi_improve

import util, traceback
import util_data_depend,util_data_statistic
from extract_simp_cmpl_data import ast_util
import complicated_code_util
import json,re
from pathos.multiprocessing import ProcessingPool as newPool


def get_node_type(node):
    if isinstance(node,ast.Expr):
        node=node.value
    type_node=str(node.__class__)
    result = re.search('\'ast.(.*)\'', type_node)
    return result.group(1)

def get_features(ast_node):
    dict_feature = {"num_=":0,"num_targets": 0,"num_starred":0}
    num_call_with_name = 0
    # for ast_node in node_list:
    dict_feature["num_="]=len(ast_node.targets)
    num_tar=0
    for tar in ast_node.targets:
        num_tar+=ast_util.get_basic_count(tar)

        dict_feature["num_starred"] = max(ast_util.get_starred_count(tar),dict_feature["num_starred"])
    dict_feature["num_targets"] =num_tar# max(ast_util.get_basic_count(tar), dict_feature["num_targets"])
    return dict_feature
# def get_stm_node(ast_node):
#     dict_stmt_node=dict()
def statistics_feature(save_complicated_code_dir_pkl):
    result_compli_for_else_list = []
    dict_feature = {"num_=":[],"num_targets": [],"num_starred":[],"repo":[],"file_html":[]}
    dict_data_attr = {"is_data_depend":[],"value_constant":[]}
    dict_value_type=dict()
    dict_tar_type = dict()
    for file_name in os.listdir(save_complicated_code_dir_pkl):
        repo_name = file_name[:-4]
        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)
        # print("come to the repo: ", repo_name)
        for file_html in complicate_code:
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if complicate_code[file_html][cl][me]:
                        for code in complicate_code[file_html][cl][me]:
                            ass_code=code
                            dict_value=dict()
                            ast_util.get_basic_type(ass_code.value,dict_value)

                            dict_tar=dict()
                            for tar in ass_code.targets:
                                ast_util.get_basic_type(tar, dict_tar)

                            for key in dict_value:
                                if key in dict_value_type:
                                    dict_value_type[key]+=1
                                else:
                                    dict_value_type[key] = 1

                            for key in dict_tar:
                                if key in dict_tar_type:
                                    dict_tar_type[key]+=1
                                else:
                                    dict_tar_type[key] = 1

                            is_data_depend = util_data_depend.is_ass_depend(ass_code)
                            dict_data_attr["is_data_depend"].append(is_data_depend)
                            dict_data_attr["value_constant"].append(util_data_depend.is_const_data(ass_code.value))
                            # count_obj=ast_util.get_basic_count(ass_code.value)
                            # count_const =0
                            # for e in ast.walk(ass_code.value):
                            #     if isinstance(e,ast.Constant):
                            #         count_const+=1
                            # if count_obj>count_const:
                            #     dict_data_attr["value_constant"].append(0)
                            # else:
                            #     dict_data_attr["value_constant"].append(1)

                            each_feature=get_features(ass_code)
                            # code[2]
                            for key in each_feature:
                                dict_feature[key].append(each_feature[key])
                            dict_feature["repo"].append(repo_name)
                            dict_feature["file_html"].append(file_html)

        #         break
        #     break
        # break
    # util_data_statistic.data_info(dict_feature,show_fig=False)
    sum_data=len(dict_data_attr["value_constant"])
    print("dict_tar_type: ",dict_tar_type)
    print("dict_value_type: ", dict_value_type)
    print("value_constant: ",sum_data,dict_data_attr["value_constant"].count(0),dict_data_attr["value_constant"].count(1),sum(dict_data_attr["value_constant"])/sum_data)
    print("is_data_depend: ",sum_data,dict_data_attr["is_data_depend"].count(0),dict_data_attr["is_data_depend"].count(1),sum(dict_data_attr["is_data_depend"])/sum_data)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_feature_num", dict_feature)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_targets_object", dict_tar_type)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object", dict_value_type)

def save_to_csv(save_complicated_code_dir_pkl):
    result_compli_for_else_list = []
    for file_name in sorted(os.listdir(save_complicated_code_dir_pkl)):
        repo_name = file_name[:-4]
        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)
        print("come to the repo: ", repo_name)
        for file_html in complicate_code:
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if complicate_code[file_html][cl][me]:
                        for code in complicate_code[file_html][cl][me]:
                            # result_compli_for_else_list.append(
                            #     [repo_name, file_html, cl, me, ast.unparse(code[0]),"\n".join([code[1],code[0],code[2]])
                            #      ])
                            ass_node=code
                            each_feature = get_features(ass_node)

                            is_data_depend=util_data_depend.is_ass_depend(ass_node)
                            # print("save_to_csv code: ",code)
                            result_compli_for_else_list.append(
                                [repo_name, file_html, cl, me, ast.unparse(ass_node),is_data_depend,each_feature["num_="],each_feature["num_targets"],each_feature["num_starred"]
                                 ])
    random.seed(2023)
    random.shuffle(result_compli_for_else_list)
    print(result_compli_for_else_list[:5])
    util.save_csv(util.data_root + "detection_idiom_code_dir_star_1000_csv/multi_assign_idiom_code.csv",
                  result_compli_for_else_list,
                  ["repo_name", "file_html", "cl", "me","code", "has_data_depend","num_=", "num_targets", "num_starred"])

def save_repo_for_else_complicated(repo_name):
    count_complicated_code = 0
    # print("come the repo: ", repo_name)
    one_repo_for_else_code_list = []
    dict_file = dict()
    for file_info in dict_repo_file_python[repo_name]:

        file_path = file_info["file_path"]
        file_path = util.prefix_root + file_path
        # file_path = "/home/" + "/".join(file_path.split("/")[2:])
        # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
        #     continue
        file_html = file_info["file_html"]
        print("come this file: ", file_path)
        try:
            content = util.load_file_path(file_path)
        except:
            print(f"{file_path} is not existed!")
            continue
        # print("content: ",content)
        try:
            file_tree = ast.parse(content)
            ana_py = ast_util.Fun_Analyzer()
            ana_py.visit(file_tree)

            dict_class = dict()
            for tree, class_name in ana_py.func_def_list:
                # code_list = []

                code_list = get_idiom_assign_multi_improve(tree)

                # old_code_list=get_idiom_truth_value_test_improve_add_parent_node(tree)
                # for code in old_code_list:
                #     # print("code: ",ast.unparse(code))
                #     old_code_list[code].append(code)
                #     code_list.append(old_code_list[code])

                # code_list=get_pair_idiom_nonIdiom(tree)
                if code_list:
                    ast_util.set_dict_class_code_list(tree, dict_class, class_name, code_list)

            # print("func number: ",file_html,len(ana_py.func_def_list))
            # for tree in ana_py.func_def_list:
            #     #print("tree_ func_name",tree.__dict__)
            #     code_list.extend(get_idiom_assign_multi(tree))
            # if code_list:
            #         one_repo_for_else_code_list.append([code_list, file_path, file_html])
            if dict_class:
                dict_file[file_html] = dict_class
        except SyntaxError:
            print("the file has syntax error")
            continue
        except ValueError:

            traceback.print_exc()

            print("the file has value error: ", file_html)

            continue
        # break
    if 1:  # dict_file:
        # count_complicated_code=count_complicated_code+len(one_repo_for_else_code_list)
        # print("it exists for else complicated code1: ", len(one_repo_for_else_code_list))
        # util.save_pkl(save_complicated_code_dir_pkl,repo_name,dict_file)
        util.save_pkl(save_complicated_code_dir_pkl, repo_name, dict_file)

        # util.save_json(save_complicated_code_dir, repo_name, dict_file)
        # print("save successfully! ", save_complicated_code_dir + repo_name)

    return count_complicated_code

# def parse_a_tree(tree):
#     code_list=[]
#     old_code_list = get_idiom_list_comprehension_improve(tree)
#     for code in old_code_list:
#         each_code_pair = transform_idiom_list_comprehension(code[0], code[1])
#         if each_code_pair:
#             code_list.append(each_code_pair)



if __name__ == '__main__':
    print("begin to run code ", util.data_root)
    code = '''
info_list = [[x.strip() for x in list(g)] for (k, g) in groups if not k] 
perm_back += [max(e.axis1, e.axis2) for e in edges]
a=[e for e in w if e>2]
a=[e if e else w if w else b for e in w if e>2]
order_payload = {'identifiers': [{'type': 'dns', 'value': d} for d in domains]}
ret = [[value[0]] + value[1] for value in zip(self.rownames, ret)]

crc, magic, attributes = [field.decode(data) for field in base_fields]

d = ((n, x, [(y, m / n) for (y, m) in y]) for (n, x, y) in d)
ohlcv['ll'] = [min(l, c) for (l, c) in zip(ohlcv['low'], ohlcv['close'].shift(1))]
p = sum([opp[state] for (j, opp) in enumerate(player) if i != j])

ix2 = [ix2 for (ix2, (_, col2)) in enumerate(first_linewithcol) if col2 == col1] 
'''
    ast_node=ast.parse("info_list = [[x.strip() if w else [1 for i in a if k] for x in list(g)] if k else c for (k, g) in groups if not k if w]")
    for node in ast.walk(ast_node):
        if isinstance(node,ast.ListComp):
            # print(get_features(node))
            pass
    # '''
    data=[1]
    # json_file=open(util.data_root + "python3_1000repos_files_info" + '.json', 'r')
    with open(util.data_root + 'test_dump_json.json', 'w') as json_file:
        json.dump(data, json_file)
    with open(util.data_root + 'test_dump_json.json', 'r') as json_file:

        data=json.load(json_file)
        print("data: ",data)
    # dict_repo_file_python= util.load_json(util.data_root, "test_dump_json")

    print("load test repo info successfuly")

    print("util.data_root: ",util.data_root)
    # '''
    # '''
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    # json_file=open(util.data_root + "python3_1000repos_files_info" + '.json', 'r')
    # w=json.load(json_file)
    # print("content of json: ",w)
    print("load repo info successfuly")
    # save_complicated_code_dir_pkl= util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_is_not_no_len/"
    # save_complicated_code_dir_pkl= util.data_root_mv + "idiom_code_pair/dir_pkl/multi_assign_idiom_code/"
    # save_complicated_code_dir_pkl= util.data_root_home + "idiom_code_dir_pkl/multi_assign_idiom_code/"
    save_complicated_code_dir_pkl = util.data_root + "detection_idiom_code_dir_pkl_new/chained_comparison_idiom_code/"
    save_complicated_code_dir_pkl= util.data_root + "detection_idiom_code_dir_pkl_new/truth_value_test_idiom_code_create_func/"
    save_complicated_code_dir_pkl = util.data_root + "detection_idiom_code_dir_pkl_new/for_else_idiom_code/"
    save_complicated_code_dir_pkl= util.data_root + "detection_idiom_code_dir_pkl_new/multi_assign_idiom_code/"
    save_complicated_code_feature_dir_pkl = util.data_root + "rq_1/"

    repo_name_list = []
    for repo_name in dict_repo_file_python:
        if not os.path.exists(util.pro_dir + repo_name):
            continue
        repo_name_list.append(repo_name)
    print(f"it has {len(repo_name_list)} repos")

    '''
    pool = newPool(nodes=50)
    pool.map(save_repo_for_else_complicated, repo_name_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    '''

    # complicate_code = util.load_pkl(save_complicated_code_dir_pkl, "CobaltStrikeParser")
    # print("complicate_code: ",complicate_code)
    statistics_feature(save_complicated_code_dir_pkl)
    # save_to_csv(save_complicated_code_dir_pkl)
    

