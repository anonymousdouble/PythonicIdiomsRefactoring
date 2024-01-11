import os,sys
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
import util

from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
from extract_transform_complicate_code_new.extract_compli_chain_ass_value import get_ass
from tokenize import tokenize
import ast,traceback
def refactor_chain_ass(file_path):

    content = util.load_file_path(file_path)
    new_code_list=[]
    try:
        tree=ast.parse(content)
        new_code_list = get_ass(tree)

    except:
        traceback.print_exc()
    return new_code_list


def refactor_chain_ass_by_method(tree):

    new_code_list=[]
    try:
        new_code_list = get_ass(tree)

    except:
        traceback.print_exc()
    return new_code_list

if __name__ == '__main__':
    code='''
def __init__(self, plot):
    self.plot = plot
    self.full_csv_path = ''
    self.dir = ''
    self.filename = ''
    self.signals_averaging_window = 1
    self.show_bollinger_bands = False
    self.csv = None
    self.bokeh_source = None
    self.bokeh_source_orig = None
    self.last_modified = None
    self.signals = {}
    self.separate_files = False
    self.last_reload_data_fix = False
'''
    tree=ast.parse(code)
    new_list=refactor_chain_ass_by_method(tree)
    print("**********")
    for e1,e2 in new_list:
        print(">>>>unparse: ",ast.unparse(e1),"\n>>>>\n",e2)
