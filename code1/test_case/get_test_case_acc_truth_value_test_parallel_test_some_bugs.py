
import sys, ast, os, copy
import tokenize
import sys,shutil

sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/test_case")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import time
import util, github_util
import replace_content_by_ast
import confiure_pro_envior_by_requirements
import subprocess
from pathos.multiprocessing import ProcessingPool as newPool
# 统计某一种化繁为简的代码中，有多少的repo, files, methods, complicated code1 fragments 中存在可以运行的测试用例
def get_comp_code_can_test_me(repo_name):
    dict_complica_me_list = dict()
    full_test_me_list = []
    dict_test_html_each_me_res = util.load_pkl(save_test_file_res_dir, repo_name)
    dict_intersect_test_methods = util.load_pkl(save_me_test_me_dir, repo_name)

    for test_html in dict_test_html_each_me_res:
        if dict_test_html_each_me_res[test_html]:
            full_test_me_list.extend(dict_test_html_each_me_res[test_html]['test_methods'])

    for file_html in dict_intersect_test_methods:
        dict_complica_me_list[file_html]=dict()
        for complic_me in dict_intersect_test_methods[file_html]:
            dict_complica_me_list[file_html][complic_me] = []
            dict_test_info = dict()
            # print(complic_me, dict_intersect_test_methods[file_html][complic_me])
            complica_code_fragments_num = dict_intersect_test_methods[file_html][complic_me]['complica_num']
            test_me_of_compl_code = []
            for test_case_html, cl, me in dict_intersect_test_methods[file_html][complic_me]["test_pair"]:
                real_file_html = test_case_html.replace("//", "/")
                path_list = real_file_html.split("/")[6:]
                path_list[-1] = path_list[-1][:-3]
                rela_path = ".".join(path_list)

                if cl:
                    total_test_me_name = ".".join([rela_path, cl, me])
                else:
                    total_test_me_name = ".".join([rela_path, me])
                test_me_of_compl_code.append(total_test_me_name)
                dict_test_info[total_test_me_name] = [test_case_html, rela_path, cl, me]
            for e in set(test_me_of_compl_code) & set(full_test_me_list):
                dict_complica_me_list[file_html][complic_me].append(dict_test_info[e])
    return dict_complica_me_list


def get_total_name(file_html,cl,me_name):
    map_file_name = file_html.split("/")[-1][:-3]
    real_file_html = file_html.replace("//", "/")
    rela_path = ".".join(real_file_html.split("/")[6:-1])

    if rela_path:
        total_name = ".".join([rela_path, map_file_name, cl, me_name])
    else:
        total_name = ".".join([map_file_name, cl, me_name])
    total_name = total_name.replace("..", ".")
    return total_name
'''
首先获得有可以运行的测试用例的complicated code的测试用例信息
'''
'''
def get_test_acc():
    res=[]
    # for each repo
    me_count=0
    file_count=0
    repo_count=0
    complic_code_count=0
    total_count=0
    total_acc_count=0

    for file in os.listdir(save_test_file_res_dir):


        repo_name=file[:-4]
        repo_fla = 0
        # if repo_name != "spiderfoot":
        #     continue
        print("come to the repo: ", file)
        repo_path=pro_path + repo_name + "/"
        dict_complica_me_list = get_comp_code_can_test_me(repo_name)
        # print("dict_complica_me_list: ", dict_complica_me_list)
        complicate_code = util.load_pkl(complicated_code_dir_pkl, repo_name)
        for file_html in complicate_code:
            flag_file=0
            if file_html in dict_complica_me_list:

                # if file_html!="https://github.com/smicallef/spiderfoot/tree/master//sflib.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#
                #     continue

                print("come the file_html: ",file_html)
                for cl in complicate_code[file_html]:

                    for me in complicate_code[file_html][cl]:
                        me_name = me.split("$")[0]
                        if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
                            continue
                        total_name=get_total_name(file_html,cl,me_name)

                        if total_name in dict_complica_me_list[file_html]:
                            test_me_inf_list=dict_complica_me_list[file_html][total_name]
                            if complicate_code[file_html][cl][me] and test_me_inf_list:
                                flag_file=1
                                repo_fla=1
                                me_count+=1
                                for ind, (old_tree, new_tree) in enumerate(
                                    complicate_code[file_html][cl][me]):
                                    complic_code_count += 1
                                    # print("come to complicate_code: ", file_html)
                                    # print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ", new_tree.lineno, ast.unparse(new_tree))  #
                                    # print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ", old_tree.lineno,
                                    #       ast.unparse(old_tree))  # old_tree.lineno,arg_list

                                    total_count+=1

                                    # old_content, new_content = replace_content.replace_content_for_else(repo_name, file_html, old_tree,new_tree)
                                    old_content, new_content,flag_same = replace_content_by_ast.replace_content_truth_value_test(repo_name, file_html, old_tree,new_tree)
                                    if flag_same:
                                        print("please check because the code1 is not changed: ", file_html)
                                        continue
                                    # print(">>>>>>>>>>old_content: ", old_content)

                                    real_file_html = file_html.replace("//", "/")
                                    rela_path =  real_file_html.split("/")[6:]
                                    old_path = repo_path + "/".join(rela_path)
                                    # util.save_file_path(old_path, new_content)
                                    rela_path[-1]="".join([rela_path[-1][:-3],"_copy_zejun",".py"])
                                    # print(">>>>>>>>>>new_content: ", new_content)
                                    rela_path="/".join(rela_path)
                                    # print(repo_path+rela_path)
                                    util.save_file_path(repo_path+rela_path, old_content)# copy 一份原来的文件防止失去

                                    test_info = []

                                    for test_html,each_rela_path, cl, me in test_me_inf_list:
                                        # test_html_list=test_html.split("/")
                                        # test_html_list[-1] = "".join([test_html_list[-1][:-3],"_copy_zejun",".py"])
                                        # test_html_list="/".join(test_html_list)
                                        fun_list = [ "::".join([cl,me])if cl else me]
                                        test_info.append([test_html,cl, me])
                                        # test_content=util.load_file_path(old_path)
                                        # print(">>>>>>>>>>test_content: ",test_content)
                                        run_test_result = confiure_pro_envior_by_requirements.run_test_file(test_html, repo_path,fun_list=fun_list)
                                        # print(">>>>>>>>>>run_test_result: ", run_test_result)
                                        dict_me_re, flag_pass = confiure_pro_envior_by_requirements.get_test_result(run_test_result)
                                        print(">>>>>>>>>>dict_me_re: ",dict_me_re,flag_pass)

                                        if not flag_pass:
                                            util.save_file_path(old_path, old_content)
                                            res.append(
                                                [repo_name, file_html,test_info,str(flag_pass),ast.unparse(old_tree), ast.unparse(new_tree)])
                                            # print(">>>>>>>>>>old_content: ", old_content)

                                            break
                                    else:

                                        total_acc_count+=1

                                        util.save_file_path(old_path, old_content)
                                        res.append([repo_name, file_html, test_info,str(1),ast.unparse(old_tree), ast.unparse(new_tree)])
                                        # print(repo_path + rela_path)
                                        break
                                    # util.save_file_path(old_path, old_content)
        #     file_count+=flag_file
        # repo_count+=repo_fla
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
                                    # util.save_file_path(repo_path+rela_path, old_content)
    print(total_acc_count,total_count)
    print("repo_count,file_count,me_count,complic_code_count:",repo_count,file_count,me_count,complic_code_count)
    util.save_csv(save_acc_res_csv_dir,
                  res,
                  ["repo_name", "file_html", "test_html_list","flag_pass", "old_code", "new_code"])


    return total_acc_count/total_count
'''
'''
首先获得有可以运行的测试用例的complicated code的测试用例信息
'''
def get_each_repo_test_acc(file):
    res=[]
    # for each repo
    file_list = set([])
    me_list = set([])
    me_count=0
    file_count=0
    repo_count=0
    complic_code_count=0
    total_count=0
    total_acc_count=0
    if 1:
    # for file in os.listdir(save_test_file_res_dir):
        dict_test_acc = {'total_count': 0, 'total_acc_count': 0, 'repo_count': 0, 'file_count': 0,
                     'me_count': 0, 'complic_code_count': 0, "record_res": [], 'me_list': set([]), 'file_list': set([])}

        repo_name=file[:-4]
        repo_fla = 0
        # if repo_name != "cloud-custodian":#"spiderfoot":
        #     continue
        print("come to the repo: ", file)
        repo_path=pro_path + repo_name + "/"
        dict_complica_me_list = get_comp_code_can_test_me(repo_name)
        # print("dict_complica_me_list: ", dict_complica_me_list)
        complicate_code = util.load_pkl(complicated_code_dir_pkl, repo_name)
        for file_html in complicate_code:
            flag_file=0
            if file_html in dict_complica_me_list:

                if file_html!="https://github.com/powerline/powerline/tree/master/powerline/listers/i3wm.py":#"https://github.com/AIStream-Peelout/flow-forecast/tree/master/flood_forecast/da_rnn/train_da.py":#"https://github.com/Project-MONAI/MONAI/tree/master/monai/optimizers/lr_finder.py":#"https://github.com/searx/searx/tree/master/searx/utils.py":#"https://github.com/google/TensorNetwork/tree/master/tensornetwork/block_sparse/blocksparsetensor.py":#"https://github.com/tanghaibao/goatools/tree/master/goatools/go_enrichment.py":#"https://github.com/microsoft/msticpy/tree/master/msticpy/sectools/syslog_utils.py":#"https://github.com/chezou/tabula-py/tree/master/tabula/io.py":#"https://github.com/astorfi/speechpy/tree/master/speechpy/feature.py":#"https://github.com/pytoolz/toolz/tree/master/toolz/functoolz.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#"https://github.com/huggingface/transformers/tree/master/src/transformers/trainer_pt_utils.py":#"https://github.com/pytransitions/transitions/tree/master/transitions/core.py":#"https://github.com/google/yapf/tree/master/yapf/yapflib/file_resources.py":#"https://github.com/zalando/patroni/tree/master/patroni/ctl.py":#"https://github.com/pymc-devs/pymc/tree/master/pymc/sampling.py":#"https://github.com/smicallef/spiderfoot/tree/master//sflib.py":#"https://github.com/smicallef/spiderfoot/tree/master//sfwebui.py":#
                    continue

                print("come the file_html: ",file_html)
                for cl in complicate_code[file_html]:

                    for me in complicate_code[file_html][cl]:
                        me_name = me.split("$")[0]
                        if me_name == "if_main_my":  # it is impossible for the main code1 have test cases
                            continue
                        total_name=get_total_name(file_html,cl,me_name)
                        # print("come total_name: ", cl,me_name,total_name)
                        if total_name in dict_complica_me_list[file_html]:
                            test_me_inf_list=dict_complica_me_list[file_html][total_name]
                            if complicate_code[file_html][cl][me] and test_me_inf_list:
                                flag_file=1
                                repo_fla=1
                                me_count+=1
                                dict_test_acc['me_count'] += 1
                                for ind, (old_tree, new_tree) in enumerate(
                                    complicate_code[file_html][cl][me]):
                                    complic_code_count += 1
                                    dict_test_acc['complic_code_count'] += 1
                                    # print("come to complicate_code: ", file_html)
                                    print(">>>>>>>>>>>>>>>>>>>>new_tree:\n ", ast.unparse(new_tree))  #
                                    print(">>>>>>>>>>>>>>>>>>>>old_tree:\n ",
                                          ast.unparse(old_tree))  # old_tree.lineno,arg_list
                                    file_list.add(file_html)
                                    me_list.add(total_name)
                                    total_count+=1
                                    dict_test_acc['total_count'] += 1
                                    old_content, new_content,flag_same = replace_content_by_ast.replace_content_truth_value_test(repo_name, file_html, old_tree,new_tree)
                                    if flag_same:
                                        print("please check because the code1 is not changed: ", file_html)
                                        continue
                                    # print(">>>>>>>>>>old_content: ", old_content)

                                    real_file_html = file_html.replace("//", "/")
                                    rela_path =  real_file_html.split("/")[6:]
                                    old_path = repo_path + "/".join(rela_path)
                                    # util.save_file_path(old_path, new_content)
                                    rela_path[-1]="".join([rela_path[-1][:-3],"_copy_zejun",".py"])
                                    # print(">>>>>>>>>>new_content: ", new_content)
                                    rela_path="/".join(rela_path)
                                    # print(repo_path+rela_path)
                                    util.save_file_path(repo_path+rela_path, old_content)# copy 一份原来的文件防止失去

                                    test_info = []

                                    for test_html,each_rela_path, cl, me in test_me_inf_list:
                                        # test_html_list=test_html.split("/")
                                        # test_html_list[-1] = "".join([test_html_list[-1][:-3],"_copy_zejun",".py"])
                                        # test_html_list="/".join(test_html_list)
                                        fun_list = [ "::".join([cl,me])if cl else me]
                                        test_info.append([test_html,cl, me])
                                        # test_content=util.load_file_path(old_path)
                                        # print(">>>>>>>>>>test_content: ",test_content)
                                        run_test_result = confiure_pro_envior_by_requirements.run_test_file(test_html, repo_path,fun_list=fun_list)
                                        print(">>>>>>>>>>run_test_result: ", run_test_result)
                                        dict_me_re, flag_pass = confiure_pro_envior_by_requirements.get_test_result(run_test_result)

                                        print(">>>>>>>>>>dict_me_re: ",fun_list,dict_me_re,flag_pass)

                                        if not flag_pass:
                                            util.save_file_path(old_path, old_content)
                                            res.append(
                                                [repo_name, file_html,test_info,str(flag_pass),ast.unparse(old_tree), ast.unparse(new_tree)])
                                            print("****************we save the old content to original file: ", old_path)

                                            break
                                    else:

                                        total_acc_count+=1
                                        dict_test_acc['total_acc_count'] +=1

                                        util.save_file_path(old_path, old_content)
                                        res.append([repo_name, file_html, test_info,str(1),ast.unparse(old_tree), ast.unparse(new_tree)])
                                        print("****************we save the old content to original file: ", old_path)
                                        # break
        #                             # util.save_file_path(old_path, old_content)
            file_count+=flag_file
            dict_test_acc['file_count']+=flag_file
        repo_count+=repo_fla
        dict_test_acc['repo_count']+=repo_fla
        dict_test_acc['record_res']=res
        dict_test_acc['me_list'] = me_list
        dict_test_acc['file_list'] = file_list

        #                         else:
        #                             continue
        #                         break
        #             else:
        #                 continue
        #             break
        #         else:
        #             continue
        #         break

        # util.save_pkl(save_test_acc_dir, repo_name, dict_test_acc)
    print(total_acc_count,total_count)
    print("repo_count,file_count,me_count,complic_code_count:",repo_count,file_count,me_count,complic_code_count)
    # util.save_csv(save_acc_res_csv_dir,
    #               res,
    #               ["repo_name", "file_html", "test_html_list","flag_pass", "old_code", "new_code"])
    #

    # return total_acc_count/total_count


def get_test_acc():
    me_count = 0
    file_count = 0
    repo_count = 0
    complic_code_count = 0
    total_count = 0
    total_acc_count = 0

    for file in os.listdir(save_test_acc_dir):
        repo_name = file[:-4]
        complicate_code = util.load_pkl(save_test_acc_dir, repo_name)

        total_count+=complicate_code['total_count']
        total_acc_count+=complicate_code['total_acc_count']
        repo_count+=complicate_code['repo_count']
        file_count+=complicate_code['file_count']

        me_count+=complicate_code['me_count']
        complic_code_count+=complicate_code['complic_code_count']
    print("repo_count,file_count,me_count,complic_code_count:",repo_count,file_count,me_count,complic_code_count)
    print("acc: ",total_acc_count,total_count,total_acc_count/total_count)



if __name__ == '__main__':
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    save_me_test_me_dir= util.data_root + "methods_test_method_pair/truth_value_test_complicated/"
    save_test_file_res_dir=util.data_root + "save_test_file_res_dir/truth_value_test_complicated/"
    complicated_code_dir_pkl= util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated/"
    save_acc_res_csv_dir = util.data_root + "acc_res_compli_test_case/truth_value_test_complicated.csv"

    save_test_acc_dir = util.data_root + "acc_res_compli_test_case/truth_value_test_complicated_acc_dir/"
    dict_repo_file_python = util.load_json(util.data_root, "python3_1000repos_files_info")
    save_me_test_me_dir = util.data_root + "methods_test_method_pair/truth_value_test_complicated/"
    save_me_test_me_dir = util.data_root + "methods_test_method_pair/truth_value_test_complicated_remove_is_is_not/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/truth_value_test_complicated/"
    save_test_file_res_dir = util.data_root + "save_test_file_res_dir/truth_value_test_complicated_remove_is_is_not/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated/"
    complicated_code_dir_pkl = util.data_root + "transform_complicate_to_simple_pkl/truth_value_test_complicated_remove_is_is_not/"
    save_acc_res_csv_dir = util.data_root + "acc_res_compli_test_case/truth_value_test_complicated_remove_is_is_not.csv"

    save_test_acc_dir = util.data_root + "acc_res_compli_test_case/truth_value_test_complicated_remove_is_is_not_acc_dir_copy/"

    # os.mkdir(save_test_acc_dir)
    pro_path = util.data_root + "python_star_2000repo/"
    repo_list = []
    for file in os.listdir(save_test_file_res_dir):
        if file!="powerline.pkl":#"flow-forecast.pkl":#"MONAI.pkl":#"searx.pkl":#"TensorNetwork.pkl":#"goatools.pkl":#"msticpy.pkl":#"tabula-py.pkl":#"speechpy.pkl":#"toolz.pkl":#"spiderfoot.pkl":#"transformers.pkl":#"transitions.pkl":#"yapf.pkl":#"patroni.pkl":
            continue
        repo_list.append(file)

        get_each_repo_test_acc(file)

    # pool = newPool(nodes=30)
    # pool.map(get_each_repo_test_acc, repo_list)  # [:3]sample_repo_url ,token_num_list[:1]
    # pool.close()
    # pool.join()
    # get_test_acc()
