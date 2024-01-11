import sys,ast,os
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("../")
sys.path.append("../..")
sys.path.append("../../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")

sys.path.append("/mnt/zejun/smp/code1/")
import util,traceback
from extract_simp_cmpl_data import ast_util
import complicated_code_util

from pathos.multiprocessing import ProcessingPool as newPool


# def test_is_simple_object(e):
#
#     if isinstance(e, (ast.Compare,ast.BoolOp, ast.Call,ast.Constant)):# 这里的constant是 true false 如 while true
#         return False
#     elif isinstance(e, ast.UnaryOp):
#         if isinstance(e.op, ast.Not):
#             operand=e.operand
#             if isinstance(operand, (ast.Compare, ast.BoolOp, ast.Call,ast.Constant)):
#                 return False
#             else:
#                 return True
#
#
#     return True

def find_not_op_contains_idiom(node):
    operand=node.operand
    if isinstance(operand,(ast.Call,ast.Compare,ast.BoolOp, ast.Not)):
            return False
    return True

def get_idiom_assign_multi_improve(tree):
    code_list = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets=node.targets
            for tar in targets:
                star_count=0
                for tar_child in ast.walk(tar):
                    if isinstance(tar_child,ast.Starred):
                        star_count+=1
                        if star_count>1:
                            print("the assignment has syntax errors",ast.unparse(node))
                            continue
            # value=node.value
            # for val_child in ast.walk(value):
            #     if isinstance(val_child,ast.Starred):
            #         print("the assignment cannot be explained precisely because we cannot know the length of Starred: ",ast.unparse(node))
            #         continue
            num_tar=0
            for t in targets:
                num_tar+=ast_util.get_basic_count(t)

            if num_tar>1:
                code_list.append(node)
                # return node

            # value=node.value
            # num_value=ast_util.get_basic_count(value)
            # if num_value==num_tar>1:
            #     code_list.append([ast.unparse(node),num_value])
    return code_list
def get_idiom_for_else(tree):
    code_list = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            targets = node.targets
            num_tar = 0
            for t in targets:
                num_tar += ast_util.get_basic_count(t)
            value = node.value
            num_value = ast_util.get_basic_count(value)
            if num_value == 1 and num_tar > 1 and isinstance(value,ast.Constant) and ast.unparse(node).count("=")>1:
                # print(">>code: ",ast.unparse(node))
                code_list.append([ast.unparse(node), num_value])
    return code_list
def save_repo_for_else_complicated(repo_name):
    count_complicated_code=0
    # print("come the repo: ", repo_name)
    one_repo_for_else_code_list = []
    dict_file = dict()
    for file_info in dict_repo_file_python[repo_name]:

        file_path = file_info["file_path"]
        # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
        #     continue
        file_html = file_info["file_html"]
        file_path = util.prefix_root + "/" + file_path

        #print("come this file: ", file_path)

        try:
            content = util.load_file_path(file_path)
        except:
            print(f"{file_path} is not existed!")
            continue
        #print("content: ",content)
        try:
            file_tree = ast.parse(content)
            ana_py = ast_util.Fun_Analyzer()
            ana_py.visit(file_tree)
            dict_class = dict()
            for tree, class_name in ana_py.func_def_list:
                code_list = get_idiom_for_else(tree)
                if code_list:
                    ast_util.set_dict_class_code_list(tree, dict_class, class_name, code_list)
            if dict_class:
                dict_file[file_html] = dict_class
            # file_tree = ast.parse(content)
            # ana_py = ast_util.Analyzer()
            # ana_py.visit(file_tree)
            # #print("func number: ",file_html,len(ana_py.func_def_list))
            # for tree in ana_py.func_def_list:
            #     #print("tree_ func_name",tree.__dict__)
            #
            #     code_list=get_idiom_for_else(tree)
            #     if code_list:
            #         one_repo_for_else_code_list.append([code_list, file_path, file_html])


        except SyntaxError:

            print("the file has syntax error")

            continue

        except ValueError:

            traceback.print_exc()

            print("the file has value error: ", file_html)

            continue
        except:
            traceback.print_exc()
            print("the file has other error: ", file_html)
        #break
    util.save_pkl(save_complicated_code_dir_pkl, repo_name, dict_file)

    # if one_repo_for_else_code_list:
    #     count_complicated_code=count_complicated_code+len(one_repo_for_else_code_list)
    #     # print("it exists for else complicated code1: ", len(one_repo_for_else_code_list))
    #     util.save_json(save_complicated_code_dir, repo_name, one_repo_for_else_code_list)
    #     print("save successfully! ", save_complicated_code_dir + repo_name)

    # return count_complicated_code

if __name__ == '__main__':
    code='''
for i,(e,w) in enumerate(range(10)):
    print(i,e)
else:
    print("yes")
for i,(e,w) in enumerate(range(10)):
    print(i,e)
    for a in [1,2]:
        print(a)
    else:
        print("else")

    if i>1:
        break
else:
    print("yes")
'''
    #
    # tree = ast.parse(code1)
    # code_list=get_idiom_for_else(tree)
    # print("find these codes: ",code_list)


    save_complicated_code_dir= util.data_root + "idiom_code_dir/for_else_idiom_code_fragments/"
    #dict_repo_file_python=util.load_json(util.data_root, "python3_repos_files_info" )
    save_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl/chain_ass_same_value_idiom_code_fragments_new/"
    dict_repo_file_python= util.load_json(util.data_root, "python3_1000repos_files_info")

    #dict_repo_file_python=util.load_json(util.data_root, "python3_1000repos_files_info_modify" )

    repo_list = []

    for ind, repo_name in enumerate(dict_repo_file_python):
        #print("repo infor: ",dict_repo_file_python[repo_name])
        # if os.path.exists(save_complicated_code_dir_pkl + repo_name + ".pkl"):
        #     continue
        # print("repo_name: ", repo_name)
        repo_list.append(repo_name)
    print("count: ", len(repo_list))
    
    # '''

    pool = newPool(nodes=30)
    pool.map(save_repo_for_else_complicated, repo_list[:])  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    print(">>>>>>>>len all_files: ", len(repo_list))
    # '''
    '''
    count = 0
    file_list=set([])
    result_compli_for_else_list=[]
    for file_name in os.listdir(save_complicated_code_dir):
        complicate_code=util.load_json(save_complicated_code_dir,file_name[:-5])
        for code_list, file_path,file_html in complicate_code:
            count +=len(code_list)
            for code1 in code_list:
                repo_name=file_html.split("/")[4]
                file_list.add(file_html)
                result_compli_for_else_list.append([repo_name,code1,file_html,file_path])
            #     print("one code1: ",repo_name,code1,file_html,file_path)
            #     break
            # break
        # print("file: ",file_name)
        # break
    print("count: ", count, len(os.listdir(save_complicated_code_dir)),len(file_list))

    util.save_csv(util.data_root+"idiom_code_dir/for_else_idiom_code_fragments.csv",result_compli_for_else_list,["repo_name","code1","file_html","file_path"])
    '''
    files_num_list = []
    star_num_list = []
    contributor_num_list = []
    count_repo, file_count, me_count, code_count = 0, 0, 0, 0
    file_list = set([])
    repo_code_num = dict()
    result_compli_for_else_list = []
    all_count_repo, all_file_count, all_me_count = 0, 0, 0
    for file_name in os.listdir(save_complicated_code_dir_pkl):
        all_count_repo += 1
        repo_name = file_name[:-4]
        # files_num_list.append(repo_files_info[repo_name])
        # star_num_list.append(repo_star_info[repo_name])
        # contributor_num_list.append(repo_contributor_info[repo_name])

        complicate_code = util.load_pkl(save_complicated_code_dir_pkl, repo_name)

        repo_file_count, repo_me_count, repo_code_count, repo_all_file_count, repo_all_me_count = complicated_code_util.get_code_count(
            complicate_code)
        # for code_list, file_path, file_html in complicate_code:
        code_count += repo_code_count
        file_count += repo_file_count
        me_count += repo_me_count
        all_file_count += repo_all_file_count
        all_me_count += repo_all_me_count
        repo_exist = 0
        for file_html in complicate_code:
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    if complicate_code[file_html][cl][me]:
                        repo_exist = 1
                        break
                        # for code1 in complicate_code[file_html][cl][me]:
                        #     # print("html: ",file_html,cl,me,ast.unparse(code1[0]))
                        #     #                code_index_start_end_list.append([node,assign_stmt,node.lineno, node.end_lineno,assign_stmt_lineno,assign_block_list_str])
                        #
                        #     result_compli_for_else_list.append(
                        #         [repo_name, file_html, cl, me, code1[0]])

            # print(f"{file_html} of {repo_name} has  {len(code_list)} code1 fragments")
        count_repo += repo_exist

    # a=dict(sorted(repo_code_num.items(), key=lambda item: item[1], reverse=True))
    # print(a)
    # print(np.median(list(a.values())), np.max(list(a.values())), np.min(list(a.values())))
    # print(np.median(files_num_list), np.max(files_num_list), np.min(files_num_list))
    # print(np.median(star_num_list), np.max(star_num_list), np.min(star_num_list))
    # print(np.median(contributor_num_list), np.max(contributor_num_list), np.min(contributor_num_list))
    print("count: ", count_repo, code_count, file_count, me_count, all_count_repo, all_file_count, all_me_count)

    # print("----------------------------\n")
    # for code1 in for_else_filter_redundant_code_list:
    #     print("each code1: ", code1[0])
