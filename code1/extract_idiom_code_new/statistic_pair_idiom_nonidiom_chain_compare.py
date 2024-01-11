import sys, ast, os,random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir + "extract_idiom_code_new/")
sys.path.append(code_dir + "transform_s_c/")
from extrac_idiom_chained_comparison import get_idiom_chained_comparison_improve,get_idiom_chained_comparison_improve_add_parent_node
from transform_chain_compare_s_c import transform_idiom_chain_compare

import util, traceback
from extract_simp_cmpl_data import ast_util
import complicated_code_util,util_data_statistic
import json,re
from pathos.multiprocessing import ProcessingPool as newPool


def get_node_type(node):
    if isinstance(node,ast.Expr):
        node=node.value
    type_node=str(node.__class__)
    result = re.search('\'ast.(.*)\'', type_node)
    return result.group(1)

def get_features(ast_node):
    dict_feature = {'num_cmpop': 0, "num_Lt": 0, "num_Gt": 0,
                    "num_Eq": 0, "num_NotEq": 0, "num_LtE": 0, "num_GtE": 0, "num_NotIn": 0, "num_In": 0, "num_Is": 0,
                    "num_IsNot": 0}
    cmpop_1, cmpop_2, cmpop_3, cmpop_4, cmpop_5, cmpop_6, cmpop_7, cmpop_8, cmpop_9, cmpop_10 = 0, 0, 0, 0, 0, 0, 0, 0, 0, 0

    for node in ast.walk(ast_node):
        if isinstance(node, ast.Compare):
            if len(node.ops) > 1:
                dict_feature['num_cmpop']=len(node.ops)

                for cmpop in node.ops:
                    if isinstance(cmpop, ast.Eq):
                        dict_feature['num_Eq'] += 1
                    elif isinstance(cmpop, ast.NotEq):
                        dict_feature['num_NotEq'] += 1
                    elif isinstance(cmpop, ast.LtE):
                        dict_feature['num_LtE'] += 1
                    elif isinstance(cmpop, ast.GtE):
                        dict_feature['num_GtE'] += 1
                    elif isinstance(cmpop, ast.Lt):
                        dict_feature['num_Lt'] += 1
                    elif isinstance(cmpop, ast.Gt):
                        dict_feature['num_Gt'] += 1
                    elif isinstance(cmpop, ast.NotIn):
                        dict_feature['num_NotIn'] += 1
                    elif isinstance(cmpop, ast.In):
                        dict_feature['num_In'] += 1
                    elif isinstance(cmpop, ast.Is):
                        dict_feature['num_Is'] += 1
                    elif isinstance(cmpop, ast.IsNot):
                        dict_feature['num_IsNot'] += 1
                break
    # print("dict_feature: ", dict_feature)


    return dict_feature
# def get_stm_node(ast_node):
#     dict_stmt_node=dict()
def statistics_feature(save_complicated_code_dir_pkl):
    result_compli_for_else_list = []
    # dict_feature = {'num_cmpop': [], "num_Lt": 0, "num_Gt": 0,
    #                 "num_Eq": 0, "num_NotEq": 0, "num_LtE": 0, "num_GtE": 0, "num_NotIn": 0, "num_In": 0, "num_Is": 0,
    #                 "num_IsNot": 0}
    dict_feature = {'num_cmpop': [], "num_Lt": [], "num_Gt": [],
                    "num_Eq": [], "num_NotEq": [], "num_LtE": [], "num_GtE": [],
                    "num_NotIn": [], "num_In": [], "num_Is": [],
                    "num_IsNot": [],"repo":[],"file_html":[]}
    dict_chained_objects=dict()# data type of the chained object

    for file_name in os.listdir(save_complicated_code_dir_pkl):
        repo_name = file_name[:-4]
        # repo_name="electrum-personal-server"
        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)
        # print("come to the repo: ", repo_name)
        for file_html in complicate_code:
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if complicate_code[file_html][cl][me]:
                        for code in complicate_code[file_html][cl][me]:
                            compare_code=code[-1]
                            each_feature=get_features(code[1])
                            comparators=compare_code.comparators[:-1]
                            for compa in comparators:
                                compa_type=get_node_type(compa)
                                if compa_type not in dict_chained_objects:
                                    dict_chained_objects[compa_type]=1
                                else:
                                    dict_chained_objects[compa_type] += 1
                            # code[2]
                            # print("each_feature: ", each_feature)
                            for key in each_feature:
                                if 'num_cmpop'==key:
                                    dict_feature[key].append(each_feature[key])
                                else:
                                    dict_feature[key].append(1 if each_feature[key] else 0)
                                # dict_feature[key].append(each_feature[key])
                            dict_feature["repo"].append(repo_name)
                            dict_feature["file_html"].append(file_html)

                # break
            # break
        # break
    # print("dict_feature: ",dict_feature)
    # util_data_statistic.data_info(dict_feature,show_fig=False)
    total_num = sum(list(dict_chained_objects.values()))
    print("total num of dict_chained_objects: ",total_num,dict_chained_objects)
    dict_chained_objects_total=dict()
    # for key in dict_feature:
    #     dict_chained_objects_total[key] = sum(dict_feature[key])
    #
    for key in dict_chained_objects:
        print("dict_chained_objects, key and ratio: ", key,dict_chained_objects[key], dict_chained_objects[key] / total_num)
    print("dict_chained_objects_total: ",dict_chained_objects_total)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "chain_compare_feature_num", {'num_cmpop':dict_feature['num_cmpop'],'repo': dict_feature['repo'],'file_html':dict_feature['file_html']})
    util.save_pkl(save_complicated_code_feature_dir_pkl, "chain_compare_object", dict_chained_objects)

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
                            compare_code=code[-1]
                            each_feature = get_features(code[1])
                            num_ops,num_Is,num_In,num_IsNot=each_feature["num_cmpop"],each_feature["num_Is"],each_feature["num_In"],each_feature["num_IsNot"]

                            direct_parent=code[1]
                            stmt_node=code[0]
                            comparators = compare_code.comparators[:-1]
                            comparators_str=[ast.unparse(comp) for comp in comparators]
                            type_list=[get_node_type(comp) for comp in comparators]
                            # print("save_to_csv code: ",code,compare_code.__dict__,file_html,ast.unparse(compare_code))
                            result_compli_for_else_list.append(
                                [repo_name, file_html, cl, me, ast.unparse(compare_code),ast.unparse(stmt_node),ast.unparse(direct_parent),get_node_type(stmt_node),get_node_type(direct_parent),comparators_str,type_list,num_ops,num_Is,num_In,num_IsNot
                                 ])

        #     break
        # break
    # for e in result_compli_for_else_list:
    #     print("each code: ",e)
    dict_num_parent=dict()
    dict_num_stmt = dict()
    dict_num_stmt_parent=dict()
    for e in result_compli_for_else_list:
        parent=e[7]
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

    item_parent = list(dict_num_parent.items())
    print(">>>>>>>>>>>>")
    for e in item_parent:
        print(e[0])
    print(">>>>>>>>>>>>")
    for e in item_parent:
        print(e[1])
    util.save_pkl(util.data_root +"usage_context/", "chain_compare", dict_num_parent)

    random.shuffle(result_compli_for_else_list)
    util.save_csv(util.data_root + "detection_idiom_code_dir_star_1000_csv/chained_comparison_idiom_code.csv",
                  result_compli_for_else_list,
                  ["repo_name", "file_html", "cl", "me","complicate_code", "stmt_code","parent_code","stmt_type","parent_type","comparators_str","comparator type","num_ops","num_Is","num_In","num_IsNot"])

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
                code_list = []
                old_code_list = get_idiom_chained_comparison_improve_add_parent_node(tree)
                for code in old_code_list:
                    # print("code: ",ast.unparse(code))
                    old_code_list[code].append(code)
                    code_list.append(old_code_list[code])

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

def parse_a_tree(tree):
    code_list=[]
    old_code_list = get_idiom_list_comprehension_improve(tree)
    for code in old_code_list:
        each_code_pair = transform_idiom_list_comprehension(code[0], code[1])
        if each_code_pair:
            code_list.append(each_code_pair)



if __name__ == '__main__':
    print("begin to run code ", util.data_root)
    code = '''
if 0 < x < world.width - 1 and 0 < y < world.height - 1:
    surr_tiles = solid_map[y-1:y+2, x-1:x+2]
'''
    ast_node=ast.parse(code)
    get_idiom_chained_comparison_improve_add_parent_node(ast_node)

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
    # statistics_feature(save_complicated_code_dir_pkl)
    save_to_csv(save_complicated_code_dir_pkl)
    

