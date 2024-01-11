import sys,ast,os

sys.path.append("../")
import time,complicated_code_util
import util
from pathos.multiprocessing import ProcessingPool as newPool
from transform_c_s import transform_with_compli_to_simple
from extract_simp_cmpl_data import ast_util
from pathos.multiprocessing import ProcessingPool as newPool
import traceback
'''
input: 代码片段 code1
if if,while,assert节点
    if test是compare节点
        
elif if boolOP节点
    if values 中含有compare 节点


'''
#https://runebook.dev/en/docs/numpy/reference/generated/numpy.ndarray.__bool__
def decide_compare_complicate_truth_value(test):
    flag=0
    ops = test.ops
    left = ast.unparse(test.left)
    comparators = test.comparators
    comp_str = ast.unparse(comparators[0])

    empty_list = ["None", "True", "False", "0", "0.0", "0j", "Decimal(0)", "Fraction(0, 1)", "''", "()","[]", "{}", "dict()", "set()", "range(0)"]

    if len(ops) == 1 and isinstance(ops[0], (ast.Eq, ast.NotEq)):
        if left in empty_list or comp_str in empty_list:
            flag=1
    # print("decide_compare_complicate_truth_value: ",left,comp_str,comp_str=="''",comp_str in empty_list,flag)
    return flag
#node, node.body, code_list, 0
def detection_with(tree,node,block,flag):
    code_list=[]
    if not isinstance(block, ast.AST):
        for child_node in block:
            # 对每一个stmt语句找是否含有open函数调用
            if isinstance(child_node, ast.stmt):
                for ind,e_node in enumerate(ast.walk(child_node)):
                    if ind and isinstance(e_node,ast.stmt):
                        # print(">>>has other stmt: ",ast.unparse(child_node))
                        break
                else:
                    # print(">>>come here:\n",ast.unparse(child_node))
                    if not isinstance(child_node,ast.With):
                        flag_use_after_block=1
                        for ind,e_node in enumerate(ast.walk(child_node)):
                            if isinstance(e_node, ast.Call) and ast.unparse(e_node.func) == "open" :
                                pass
                                # print(">>>come here: ",ast.unparse(child_node))
                                if isinstance(child_node, ast.Assign) and ast.unparse(child_node.value) == ast.unparse(e_node):
                                    tar = child_node.targets[0]
                                    for child_node_a in ast.walk(tree):

                                        if hasattr(child_node_a,'lineno') and hasattr(node,'end_lineno') and child_node_a.lineno > node.end_lineno:
                                            for e_child_node in ast.walk(child_node_a):
                                                # print(">>>>>child_node.lineno: ",ast.unparse(child_node_a))
                                                if ast.unparse(e_child_node) == ast.unparse(tar):
                                                    flag_use_after_block=0
                                                    break
                                        # elif hasattr(child_node_a, 'lineno'):
                                        #     for e_child_node in ast.walk(child_node_a):
                                        #         # print(">>>>>child_node.lineno: ",ast.unparse(child_node_a))
                                        #         if ast.unparse(e_child_node) == ast.unparse(tar):
                                        #             flag_use_after_block=0
                                        #             break


                                if flag_use_after_block:
                                    # print("come here")

                                    new_with_node,new_block_node=transform_with_compli_to_simple.transform_c_s_with(node,block,child_node,e_node,flag)
                                    # do transformation
                                    if new_with_node:

                                        # print("with_non_idiomatic_code: ",ast.unparse(child_node),"\n*****\n",ast.unparse(node),"\n*****\n",ast.unparse(new_block_node))
                                        # call(open), child_node: stmt_call, node: block_node, new_with_node: , new_block_node:
                                        code_list.append([e_node, child_node, node,new_with_node,new_block_node])
                                break
    return code_list
def get_with(tree):
    code_list = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and ast.unparse(node.func) == "open":
            parent_node=ast_util.find_parent_node(tree, node)
            block_node=ast_util.find_parent_node(tree, node)
            while not isinstance(parent_node,ast.stmt):
                parent_node = ast_util.find_parent_node(tree, parent_node)
            while not hasattr(block_node,"orelse") and not hasattr(block_node,"body"):
                block_node = ast_util.find_parent_node(tree, block_node)
            # print("block_node: ",block_node)
            if isinstance(parent_node, ast.With):
                continue
            flag_use_after_block = 1

            if isinstance(parent_node, ast.Assign) and ast.unparse(parent_node.value) == ast.unparse(node):
                tar = parent_node.targets[0]
                for child_node_a in ast.walk(tree):

                    if hasattr(child_node_a, 'lineno') and hasattr(node,
                                                                   'end_lineno') and child_node_a.lineno > block_node.end_lineno:
                        for e_child_node in ast.walk(child_node_a):
                            # print(">>>>>child_node.lineno: ",ast.unparse(child_node_a))
                            if ast.unparse(e_child_node) == ast.unparse(tar):
                                flag_use_after_block = 0
                                break
                        else:
                            continue
                        break
            if flag_use_after_block:
                # print("come here")
                if hasattr(block_node, "body"):
                    new_with_node, new_block_node = transform_with_compli_to_simple.transform_c_s_with(block_node,
                                                                                                       block_node.body,
                                                                                                       parent_node,
                                                                                                       node, 0)
                    if new_with_node:
                        # print(">>>>new_with_node: ",ast.unparse(new_with_node))
                        code_list.append([node, parent_node, new_with_node, new_block_node])

                if hasattr(block_node, "orelse"):
                    new_with_node, new_block_node = transform_with_compli_to_simple.transform_c_s_with(block_node,
                                                                                                       block_node.orelse,
                                                                                                       parent_node,
                                                                                                       node, 1)
                    if new_with_node:
                        # print(">>>>new_with_node: ",ast.unparse(new_with_node))
                        code_list.append([node, parent_node, new_with_node, new_block_node])
                    # code_list.append([node, parent_node, new_with_node, new_block_node])                                                                                  node, 1)

            # do transformation
                # if new_with_node:
                #     # print("with_non_idiomatic_code: ",ast.unparse(child_node),"\n*****\n",ast.unparse(node),"\n*****\n",ast.unparse(new_block_node))
                #     # call(open), child_node: stmt_call, node: block_node, new_with_node: , new_block_node:
                #     code_list.append([node, parent_node, new_with_node, new_block_node])                                                                                  node, 1)

    return code_list
def save_repo_for_else_complicated(repo_name):
    start=time.time()
    count_complicated_code = 0
    # print("come the repo: ", repo_name)
    one_repo_for_else_code_list = []

    dict_file=dict()
    # print("dict_repo_file_python[repo_name]: ",dict_repo_file_python[repo_name])
    # if os.path.exists(save_complicated_code_dir_pkl + repo_name + ".pkl"):
    #     print("the repo has been saved before")
    #     return None
    if 1:#not os.path.exists(save_complicated_code_dir_pkl + repo_name + ".pkl"):
        for ind,file_info in enumerate(dict_repo_file_python[repo_name]):

            file_path = file_info["file_path"]
            file_path=util.prefix_root+"/"+file_path
            # if file_path!="/mnt/zejun/smp/data/python_repo_1000/VideoPose3D//run.py":
            #     continue
            file_html = file_info["file_html"]
            # if file_html != "https://github.com/google/TensorNetwork/tree/master/tensornetwork/block_sparse/blocksparsetensor.py":  # "https://github.com/tanghaibao/goatools/tree/master/goatools/go_enrichment.py":#"https://github.com/microsoft/msticpy/tree/master/msticpy/sectools/syslog_utils.py":#"https://github.com/chezou/tabula-py/tree/master/tabula/io.py":#"https://github.com/astorfi/speechpy/tree/master/speechpy/feature.py":#"https://github.com/pytoolz/toolz/tree/master/toolz/functoolz.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#"https://github.com/huggingface/transformers/tree/master/src/transformers/trainer_pt_utils.py":#"https://github.com/pytransitions/transitions/tree/master/transitions/core.py":#"https://github.com/google/yapf/tree/master/yapf/yapflib/file_resources.py":#"https://github.com/zalando/patroni/tree/master/patroni/ctl.py":#"https://github.com/pymc-devs/pymc/tree/master/pymc/sampling.py":#"https://github.com/smicallef/spiderfoot/tree/master//sflib.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#
            #     continue
            # if file_html != "https://github.com/chezou/tabula-py/tree/master/tabula/io.py":  # "https://github.com/astorfi/speechpy/tree/master/speechpy/feature.py":#"https://github.com/pytoolz/toolz/tree/master/toolz/functoolz.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#"https://github.com/huggingface/transformers/tree/master/src/transformers/trainer_pt_utils.py":#"https://github.com/pytransitions/transitions/tree/master/transitions/core.py":#"https://github.com/google/yapf/tree/master/yapf/yapflib/file_resources.py":#"https://github.com/zalando/patroni/tree/master/patroni/ctl.py":#"https://github.com/pymc-devs/pymc/tree/master/pymc/sampling.py":#"https://github.com/smicallef/spiderfoot/tree/master//sflib.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#
            #     continue
            # if file_html!="":#"https://github.com/astorfi/speechpy/tree/master/speechpy/feature.py":#"https://github.com/vt-vl-lab/3d-photo-inpainting/tree/master//mesh.py":
            #     continue

            try:
                content = util.load_file_path(file_path)
            except:
                print(f"{file_path} is not existed!")
                continue

            # print("content: ",content)
            try:
                # print("come here")
                file_tree = ast.parse(content)
                ana_py = ast_util.Fun_Analyzer()
                ana_py.visit(file_tree)
                # print("ana_py.func_def_list ", ana_py.func_def_list)
                # dict_file["repo_name"]=repo_name


                dict_class=dict()
                for tree, class_name in ana_py.func_def_list:

                    new_code_list=get_with(tree)
                    # print("new_code_list ", new_code_list)
                    #
                    # for old_code,new_code in new_code_list:
                    #      print("old_code,new_code: ",ast.unparse(old_code),ast.unparse(new_code))
                    ast_util.set_dict_class_code_list(tree,dict_class, class_name, new_code_list)


                dict_file[file_html]=dict_class



            except SyntaxError:
                print("the file has syntax error")
                continue
            except ValueError:
                print("the file has value error: ", content, file_html)
                continue
            # break
        end = time.time()
        #'''
        if dict_file:
            count_complicated_code = count_complicated_code + len(one_repo_for_else_code_list)
            # print("it exists for else complicated code1: ", len(one_repo_for_else_code_list))
            util.save_pkl(save_complicated_code_dir_pkl, repo_name, dict_file)
            # util.save_json(save_complicated_code_dir, repo_name, one_repo_for_else_code_list)
            print(end-start," save successfully! ", save_complicated_code_dir_pkl + repo_name)
        else:
            print(end-start," the repo has no with")
            util.save_pkl(save_complicated_code_dir_pkl, repo_name, dict_file)
            # util.save_json(save_complicated_code_dir, repo_name, one_repo_for_else_code_list)
        #'''
        # return count_complicated_code
if __name__ == '__main__':
    code='''
if self . get_conf_value ( 'show' , header = header ) == [ ] :
    pass
elif stats_grab == { } :
    pass
assert policy . remember ( pretend . stub ( ) , pretend . stub ( ) ) == 0
while a!=[]:
    pass

'''



    # ana_py = Analyzer()
    # ana_py.visit(file_tree)
    # print("fun number: ",len(ana_py.func_def_list))

    save_complicated_code_dir= util.data_root + "complicated_code_dir/truth_value_test_complicated/"
    save_complicated_code_dir_pkl= util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_is_not/"
    save_complicated_code_dir_pkl= util.data_root + "transform_complicate_to_simple_pkl/with_complicated/"
    save_complicated_code_dir_pkl= util.data_root + "transform_complicate_to_simple_pkl/with_complicated_remove_after_block_use_f/"

    #dict_repo_file_python=util.load_json(util.data_root, "python3_repos_files_info" )
    # dict_repo_file_python=util.load_json(util.data_root, "python3_1000repos_files_info_modify" )
    dict_repo_file_python= util.load_json(util.data_root, "python3_1000repos_files_info")


    repo_name_list=[]
    for ind,repo_name in enumerate(dict_repo_file_python):
        # print(dict_repo_file_python[repo_name])
        # if repo_name!="3d-photo-inpainting":#anki
        #     continue
        # if repo_name!="TensorNetwork":#"tabula-py":#"speechpy":#"gdb-dashboard":
        #     continue
        # if os.path.exists(save_complicated_code_dir_pkl + repo_name + ".pkl"):
        #
        #     continue

        # if 5>ind:
            # break
        repo_name_list.append(repo_name)
        # else:

    # save_repo_for_else_complicated(repo_name_list)
    print("len of repo: ",len(repo_name_list))
    # repo_name_list=['micropython-lib']
    '''
    count_complicated_code=0
    for ind,repo_name in enumerate(dict_repo_file_python):
        one_repo_truth_value_test_code_list = []
        for file_info in dict_repo_file_python[repo_name]:
            file_path = file_info["file_path"]
            file_html = file_info["file_html"]
            content = util.load_file(file_path)
            try:
            #if 1:
                one_file_truth_value_test_code_list=get_truth_value_test(content)
                count_complicated_code+=len(one_file_truth_value_test_code_list)
                if one_file_truth_value_test_code_list:
                    one_repo_truth_value_test_code_list.append([one_file_truth_value_test_code_list, file_path, file_html])
                    # print("one_file_truth_value_test_code_list: ",one_file_truth_value_test_code_list)
                    # break
            except SyntaxError:
                print("the file has syntax error")
                continue
            # break
        if one_repo_truth_value_test_code_list:
            # print("it exists truth value test complicated code1: ", len(one_repo_for_else_code_list))
            util.save_json(save_complicated_code_dir, repo_name, one_repo_truth_value_test_code_list)

        # break
    # print()


        # break
    print("count_complicated_code: ",ind,count_complicated_code)
    
    '''
    '''
    pool = newPool(nodes=30)
    pool.map(save_repo_for_else_complicated, repo_name_list)  # [:3]sample_repo_url ,token_num_list[:1]
    pool.close()
    pool.join()
    # print("len all_files: ", len(all_files))
    '''
    # '''
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
                        for code in complicate_code[file_html][cl][me]:
                            # print("html: ",file_html,cl,me,ast.unparse(code1[0]))
                            #                code_index_start_end_list.append([node,assign_stmt,node.lineno, node.end_lineno,assign_stmt_lineno,assign_block_list_str])
                            result_compli_for_else_list.append(
                                [repo_name, file_html, cl, me, code[0].lineno,
                                 ast.unparse(code[0]),ast.unparse(code[2]),
                                 ast.unparse(code[-2]),
                                 ast.unparse(code[-1])])

                            # result_compli_for_else_list.append(
                            #     [repo_name, file_html, cl, me, code[0].lineno,ast.unparse(code[0]), ast.unparse(code[1])])

            # print(f"{file_html} of {repo_name} has  {len(code_list)} code1 fragments")
        count_repo += repo_exist

    # a=dict(sorted(repo_code_num.items(), key=lambda item: item[1], reverse=True))
    # print(a)
    # print(np.median(list(a.values())), np.max(list(a.values())), np.min(list(a.values())))
    # print(np.median(files_num_list), np.max(files_num_list), np.min(files_num_list))
    # print(np.median(star_num_list), np.max(star_num_list), np.min(star_num_list))
    # print(np.median(contributor_num_list), np.max(contributor_num_list), np.min(contributor_num_list))
    import random

    # util.save_csv(util.data_root + "result_csv/with_make_code_idiomatic.csv", result_compli_for_else_list,
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code_call", "old_code_with",
    #                "new_code_with", "new_code_block_node"])

    util.save_csv(util.data_root + "result_csv/with_make_code_idiomatic_remove_after_block_use_f_all.csv", result_compli_for_else_list,
                  ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code_call", "old_code_with",
                   "new_code_with", "new_code_block_node"])

    random.shuffle(result_compli_for_else_list)
    # util.save_csv(util.data_root + "result_csv/with_make_code_idiomatic.csv", result_compli_for_else_list[:400],
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code_call", "old_code_with", "new_code_with","new_code_block_node"])
    #
    util.save_csv(util.data_root + "result_csv/with_make_code_idiomatic_remove_after_block_use_f.csv", result_compli_for_else_list[:400],
                  ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code_call", "old_code_with",
                   "new_code_with", "new_code_block_node"])

    # util.save_csv(util.data_root + "result_csv/truth_value_test_remove_line.csv", result_compli_for_else_list,
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code"])

    # util.save_csv(util.data_root + "result_csv/truth_value_test.csv", result_compli_for_else_list[:400],
    #               ["repo_name", "file_html", "class_name", "me_name", "line_no", "old_code", "new_code"])

    print("count: ", count_repo, code_count, file_count, me_count, all_count_repo, all_file_count, all_me_count)
    #count:  2901 17954 9281 14132 7638 474926 4266514
    # 791 2010 103165 1291 800 121348 1192868
    # util.save_csv(util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_isnot.csv", result_compli_for_else_list,
    #               ["repo_name", "file_html", "class_name", "me_name", "for_code", "assign_code"])

    # '''




    # #'''
    # count=0
    # result_compli_for_else_list=[]
    # for file_name in os.listdir(save_complicated_code_dir):
    #     complicate_code=util.load_json(save_complicated_code_dir,file_name[:-5])
    #     for code_list, file_path,file_html in complicate_code:
    #         count += len(code_list)
    #         for code1 in code_list:
    #             repo_name=file_html.split("/")[4]
    #             result_compli_for_else_list.append([repo_name,code1,file_html,file_path])
    #         #     print("one code1: ",repo_name,code1,file_html,file_path)
    #         #     break
    #         # break
    #     # print("file: ",file_name)
    #     # break
    # print("count: ",count,len(os.listdir(save_complicated_code_dir)))
    # util.save_csv(util.data_root+"complicated_code_dir/truth_value_test_complicated.csv",result_compli_for_else_list,["repo_name","code1","file_html","file_path"])
    #'''











    # print("----------------------------\n")
    # for code1 in for_else_filter_redundant_code_list:
    #     print("each code1: ", code1[0])
