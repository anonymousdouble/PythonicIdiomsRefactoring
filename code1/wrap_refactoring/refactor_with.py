import os,sys
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
import util

from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
from extract_transform_complicate_code_new.extract_compli_with_new import get_with
from tokenize import tokenize
import ast,traceback
def refactor_with(file_path):

    content = util.load_file_path(file_path)
    new_code_list=[]
    try:
        tree=ast.parse(content)
        new_code_list = get_with(tree)

    except:
        traceback.print_exc()
    return new_code_list


def refactor_with_by_method(tree):

    new_code_list=[]
    try:
        new_code_list = get_with(tree)

    except:
        traceback.print_exc()
    return new_code_list

if __name__ == '__main__':
    #return '<a href="%s">%s</a>' % (quote(url.encode('utf-8')), anchor)
    code='''
def func():
        out_file = open(out_path, "w")
        txt_ids = []
        txt_l_path = txt_partial_path
        for txtpath in os.listdir(txt_l_path):
            print("Processing %s" % txtpath)
            full_txtpath = txt_l_path + txtpath
            name = txtpath.split(".")[0]
            wavpath_matches = [fname.split(".")[0] for fname in os.listdir(wav_partial_path)
                               if name in fname]
            for name in wavpath_matches:
                # Need an extra level here for pavoque :/
                with open(full_txtpath, 'r') as f:
                    r = f.readlines()
                if len(r) == 0:
                    continue
                if len(r) != 1:
                    new_r = []
                    for ri in r:
                        if ri != "\n":
                            new_r.append(ri)
                    r = new_r
                if len(r) != 1:
                    print("Something wrong in text extraction, cowardly bailing to IPython")
                    from IPython import embed
                    embed()
                    raise ValueError()
                assert len(r) == 1
                # remove txt extension
                text = r[0].strip()
                info_tup = (name, text)
                txt_ids.append(name)
                out_file.writelines(format_info_tup(info_tup))
        out_file.close()
'''
    tree=ast.parse(code)
    new_list=refactor_with_by_method(tree)
    print("**********")
    for e,child_node,*middle,new_with_node,new_block_node in new_list:
        print(">>>>unparse: ",ast.unparse(child_node),"\n>>>>\n",ast.unparse(new_with_node))
