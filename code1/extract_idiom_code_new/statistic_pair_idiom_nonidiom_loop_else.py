import copy
import sys, ast, os,random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir + "extract_idiom_code_new/")
sys.path.append(code_dir + "transform_s_c/")

from extract_idiom_for_else import get_idiom_for_else_improve
from transform_for_else_s_c import For_Else_C_S
import util, traceback,util_data_statistic,util_idiom_rq1
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

# def get_stm_node(ast_node):
#     dict_stmt_node=dict()
def statistics_feature(save_complicated_code_dir_pkl):
    result_compli_for_else_list = []
    dict_feature = {"For":0,"While":0}
    dict_objects = {"has_break":[],"repo":[],"file_html":[]}
    dict_data_attr = dict()
    for file_name in os.listdir(save_complicated_code_dir_pkl):
        repo_name = file_name[:-4]
        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)
        # print("come to the repo: ", repo_name)
        for file_html in complicate_code:
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if complicate_code[file_html][cl][me]:
                        for code in complicate_code[file_html][cl][me]:
                            for_node=code[-1]
                            loop_kind=get_node_type(for_node)
                            if loop_kind in dict_feature:
                                dict_feature[loop_kind]+=1
                            else:
                                dict_feature[loop_kind] =1
                            if isinstance(for_node,ast.For):
                                util_idiom_rq1.count_key_value(for_node.iter,dict_data_attr)
                            else:
                                util_idiom_rq1.count_key_value(for_node.test,dict_data_attr)

                            copy_node = copy.deepcopy(code[-1])
                            for_else_traverse = For_Else_C_S()
                            for_else_traverse.traverse_cur_layer(copy_node)
                            has_break = for_else_traverse.has_break
                            dict_objects["has_break"].append(has_break)
                            dict_objects["repo"].append(repo_name)
                            dict_objects["file_html"].append(file_html)

                            # each_feature=get_features(code[1])
                            # # code[2]
                            # for key in each_feature:
                            #     dict_feature[key].append(each_feature[key])

        #         break
        #     break
        # break
    # util_data_statistic.data_info(dict_objects, show_fig=False)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "loop_else_feature_num", dict_objects)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "loop_else_data", dict_data_attr)

    print("dict_data_attr: ",dict_data_attr)
    total_num=sum(dict_feature.values())
    print("dict_feature: ",dict_feature,total_num)

    for key in dict_feature:
        print("key, value, ratio: ",key, dict_feature[key], dict_feature[key]/total_num)
def save_to_csv(save_complicated_code_dir_pkl):
    result_compli_for_else_list = []
    for file_name in os.listdir(save_complicated_code_dir_pkl):
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
                            loop_code=code[-1]

                            copy_node = copy.deepcopy(loop_code)
                            for_else_traverse = For_Else_C_S()
                            for_else_traverse.traverse_cur_layer(copy_node)
                            has_break=for_else_traverse.has_break
                            # print("save_to_csv code: ",code)
                            result_compli_for_else_list.append(
                                [repo_name, file_html, cl, me, ast.unparse(loop_code),get_node_type(loop_code),has_break
                                 ])



    random.shuffle(result_compli_for_else_list)
    util.save_csv(util.data_root + "detection_idiom_code_dir_star_1000_csv/loop_else_idiom_code.csv",
                  result_compli_for_else_list,
                  ["repo_name", "file_html", "cl", "me","complicate_code", "loop_type","has_break"])

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
                code_list = get_idiom_for_else_improve(tree)

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
    

