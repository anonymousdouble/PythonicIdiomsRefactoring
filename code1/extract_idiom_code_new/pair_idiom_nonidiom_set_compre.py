import sys, ast, os, random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
# print("code_dir: ", code_dir)
sys.path.append(code_dir)
sys.path.append(code_dir + "extract_idiom_code_new/")
sys.path.append(code_dir + "transform_s_c/")
from extrac_idiom_for_set_comprehension import get_idiom_set_comprehension_improve
from transform_set_compre_s_c import transform_idiom_list_comprehension

import util, traceback
from extract_simp_cmpl_data import ast_util
import complicated_code_util
import json
from pathos.multiprocessing import ProcessingPool as newPool


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
                            #     [repo_name, file_html, cl, me, ast.unparse(code[0]),
                            #      code[1]])
                            # result_compli_for_else_list.append(
                            #     [repo_name, file_html, cl, me, ast.unparse(code[0]), "\n".join(code[1][::-1])
                            #      ])
                            parent_node, node, complete_code, temporary_flag, create_fun_flag = code[0], code[3], code[
                                4], code[5], code[6]

                            for node in ast.walk(parent_node):
                                for child in ast.iter_child_nodes(node):
                                    if isinstance(child, ast.SetComp):
                                        direct_parent = node
                                        break
                                else:
                                    continue
                                break
                            # result_compli_for_else_list.append(
                            #     [repo_name, file_html, cl, me, ast.unparse(code[0]),
                            #      "\n".join([code[1][1], code[1][0], code[1][2]])
                            #      ])
                            parent_node_type = ast_util.get_node_type(parent_node)
                            direct_parent_type = ast_util.get_node_type(direct_parent)
                            result_compli_for_else_list.append(
                                [repo_name, file_html, cl, me, ast.unparse(parent_node), ast.unparse(direct_parent),
                                 ast.unparse(node), complete_code,
                                 parent_node_type, direct_parent_type, temporary_flag, create_fun_flag
                                 ])
        #     break
        # break
    # for e in result_compli_for_else_list:
    #     print("each code: ",e)
    # util.save_csv(util.data_root + "idiom_code_dir_star_1000_csv/set_comprehension_idiom_code.csv",
    #               result_compli_for_else_list,
    #               ["repo_name", "file_html", "cl", "me", "complicate_code", "simple_code"])
    util.save_pkl(util.data_root + "idiom_code_dir_star_1000_csv/", "set_comprehension_idiom_code_shuffle", result_compli_for_else_list)
    random.seed(2023)
    random.shuffle(result_compli_for_else_list)

    util.save_csv(util.data_root + "idiom_code_dir_star_1000_csv/set_comprehension_idiom_code_shuffle.csv",
                  result_compli_for_else_list,
                  ["repo_name", "file_html", "cl", "me","stmt_code","parent_code","code","complicate_code", "parent_node_type","direct_parent_type","temporary_flag", "create_fun_flag"])


# def get_pair_idiom_nonIdiom(tree):
#     transform_idiom_multi_ass(node)
#     code_list = []
#     for node in ast.walk(tree):
#         if isinstance(node, ast.Assign):
#             targets=node.targets
#             num_tar=0
#             for t in targets:
#                 num_tar+=ast_util.get_basic_count(t)
#             value=node.value
#             num_value=ast_util.get_basic_count(value)
#             if num_value==num_tar>1:
#                 transform_idiom_multi_ass(node)
#     code_list.append([test, new_code])
#     return code_list

def parse_a_tree(tree):
    code_list=[]
    old_code_list = get_idiom_set_comprehension_improve(tree)
    for code in old_code_list:
        each_code_pair = transform_idiom_list_comprehension(code[0], code[1])
        if each_code_pair:
            code_list.append(each_code_pair)

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
                old_code_list = get_idiom_set_comprehension_improve(tree)
                for code in old_code_list:
                    each_code_pair = transform_idiom_list_comprehension(code[0],code[1])
                    if each_code_pair:
                        code_list.append(each_code_pair)

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


def cp_repo_python(repo_name):
    for file_info in dict_repo_file_python[repo_name]:
        file_path = file_info["file_path"]
        dst_path = "/data/" + "/".join(file_path.split("/")[2:])
        if not os.path.isdir(dst_path):  # 如果 to_path 目录不存在，则创建
            os.makedirs(dst_path)
        shutil.copy(file_path, dst_path)


if __name__ == '__main__':
    print("begin to run code ", util.data_root)
    code = '''
# a={i for i in range(1)} and {j for j in range(1)}
info_list = {{x.strip() for x in list(g)} for (k, g) in groups if not k}
# perm_back += {max(e.axis1, e.axis2) for e in edges}
# a={e for e in w if e>2}
# a={e if e else w if w else b for e in w if e>2}
split2_episodes = {(ep.scene_id, ep.episode_id) for ep in split2_dataset.episodes}
'''
    parse_a_tree(ast.parse(code))
    '''
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
    '''
    # '''
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    # json_file=open(util.data_root + "python3_1000repos_files_info" + '.json', 'r')
    # w=json.load(json_file)
    # print("content of json: ",w)
    print("load repo info successfuly")
    # save_complicated_code_dir_pkl= util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_is_not_no_len/"
    # save_complicated_code_dir_pkl= util.data_root_mv + "idiom_code_pair/dir_pkl/multi_assign_idiom_code/"
    # save_complicated_code_dir_pkl= util.data_root_home + "idiom_code_dir_pkl/multi_assign_idiom_code/"
    save_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl_new/set_comprehension_idiom_code/"
    # complicate_code = util.load_pkl(save_complicated_code_dir_pkl, "CobaltStrikeParser")
    # print("complicate_code: ",complicate_code)
    
    import shutil

    repo_name_list = []
    for repo_name in dict_repo_file_python:
        # if repo_name!="3d-photo-inpainting":#anki
        #     continue
        # if repo_name!="TensorNetwork":#"tabula-py":#"speechpy":#"gdb-dashboard":
        #     continue
        # if os.path.exists("/home/zejun/smp/data/python_star_2000repo/" + repo_name):
        #     continue
        # print("come to the repo: ", repo_name)
        if not os.path.exists(util.pro_dir + repo_name):
            continue
        # for file_info in dict_repo_file_python[repo_name]:
        #     file_path = file_info["file_path"]
        #     dst_path = "/home/" + "/".join(file_path.split("/")[2:])
        #     if not os.path.isdir(dst_path):  # 如果 to_path 目录不存在，则创建
        #         os.makedirs(dst_path)
        #     shutil.copy(file_path, dst_path)
        repo_name_list.append(repo_name)
        # break
    # repo_name_list=["TensorNetwork"]
    print(f"it has {len(repo_name_list)} repos")
    # pool = newPool(nodes=30)
    # pool.map(cp_repo_python, repo_name_list)  # [:3]sample_repo_url ,token_num_list[:1]
    # pool.close()
    # pool.join()
    # save_repo_for_else_complicated(repo_name_list[0])
    # '''
    pool = newPool(nodes=30)
    pool.map(save_repo_for_else_complicated, repo_name_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    # '''
    # save_to_csv(save_complicated_code_dir_pkl)
    
    # save_to_csv(save_complicated_code_dir_pkl)
    # '''
