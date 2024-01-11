'''
file_name
一个测试test_filename文件, 可能存在多个filename,
对于test_filename中每个test_function() 需要知道测试的是哪个 function
'''
import sys, ast, os, copy,re,requests
sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
from bs4 import BeautifulSoup
import urllib
from datetime import datetime
import util,git,github_util,ast_util
if __name__ == '__main__':
    file_path=util.data_root +'python_star_2000repo/edx-platform/openedx/tests/completion_integration/test_views.py'
    try:
        content = util.load_file_path(file_path)
    except:
        print(f"{file_path} is not existed!")
    file_tree = ast.parse(content)
    ana_py = ast_util.Analyzer()
    ana_py.visit(file_tree)
    code_list=[]
    print("func number: ",len(ana_py.func_def_list))
    count=0
    for tree in ana_py.func_def_list:
        if hasattr(tree,"name: "):
            print("fun name: ",tree.name)
        for node in ast.walk(tree):
            if isinstance(node,ast.Call):
                print("call: ",ast.unparse(node),node.__dict__,node.__module__, node.__class__.__name__)

                # print(sys._getframe().f_code.co_filename)
                count+=1
                if  count>3:
                    break
        else:
            continue
        break

        #print("tree_ func_name",tree.__dict__)
        # code_list.extend(get_for_target(tree))