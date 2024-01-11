import sys, ast, os,random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir + "extract_idiom_code_new/")
sys.path.append(code_dir + "transform_s_c/")
from extrac_idiom_for_set_comprehension import get_idiom_set_comprehension_improve

import util, traceback,util_data_statistic
from extract_simp_cmpl_data import ast_util
import complicated_code_util
import json
from pathos.multiprocessing import ProcessingPool as newPool
import re
def get_node_type(node):
    if isinstance(node,ast.Expr):
        node=node.value
    type_node=str(node.__class__)
    result = re.search('\'ast.(.*)\'', type_node)
    return result.group(1)

def get_features(ast_node):
    dict_feature = {"num_comprehension":0,"num_loop": 0, "num_if": 0, "num_if_else": 0}
    num_call_with_name = 0
    # for ast_node in node_list:
    elt_flag=0
    for node in ast.walk(ast_node):
        if isinstance(node, ast.SetComp):
            print("listcomp node: ",ast.unparse(node))
            dict_feature["num_comprehension"]+=1
            generators = node.generators
            dict_feature["num_loop"] += len(generators)
            for gen in generators:
                ifs = gen.ifs
                dict_feature["num_if"] += len(ifs)
            elt = node.elt
            if not elt_flag:
                for e in ast.walk(elt):
                        if isinstance(e, ast.IfExp):
                            dict_feature["num_if_else"] += 1
            elt_flag=1
            print("dict_feature: ",dict_feature)
            break
    return dict_feature
# def get_stm_node(ast_node):
#     dict_stmt_node=dict()
def statistics_feature(save_complicated_code_dir_pkl):
    result_compli_for_else_list = []
    dict_feature = {"num_comprehension":[],"num_loop": [], "num_if": [], "num_if_else": [],"repo":[],"file_html":[]}
    dict_elt_node=dict()

    for file_name in os.listdir(save_complicated_code_dir_pkl):
        repo_name = file_name[:-4]
        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)
        print("come to the repo: ", repo_name)
        for file_html in complicate_code:
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if complicate_code[file_html][cl][me]:
                        for code in complicate_code[file_html][cl][me]:
                            each_feature=get_features(code[1])
                            # code[2]
                            elt_node = code[1].elt
                            elt_node_type = get_node_type(elt_node)
                            if elt_node_type not in dict_elt_node:
                                dict_elt_node[elt_node_type] = 1
                            else:
                                dict_elt_node[elt_node_type] += 1
                            for key in each_feature:
                                dict_feature[key].append(each_feature[key])
                            dict_feature["repo"].append(repo_name)
                            dict_feature["file_html"].append(file_html)

        #         break
        #     break
        # break
    # util_data_statistic.data_info(dict_feature,show_fig=False)
    total_num = sum(list(dict_elt_node.values()))
    print("total_num: ",total_num,dict_elt_node)

    for key in dict_elt_node:
        print("dict_elt_node, key and ratio: ", dict_elt_node[key], dict_elt_node[key] / total_num)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "set_compre_feature_num", dict_feature)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "set_compre_object", dict_elt_node)

    # print("dict_feature: ",dict_feature)

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
                            for node in ast.walk(code[0]):
                                for child in ast.iter_child_nodes(node):
                                    if isinstance(child,ast.SetComp):
                                        direct_parent=node
                                        break
                                else:
                                    continue
                                break

                            stmt_node=code[0]
                            elt_node = code[1].elt
                            elt_node_type = get_node_type(elt_node)
                            each_feature = get_features(code[1])
                            num_comprehension,num_loop,num_if,num_if_else=each_feature["num_comprehension"],each_feature["num_loop"],each_feature["num_if"],each_feature["num_if_else"]
                            # print("save_to_csv code: ",code)
                            result_compli_for_else_list.append(
                                [repo_name, file_html, cl, me, ast.unparse(code[1]), ast.unparse(stmt_node),
                                 ast.unparse(direct_parent), ast.unparse(elt_node), get_node_type(stmt_node),
                                 get_node_type(direct_parent), elt_node_type,num_comprehension,num_loop,num_if,num_if_else
                                 ])
                            # result_compli_for_else_list.append(
                            #     [repo_name, file_html, cl, me, ast.unparse(code[1]),ast.unparse(stmt_node),ast.unparse(direct_parent),get_node_type(stmt_node),get_node_type(direct_parent)
                            #      ])

        #     break
        # break
    # for e in result_compli_for_else_list:
    #     print("each code: ",e)
    dict_num_parent=dict()
    dict_num_stmt = dict()
    dict_num_stmt_parent=dict()
    for e in result_compli_for_else_list:
        parent=e[9]
        stmt=e[8]
        if parent in dict_num_parent:
            dict_num_parent[parent]+=1
        else:
            dict_num_parent[parent]=1
        if stmt in dict_num_stmt:
            dict_num_stmt[stmt] += 1
        else:
            dict_num_stmt[stmt] = 1
        if stmt in dict_num_stmt_parent:
            if parent in dict_num_stmt_parent[stmt]:
                dict_num_stmt_parent[stmt][parent] += 1
            else:
                dict_num_stmt_parent[stmt][parent]=1
        else:
            dict_num_stmt_parent[stmt] = {parent:1}
    print(">>>>>>>>>>dict_num_parent: ",dict_num_parent)
    print(">>>>>>>>>>dict_num_stmt: ",dict_num_stmt)

    print(">>>>>>>>>>dict_num_stmt_parent: ",dict_num_stmt_parent)

    item_parent=list(dict_num_parent.items())
    print(">>>>>>>>>>>>")
    for e in item_parent:
        print(e[0])
    print(">>>>>>>>>>>>")
    for e in item_parent:
        print(e[1])
    result_compli_for_else_list.append(
        [repo_name, file_html, cl, me, ast.unparse(code[1]), ast.unparse(stmt_node),
         ast.unparse(direct_parent), ast.unparse(elt_node), get_node_type(stmt_node),
         get_node_type(direct_parent), elt_node_type
         ])
    util.save_pkl(util.data_root +"usage_context/", "set_compre", dict_num_parent)

    random.shuffle(result_compli_for_else_list)
    util.save_csv(util.data_root + "detection_idiom_code_dir_star_1000_csv/set_comprehension_idiom_code.csv",
                  result_compli_for_else_list,
                  ["repo_name", "file_html", "cl", "me",
                   "complicate_code", "stmt_code",
                   "parent_code","elt_code","stmt_type","parent_type","elt_type","num_compre","num_loop","num_if","num_if_else"])


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
        # if file_html!="https://github.com/venmo/business-rules/tree/master/business_rules/operators.py":
        #     continue
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
                code_list = []
                code_list = get_idiom_set_comprehension_improve(tree)

                # for code in old_code_list:
                #     each_code_pair = transform_idiom_list_comprehension(code[0],code[1])
                #     if each_code_pair:
                #         code_list.append(each_code_pair)

                # code_list=get_pair_idiom_nonIdiom(tree)
                if code_list:
                    ast_util.set_dict_class_code_list(tree, dict_class, class_name, code_list)

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
        pass
        # util.save_json(save_complicated_code_dir, repo_name, dict_file)
        # print("save successfully! ", save_complicated_code_dir + repo_name)

    return count_complicated_code




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
    save_complicated_code_dir_pkl = util.data_root + "detection_idiom_code_dir_pkl_new/list_comprehension_idiom_code/"
    save_complicated_code_dir_pkl = util.data_root + "detection_idiom_code_dir_pkl_new/set_comprehension_idiom_code/"
    save_complicated_code_feature_dir_pkl = util.data_root + "rq_1/"

    repo_name_list = []
    for repo_name in dict_repo_file_python:
        if not os.path.exists(util.pro_dir + repo_name):
            continue
        repo_name_list.append(repo_name)
    '''
    pool = newPool(nodes=30)
    pool.map(save_repo_for_else_complicated, repo_name_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    '''
    # complicate_code = util.load_pkl(save_complicated_code_dir_pkl, "CobaltStrikeParser")
    # print("complicate_code: ",complicate_code)
    save_to_csv(save_complicated_code_dir_pkl)
    # statistics_feature(save_complicated_code_dir_pkl)


