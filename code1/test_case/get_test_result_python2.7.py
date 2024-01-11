import sys, ast, os, copy
import tokenize
import sys
sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time
import util,github_util
'''
1. install project 所需要的packages
2. module路径添加
3. command line的结果存储
'''
# 创建一个虚拟环境，安装所有的包
from subprocess import Popen, PIPE, STDOUT
def findfile(start, name):
    for file in os.listdir(start):
        # if "requirements" in file and ".txt" in file:
        if name in file:
            full_path = os.path.join(start, "", name)
            return (os.path.normpath(os.path.abspath(full_path)))
    return None

def findreq(start, name=""):
        all_require=[]
        for file in os.listdir(start):
            if "requirements" in file and ".txt" in file:

                full_path = os.path.join(start, "", file)
                all_require.append(os.path.normpath(os.path.abspath(full_path)))
        return all_require
    # for relpath, dirs, files in os.walk(start):
    #     # print(relpath,dirs)
    #     if "venv_test" in relpath:
    #         continue
    #     if name in files:
    #         full_path = os.path.join(start, relpath, name)
    #         return (os.path.normpath(os.path.abspath(full_path)))
    # return None
def create_virtual_envi(pro_path,v="9"):
    return "".join(["cd ", pro_path, " ; python2.",v," -m virtualenv venv_test_",v, " ; . ./","venv_test_",v,"/bin/activate"])
    # return "".join(["cd ", pro_path, "&& python2 -m pip install virtualenv && python2 -m virtualenv venv_test && . ./venv_test/bin/activate"])

def export_python_path(pro_path,relative_test_file_path):
    dir_up = os.path.dirname(pro_path + relative_test_file_path)
    # print("first dir: ",dir_up)
    init_module = ["export PYTHONPATH=" + dir_up]
    all_own_modules = []
    while dir_up != pro_path[:-1]:
        dir_upup = os.path.dirname(dir_up)
        all_own_modules.append(dir_upup)
        # print(dir_up, dir_upup)
        dir_up = dir_upup
    return ":".join(init_module+all_own_modules)
def pip_install(pro_path,v="9",split_install="*************************install*************************"):
    cmd_pip_pack = ""
    require_full_path = findfile(pro_path, "setup.py")
    if 1!=1:#require_full_path:#1!=1:#
        # cmd_pip_pack = "".join(["python2 ", require_full_path, " install "])
        cmd_pip_pack = "".join(["echo '",split_install,"' ; python2.",v, " ",require_full_path, " install "," ;echo '",split_install,"'"])
    else:
        require_full_path = findreq(pro_path)
        cmd_pip_pack = ["echo '", split_install, "' ;"]
        if require_full_path:
            for require in require_full_path:
                cmd_pip_pack += ["pip2.", v, " install -r ", require, " ;"]

            cmd_pip_pack = "".join(cmd_pip_pack + ["echo '", split_install, "'"])

    return cmd_pip_pack
def make_cmd_test(pro_path,relative_test_file_path,file_name,fun_list=[]):
    whether_same=relative_test_file_path.split("/")
    if len(set(whether_same))==len(whether_same):#可能有同名的module名https://github.com/nodejs/node-gyp/tree/master/gyp/pylib/gyp/input_test.py

        file_name = ".".join(relative_test_file_path.split("/")) + file_name[:-3]
        print("file_name: ",file_name)
        relative_test_file_path=""

    cmd_test = ["echo ","$PYTHONPATH;","cd ", pro_path + relative_test_file_path, " ;"]# echo '", split_test_str, "' ; "]
    if not fun_list:
        cmd_test += ["python2.", v, " -m unittest -v ", file_name," ;"]

        pass
    else:
        # cmd_test="".join(["cd ", pro_path+relative_test_file_path," && ","python2 -m unittest ",file_name])
        cmd_test += ["python2.", v, " -m unittest -v ", fun_list, " ;"]
        # for fun in fun_list:
        #     cmd_test += ["python3.", v, " -m unittest -v ", file_name[:-3] + "." + fun, " ;"]
        # cmd_test = "".join(cmd_test + ["echo '", split_test_str, "'"])
    return cmd_test
if __name__ == '__main__':
    pro_path=util.data_root+"python_star_2000repo/"#"cloud-custodian/"#"django/"#node-gyp#bert#sentence-transformers
    pro_path+="oppia/"#"lbry-sdk/"#"node-gyp/"#"cloud-custodian/"#"security_monkey/"
    v="7"

    cmd_virtu=create_virtual_envi(pro_path,v)#"".join(["cd ", pro_path," && python3.9 -m venv venv_test && . ./venv_test/bin/activate"])
    cmd_pip_pack = pip_install(pro_path,v)
    relative_test_file="scripts/linters/codeowner_linter_test.py"#"tests/unit/wallet/test_wallet.py"#"security_monkey/tests/core/test_auditor.py"#"gyp/pylib/gyp/input_test.py"#"tests/test_policy.py"#"gyp/pylib/gyp/input_test.py"
    relative_test_file_path="/".join(relative_test_file.split("/")[:-1])+"/"
    print("relative_test_file_path: ",relative_test_file_path)
    file_name=relative_test_file.split("/")[-1]
    # relative_test_file_path="gyp/pylib/gyp/"#"tests/"#"tests/forms_tests/field_tests/"#"gyp/pylib/gyp/"#"gyp/pylib/gyp/generator/"
    # file_name="input_test.py"#test_policy.py "tokenization_test.py"#"test_base.py"#"input_test.py"#"msvs_test.py" #test_util.py
    cmd_export_python=export_python_path(pro_path,relative_test_file_path)#":".join(init_module+all_own_modules)
    # cmd_pip_pack+= " && pip install tensorflow==1.11.0"
    fun_list=[]#类名.方法名
    # fun_list=[file_name[:-3]+".TokenizationTest.test_basic_tokenizer_lower",file_name[:-3]+".TokenizationTest.test_is_punctuation","optimization_test.OptimizationTest.test_adam"]
    # fun_list=" ".join(fun_list)
    split_test_str = "*************************test*************************"
    cmd_test= ["echo '", split_test_str, "' ; "]
    cmd_test +=make_cmd_test(pro_path, relative_test_file_path, file_name,fun_list)
    cmd_test = "".join(cmd_test + [" echo '", split_test_str, "'"])

    if cmd_pip_pack:
        print("it has requirements: ",cmd_pip_pack)
        total_cmd=" ; ".join([cmd_virtu,cmd_export_python,cmd_pip_pack,cmd_test])#,cmd_test
    else:
        print("it does not have requirements: ")
        total_cmd = " ; ".join([cmd_virtu,cmd_export_python, cmd_test])#, cmd_test

    # print("*************************prepare install dependency and set up self-defined path*************************")
    # with os.popen(total_cmd) as process:
    #     content = process.read()
    #     print(content)
    import subprocess
    result = subprocess.run(total_cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    std_out_res=result.stdout.decode("utf-8")
    # std_out_res=result.stdout.decode("utf-8").split("*************************test*************************")
    # if len(std_out_res)==3:
    #     test_res=std_out_res[1]
    #     print("test_result: \n",test_res)

    std_error= result.stderr.decode("utf-8") if result.stderr else ""
    std_args=result.args
    # print("\n".join(result.stdout.decode("utf-8").split("*************************test*************************")))
    print("std_out_res: \n",std_out_res)
    print("std_error: \n",std_error)
    print("std_args: \n",std_args)
#CompletedProcess(args='echo Hello ; echo World', returncode=0, stdout=b'Hello\nWorld\n')
#
# a=subprocess.Popen("'''"+total_cmd+"'''",shell=True)
#
# print(a)
# print("*************************begin test the method*************************")
# with os.popen(cmd_test) as process:
#     content = process.read()
#     print(content)
# print("*************************begin test the method*************************")
# '''