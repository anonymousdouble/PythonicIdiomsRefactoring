import sys, ast, os, copy
import tokenize
import sys
sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time
import copy
import util,github_util
from extract_simp_cmpl_data import ast_util
class Rewrite(ast.NodeTransformer):
    def __init__(self,node,new_node):
        self.old_node =node
        self.new_node =new_node

    def generic_visit(self, node):
        if hasattr(node, "body"):
            if hasattr(node,"lineno"):
                if node.lineno==self.old_node.lineno and ast.unparse(node)==ast.unparse(self.old_node):
                    return self.new_node

            for ind,child in enumerate(node.body):
                    node.body[ind] = self.generic_visit(node.body[ind])
        return node






def replace_file_content_for_compre_3_category(repo_name,file_html,for_node,assign_stmt,new_code):
    real_file_html = file_html.replace("//", "/")
    rela_path = "/".join(real_file_html.split("/")[6:])
    file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
    content = util.load_file_path(file_path)
    res_copy = content.split("\n")
    indent = ""
    for ind, e in enumerate(res_copy[for_node.lineno - 1]):
        if e != " ":
            indent = " " * ind
            break


    res_copy[for_node.lineno - 1:for_node.end_lineno] = [indent + ast.unparse(new_code)]
    res_copy[assign_stmt.lineno - 1:assign_stmt.end_lineno] = [""]
    return content,"\n".join(res_copy)
def replace_content_for_else(repo_name,file_html,old_tree,new_tree):
    real_file_html = file_html.replace("//", "/")
    rela_path = "/".join(real_file_html.split("/")[6:])
    file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
    content = util.load_file_path(file_path)
    all_tree=ast.parse(content)
    rew=Rewrite(old_tree,new_tree)
    all_tree=rew.visit(all_tree)

    return content, ast.unparse(all_tree)
    '''
    # content = util.load_file_path_lines(file_path)
    # res_copy=copy.deepcopy(content)
    # print("***************content: \n","\n".join(res_copy))
    res_copy = content.split("\n")
    # print("old_content len: ",len(res_copy))
    indent = ""
    for ind, e in enumerate(res_copy[old_tree.lineno - 1]):
        if e != " ":
            indent = " " * ind
            break
    a = [indent + e for e in ast.unparse(new_tree).split("\n")]
    # print("old_tree lineno: ", old_tree.lineno ,old_tree.end_lineno,ast.unparse(old_tree),"************\n")

    if ast.unparse(old_tree).startswith(res_copy[old_tree.lineno - 1]):
        indent = ""
        for ind, e in enumerate(res_copy[old_tree.lineno - 1]):
            if e != " ":
                indent = " " * ind
                break
        a = [indent + e for e in ast.unparse(new_tree).split("\n")]
        res_copy[old_tree.lineno - 1:old_tree.end_lineno] = a
    else:
        start=old_tree.lineno - 1
        end=old_tree.end_lineno
        for i in range(1,5):
            if ast.unparse(old_tree).startswith(res_copy[start]):
                indent = ""
                for ind, e in enumerate(res_copy[old_tree.lineno - 1-i]):
                    if e != " ":
                        indent = " " * ind
                        break
                res_copy[old_tree.lineno - 1-i:old_tree.end_lineno-i] = a
                break
        else:
            for i in range(1, 5):
                if ast.unparse(old_tree).startswith(res_copy[old_tree.lineno - 1 + i]):
                    res_copy[old_tree.lineno - 1 + i:old_tree.end_lineno+ i] = a
                    break

    return content, "\n".join(res_copy)
    '''
    # return "\n".join(content), "\n".join(res_copy)
def replace_content_multi_ass(repo_name,file_html,ass_list,new_code):
    real_file_html = file_html.replace("//", "/")
    rela_path = "/".join(real_file_html.split("/")[6:])
    file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
    content = util.load_file_path(file_path)
    res_copy = content.split("\n")

    beg = ass_list[0].lineno
    end = ass_list[-1].lineno
    # print("beg,end: ",beg,end)
    indent = ""
    for ind, e in enumerate(res_copy[beg - 1]):
        if e != " ":
            indent = " " * ind
            break
    res_copy[beg - 1] = indent + new_code
    res_copy[beg - 1:end] = res_copy[beg - 1:beg]

    return content, "\n".join(res_copy)
def replace_content_chain_compar(repo_name,file_html,compl_node,sim_node):
    real_file_html = file_html.replace("//", "/")
    rela_path = "/".join(real_file_html.split("/")[6:])
    file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
    content = util.load_file_path(file_path)
    res_copy = content.split("\n")
    row_beg=compl_node.lineno
    row_end=compl_node.end_lineno
    col_beg = compl_node.col_offset
    col_end = compl_node.end_col_offset
    # print("beg,end: ",beg,end)
    indent = ""
    for ind, e in enumerate(res_copy[row_beg - 1]):
        if e != " ":
            indent= " " * ind
            break

    a = [res_copy[row_beg-1][:col_beg]+ast.unparse(sim_node)+res_copy[row_end-1][col_end:] ]
    res_copy[row_beg - 1:row_end] = a

    return content, "\n".join(res_copy)
def replace_content_truth_value_test(repo_name,file_html,compl_node,sim_node):
    real_file_html = file_html.replace("//", "/")
    rela_path = "/".join(real_file_html.split("/")[6:])
    file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
    content = util.load_file_path(file_path)
    res_copy = content.split("\n")
    row_beg = compl_node.lineno
    row_end = compl_node.end_lineno
    col_beg = compl_node.col_offset
    col_end = compl_node.end_col_offset
    # print("beg,end: ",beg,end)
    # indent = ""
    # for ind, e in enumerate(res_copy[row_beg - 1]):
    #     if e != " ":
    #         indent.append(" " * ind)
    #         break

    a = [res_copy[row_beg - 1][:col_beg] + ast.unparse(sim_node) + res_copy[row_end - 1][col_end:]]
    res_copy[row_beg - 1:row_end] = a

    return content, "\n".join(res_copy)
def replace_content_var_unpack_for_target(repo_name,file_html,compl_node,sim_node):
    real_file_html = file_html.replace("//", "/")
    rela_path = "/".join(real_file_html.split("/")[6:])
    file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
    content = util.load_file_path(file_path)
    res_copy = content.split("\n")
    beg = compl_node.lineno
    end = compl_node.end_lineno
    # print("beg,end: ",beg,end)
    indent = ""
    for ind, e in enumerate(res_copy[beg - 1]):
        if e != " ":
            indent = " " * ind
            break
    # res_copy[beg - 1] = [indent +e for e in ast.unparse(sim_node).split("\n")]
    res_copy[beg - 1:end] = [indent +e for e in ast.unparse(sim_node).split("\n")]

    return content, "\n".join(res_copy)

def replace_content_var_unpack_call_star(repo_name,file_html,arg_seq,sim_node):
    real_file_html = file_html.replace("//", "/")
    rela_path = "/".join(real_file_html.split("/")[6:])
    file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
    content = util.load_file_path(file_path)
    res_copy = content.split("\n")
    row_beg = arg_seq[0].lineno
    row_end = arg_seq[-1].end_lineno
    col_beg = arg_seq[0].col_offset
    col_end = arg_seq[-1].end_col_offset
    # indent = ""
    # for ind, e in enumerate(res_copy[row_beg - 1]):
    #     if e != " ":
    #         indent.append(" " * ind)
    #         break
    a = [res_copy[row_beg - 1][:col_beg] + ast.unparse(sim_node) + res_copy[row_end - 1][col_end:]]
    res_copy[row_beg - 1:row_end] = a

    return content, "\n".join(res_copy)


if __name__ == '__main__':
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    # save_complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_else/"
    '''
    complic_code_me_info_dir_pkl 
    {key repo_name: {
        key full_me_id: {
            file_html:  xx
            file_path: xx
            me_line_no: [{new_file_code: xx

            old_fragm_code_line:xx
            new_frgam_code_line:xx}, {...}]
        }   
    }
    complic_code_me_overload_info_dir_pkl
    {key repo_name: {
        key full_me_id: {
            file_html:  xx
            file_path: xx
            me_line_no: [
                {new_file_code: xx, old_fragm_code_line:xx, new_frgam_code_line:xx}, {...}],
            me_line_no:[]
        }  
    }
    '''
    # complicated_code_dir_pkl=util.data_root + "transform_complicate_to_simple_pkl/for_compre_set/"
    complicated_code_dir_pkl= util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/chain_comparison/"
    complicated_code_dir_pkl=util.data_root +"transform_complicate_to_simple_pkl/var_unpack_call_star_complicated/"
    complicated_code_dir_pkl=util.data_root +"transform_complicate_to_simple_pkl/var_unpack_for_target_complicated/"
    complicated_code_dir_pkl=util.data_root + "transform_complicate_to_simple_pkl/multip_assign_complicated/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/for_else/"

    # complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/for_compre_set/"#for_else
    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/truth_value_test_complicated/"#for_else
    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/chain_comparison/"#for_else
    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/var_unpack_call_star_complicated/"#for_else
    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/var_unpack_for_target_complicated/"#for_else
    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/multip_assign_complicated/"#for_else
    complic_code_me_info_dir_pkl_test = util.data_root + "complic_code_me_info_dir_pkl/each_idiom_type_all_methods/for_else/"#for_else

    # dict_repo_file_python = util.load_json(util.data_root, "jupyter3_repos_files_info")

    repo_list = []
    count_file = 0
    dict_repo_need_test_me = dict()
    dict_repo_need_test_me_overload = dict()
    result_me_info = []

    for repo_name in dict_repo_file_python:
        # if repo_name != "salt":
        #     continue
        dict_repo_need_test_me[repo_name] = dict()
        dict_repo_need_test_me_overload[repo_name] = dict()
        if not os.path.exists(complicated_code_dir_pkl+repo_name+".pkl"):
            continue
        complicate_code = util.load_pkl(complicated_code_dir_pkl, repo_name)
        for file_html in complicate_code:

            real_file_html = file_html.replace("//", "/")
            #
            # packa_pre=".".join(real_file_html.split("/")[6:])[:-3]
            rela_path = "/".join(real_file_html.split("/")[6:])
            file_path = "".join([util.data_root, "python_star_2000repo/", repo_name, "/", rela_path])
            print("file_html: ", file_html, file_path)
            content = util.load_file_path(file_path)
            with open(file_path, "r") as f:

                res = f.readlines()  # res 为列表

            for cl in complicate_code[file_html]:
                class_name = cl
                print("class name: ", cl)
                for me in complicate_code[file_html][cl]:
                    # me_name=me.split("$")[0]
                    # line_beg=me.split("$")[1]
                    if complicate_code[file_html][cl][me]:
                        #old_tree, ass,new_tree;  old_tree, new_tree;(arg_list, new_tree ) each_assign_list, new_tree, old_tree, new_tree,break_list_in_for
                        for ind, (old_tree, new_tree,break_list_in_for) in enumerate(complicate_code[file_html][cl][me]):
                            # old_tree=arg_list
                            print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ",  new_tree.lineno,ast.unparse(new_tree))#
                            print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ",old_tree.lineno,old_tree)#old_tree.lineno,arg_list
                            # print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ", ast.unparse(each_assign_list[0]),each_assign_list[0].lineno)#old_tree.lineno,

                            # print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ", ast.unparse(old_tree))#old_tree.lineno,
                            #old_content,new_content=replace_file_content_for_compre_3_category(repo_name,file_html,old_tree, ass,new_tree)
                            # old_content,new_content=replace_content_truth_value_test(repo_name,file_html,old_tree,new_tree)
                            # arg_seq=arg_list[0]
                            # old_content,new_content=replace_content_chain_compar(repo_name,file_html,old_tree,new_tree)
                            # old_content,new_content=replace_content_var_unpack_call_star(repo_name,file_html,arg_seq,new_tree)
                            # old_content,new_content=replace_content_var_unpack_for_target(repo_name,file_html,old_tree,new_tree)
                            # old_content,new_content=replace_content_multi_ass(repo_name,file_html,each_assign_list,new_tree)
                            old_content,new_content=replace_content_for_else(repo_name,file_html,old_tree,new_tree)

                            util.save_file(complic_code_me_info_dir_pkl_test, "test", new_content, ".txt", "w")
                            util.save_file(complic_code_me_info_dir_pkl_test, "test_old", old_content, ".txt", "w")
                            print(">>>>>>>>>>>>>>>>>>>>new file:\n ", new_content)
                            print(">>>>>>>>>>>>>>>>>>>>old file:\n ", old_content)
                            break
                        # for ind, (old_tree, new_tree, break_list_info) in enumerate(complicate_code[file_html][cl][me]):
                        #     print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ", new_tree.lineno, ast.unparse(new_tree))
                        #     print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ", old_tree.lineno, ast.unparse(old_tree))
                        #     replace_file_content_for_compre_3_category(repo_name,file_html,)
                        #     util.save_file(complic_code_me_info_dir_pkl_test, "test", "\n".join(res_copy), ".txt", "w")
                        #     util.save_file(complic_code_me_info_dir_pkl_test, "test_old", content, ".txt", "w")
                        #     print(">>>>>>>>>>>>>>>>>>>>new file:\n ", "\n".join(res_copy))
                        #     print(">>>>>>>>>>>>>>>>>>>>old file:\n ", content)

                        else:
                            continue
                        break
                else:
                    continue
                break
            else:
                continue
            break
        else:
            continue
        break

