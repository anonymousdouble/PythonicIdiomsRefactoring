import sys,ast,os
import tokenize
import traceback
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+'extract_transform_complicate_code_new/')
sys.path.append(code_dir+'extract_transform_complicate_code_new/comprehension/')

import complicated_code_util
import util,copy
from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
import extract_compli_for_comprehension_logic
from transform_c_s import transform_comprehension_set_compli_to_simple
from tokenize import tokenize
from io import BytesIO
import extract_compli_for_comprehension_logic
def refactor_set_comprehension(file_path):

    content = util.load_file_path(file_path)
    new_code_list=[]
    try:
        tree=ast.parse(content)
        # print("content: ",content)
        tree_copy = copy.deepcopy(tree)
        new_code_list = extract_compli_for_comprehension_logic.get_complicated_for_comprehen_code_list(tree_copy, content,
                                                                                                       ["set()"], "add")

        for ind, (for_node, assign_node, remove_ass_flag,extend_flag) in enumerate(new_code_list):
            new_code_list[ind].append(transform_comprehension_set_compli_to_simple.transform(for_node, assign_node,extend_flag))
            for node_for in ast.walk(tree):
                if isinstance(node_for,ast.For) and node_for.lineno==for_node.lineno:
                    new_code_list[ind][0]=node_for
                    break
        # for for_node, assign_node, remove_ass_flag,new_tree in new_code_list:
        #     print("old_code: ",ast.unparse(for_node),remove_ass_flag)
        #     print("new_code: ",ast.unparse(new_tree))
        #     print("**********************")

    except:
        traceback.print_exc()
    return new_code_list

def refactor_set_comprehension_by_method(tree):
    new_code_list = []
    try:
        new_code_list = extract_compli_for_comprehension_logic.get_complicated_for_comprehen_code_list(tree, "",
                                                                                                       ["set()"], "add")
        for ind, (for_node, assign_node, remove_ass_flag) in enumerate(new_code_list):
            new_code_list[ind].append(transform_comprehension_set_compli_to_simple.transform(for_node, assign_node))
    except:
        traceback.print_exc()
    return new_code_list
