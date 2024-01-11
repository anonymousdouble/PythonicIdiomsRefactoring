import sys,shutil,os,ast
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"test_case/")
import util
from pathos.multiprocessing import ProcessingPool as newPool

def replace_code(lineno_list,simp_code, code_fragment_list, bias=0):
    # lineno_list = chain_compare_code[-1]
    # # compli_code=chain_compare_code[-4]
    # simp_code = chain_compare_code[-3]
    new_code_fragment_list = []
    # print("simp_code: ", simp_code, code_fragment_list,lineno_list)
    pre_lineno = None
    for ind, ((star_row, star_col), (end_row, end_col)) in enumerate(lineno_list):
        star_row_new = star_row - bias - 1
        end_row_new = end_row - bias - 1
        replace_code = simp_code[ind]
        # print('replace_code: ',replace_code,star_row,star_col,end_row, end_col,code_fragment_list,star_row_new,end_row_new)
        if pre_lineno and pre_lineno[1] < star_row_new:  # len(new_code_fragment_list) < star_row_new:
            new_code_fragment_list += code_fragment_list[pre_lineno[1]+1:star_row_new]
        elif not pre_lineno and star_row_new>=1:
            new_code_fragment_list += code_fragment_list[:star_row_new]
        if pre_lineno:
            pre_lineno=max(star_row_new,pre_lineno[0]), max(end_row_new,pre_lineno[1])
        else:
            pre_lineno=star_row_new, end_row_new
        # pre_lineno=star_row_new,end_row_new
        if not replace_code:
            # new_code_fragment_list.append('')
            # print("each new_code_fragment_list: ", new_code_fragment_list,code_fragment_list[end_row_new + 1:])
            if ind == len(lineno_list) - 1:
                new_code_fragment_list += code_fragment_list[end_row_new + 1:]
            # print("each new_code_fragment_list: ", new_code_fragment_list,code_fragment_list[end_row_new + 1:])
            continue

        code_str = code_fragment_list[star_row_new][:star_col] + replace_code + code_fragment_list[end_row_new][
                                                                                end_col:]
        # print("each code_str: ",code_str)
        new_code_fragment_list.append(code_str)
        if ind == len(lineno_list) - 1:
            new_code_fragment_list += code_fragment_list[end_row_new + 1:]

    # print("each new_code_fragment_list: ", new_code_fragment_list)
    return new_code_fragment_list
def get_path_from_html(file_html,repo_path):
    real_file_html = file_html.replace("//", "/")
    rela_path = real_file_html.split("/")[6:]
    abs_path = repo_path + "/".join(rela_path)
    return abs_path

def file_replace(abs_path,code_pair):
    # real_file_html = file_html.replace("//", "/")
    # rela_path = real_file_html.split("/")[6:]
    # abs_path = repo_path + "/".join(rela_path)
    print("abs_path: ", abs_path)
    abs_path_list=abs_path.split("/")
    copy_path="".join(["/".join(abs_path_list[:-1]),"/",abs_path_list[-1][:-3],"_copy_zejun.py"])

    print("copy_path: ", copy_path)
    if not os.path.exists(copy_path):
        shutil.copy(abs_path,copy_path)
    content = util.load_file_path(file_path=abs_path)
    old_node,new_code,*remain_code=code_pair
    replace_code, add_code_pre,add_code_after,*add_code_head = new_code
    print("add_code_head: ",add_code_head)
    # if "tmp" not in replace_code:
    #     return
    old_node_content=ast.get_source_segment(content, old_node)
    start_line,end_line,start_col,end_col=old_node.lineno,old_node.end_lineno,old_node.col_offset,old_node.end_col_offset
    # print("*******old_node_content**********: ", content)
    print(">>>>>>>>>>>>>>old_node: ",ast.unparse(old_node),start_line,end_line,start_col,end_col)
    print(">>>>>>>>>>>>>>replace_code: ", replace_code)
    print(">>>>>>>>>>>>>>add code: ",add_code_pre,"\n>>>>>>>>>>>>>>after code: ",add_code_after)
    # print(old_node_content)
    # print("start_line,end_line,start_col,end_col: ",start_line,end_line,start_col,end_col)
    #
    new_content = []

    '''
    # 如果r读的话,会遇到一些情况字符长度和col_set 不一致
    https://github.com/metabrainz/picard/tree/master/picard/releasegroup.py
    "country": limited_join(countries, 10, '+', '…') if co(bool(countries) if hasattr(countries, '__bool__') else len(countries)!=0 if hasattr(countries, '__len__') else countries not in [None, False, 0, 0.0, 0j, Decimal(0), Fraction(0, 1), '', (),[], {}, dict(), set(), range(0)])  
    '''
    with open(abs_path,"rb") as f:
        lines = f.readlines()
        if add_code_head:
            head_insert_line = add_code_head[0][0]
            pre_head_space = ""
            for line in lines[head_insert_line-1:]:
                line=line.decode('utf-8')
                if line.strip():
                    for e in line:
                        if e == " ":
                            pre_head_space += " "
                        elif e == "\t":
                            pre_head_space += "\t"
                            # print("\t:pre_head_space: ", [pre_head_space])
                        else:
                            break
                    break
            # print("pre_head_space: ", [lines[head_insert_line-1]],[pre_head_space])
            print("new_code,add_code_head[0][1]: ",new_code,add_code_head,add_code_head[0][1])
            add_code_head[0][1]=[pre_head_space + e + "\n" for e in add_code_head[0][1].split("\n") if e]
        if start_line>1:
            if add_code_head:
                new_content.extend(lines[:head_insert_line-1]+add_code_head[0][1]+lines[head_insert_line-1:start_line - 1])
            else:
                new_content.extend(lines[:start_line-1])
        else:
            if add_code_head:
                new_content.extend(add_code_head[0][1])

        count_space=0
        pre_space=""
        lines_start=lines[start_line - 1].decode('utf-8')
        for e in lines_start:

            if e == " ":
                pre_space+=" "
                count_space += 1
            elif e=="\t":
                pre_space += "\t"
                count_space+=4
                # print("\t:count_space: ", count_space)
                # break
            else:
                break
        print("count_space: ", count_space,[pre_space])
        # print(">>>>>>lines[20:start_line]: \n", lines[20:start_line])
        # print(">>>>>>lines[23]: \n", lines[23])

        # code_fragment_list = replace_code.split("\n")
        # for ind_row,e_row in enumerate(code_fragment_list):
        #     if e_row:
        #         code_fragment_list[ind_row]= " " * count_space +code_fragment_list[ind_row]
        start_code='    ' if lines[start_line-1][:start_col]=="\t" else lines[start_line-1][:start_col]
        start_code=start_code.decode("utf-8")
        print(">>>>>>start_code: \n", [start_code],len(start_code),start_col,[lines[start_line-1]])
        # code_str = lines[start_line-1][:start_col] + replace_code + lines[end_line-1][end_col:]
        if start_code.endswith(";"):
            ind_start=0
            pre_str=""
            for e_start in start_code:
                # print("each e_start: ",[e_start])
                if e_start==" ":
                    pre_str+=" "
                elif e_start=="\t":
                    pre_str+="\t"
                else:
                    break
            # print("ind_start: ",ind_start)
            code_str = pre_str+replace_code + lines[end_line - 1][end_col:].decode("utf-8")
            new_content.extend([start_code+"\n"])
            # print("start_code: ", start_code)
        else:
            code_str = start_code + replace_code + lines[end_line-1][end_col:].decode("utf-8")

        # print(">>>>>>lines[end_line-1][end_col:]: \n", [lines[end_line-1][end_col:]])
        new_content.extend([pre_space + e + "\n" for e in add_code_pre.split("\n") if e])
        new_content.extend([code_str])
        new_content.extend([pre_space + e + "\n" for e in add_code_after.split("\n") if e])
        if end_line<len(lines):
            new_content.extend(lines[end_line:])
        # print("lines[start_line-1]: ",[lines[start_line-1][:start_col]=='\t'],[lines[start_line-1][:start_col]],[lines[start_line-2]],[lines[start_line-1]])
        print("each code_str: \n", code_str)
        # print("new_content: ","".join(new_content))
    return content,"".join([e.decode("utf-8") if hasattr(e,"decode") else e for e in new_content])
    ''' 
        new_content.extend([code_str])

        new_content.extend(lines[end_line:])
    print("new_content: ","".join(new_content))
    '''

if __name__ == '__main__':
    save_for_else_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl_new/list_comprehension_idiom_code/"
    save_for_else_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl_new/dict_comprehension_idiom_code/"
    save_for_else_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl_new/set_comprehension_idiom_code/"
    save_for_else_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl_new/chained_comparison_idiom_code/"
    save_for_else_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl_new/truth_value_test_idiom_code/"
    save_for_else_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl_new/truth_value_test_idiom_code/"
    save_for_else_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl_new/for_else_idiom_code/"
    save_for_else_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl_new/for_else_idiom_code/"
    save_for_else_complicated_code_dir_pkl = util.data_root + "idiom_code_dir_pkl_new/for_multi_tar_idiom_code/"
    save_for_else_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl_new/multi_assign_idiom_code/"
    save_for_else_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl_new/call_star_idiom_code/"
    save_for_else_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl_new/truth_value_test_idiom_code/"
    save_for_else_complicated_code_dir_pkl= util.data_root + "idiom_code_dir_pkl_new/truth_value_test_idiom_code_create_func/"

    file_path_list=[]
    code_pair_list=[]
    for file_name in os.listdir(save_for_else_complicated_code_dir_pkl):

        repo_name = file_name[:-4]
        repo_name ="Hypernets"#"picard"#"dulwich"#"profiling"#"feature_engine"#"gunicorn"#"beancount"#"profiling"#"feature_engine"#"category_encoders"#"BERT-Classification-Tutorial"#"heatmap"#"feature_engine"#"gunicorn"#"asv"# "TensorNetwork"#"dynaconf"#"zdict" #"powerline"#"worldengine"
        repo_path = util.pro_path + repo_name + "/"

        dict_comp_file = dict()
        # test_case_complicate_code = util.load_pkl(save_test_methods_dir, repo_name)
        # files_num_list.append(repo_files_info[repo_name])
        # star_num_list.append(repo_star_info[repo_name])
        # contributor_num_list.append(repo_contributor_info[repo_name])

        complicate_code = util.load_pkl(save_for_else_complicated_code_dir_pkl, repo_name)
        for file_html in complicate_code:
            file_html="https://github.com/DataCanvasIO/Hypernets/tree/master/hypernets/core/trial.py"#"https://github.com/metabrainz/picard/tree/master/picard/releasegroup.py"#"https://github.com/dulwich/dulwich/tree/master/dulwich/contrib/release_robot.py"#"https://github.com/dulwich/dulwich/tree/master/dulwich/porcelain.py"#"https://github.com/what-studio/profiling/tree/master/profiling/stats.py"#"https://github.com/feature-engine/feature_engine/tree/master/feature_engine/selection/drop_psi_features.py"#"https://github.com/benoitc/gunicorn/tree/master/gunicorn/util.py"#"https://github.com/beancount/beancount/tree/master/beancount/utils/misc_utils.py"#"https://github.com/what-studio/profiling/tree/master/test/_utils.py"#"https://github.com/feature-engine/feature_engine/tree/master/feature_engine/variable_manipulation.py"#"https://github.com/scikit-learn-contrib/category_encoders/tree/master/category_encoders/count.py"#"https://github.com/Socialbird-AILab/BERT-Classification-Tutorial/tree/master//tokenization.py"#"https://github.com/scikit-learn-contrib/category_encoders/tree/master/category_encoders/count.py"#"https://github.com/sethoscope/heatmap/tree/master//heatmap.py"#"https://github.com/scikit-learn-contrib/category_encoders/tree/master/category_encoders/count.py"#"https://github.com/sethoscope/heatmap/tree/master//heatmap.py"#"https://github.com/Socialbird-AILab/BERT-Classification-Tutorial/tree/master//tokenization.py"#"https://github.com/feature-engine/feature_engine/tree/master/feature_engine/variable_manipulation.py"#"https://github.com/benoitc/gunicorn/tree/master/gunicorn/sock.py"#"https://github.com/airspeed-velocity/asv/tree/master/asv/statistics.py"#"https://github.com/rochacbruno/dynaconf/tree/master/dynaconf/vendor/dotenv/cli.py"#"https://github.com/zdict/zdict/tree/master/zdict/loader.py"#"https://github.com/powerline/powerline/tree/master/powerline/commands/main.py"
            for cl in complicate_code[file_html]:
                for me in complicate_code[file_html][cl]:
                    real_file_html = file_html.replace("//", "/")
                    rela_path = real_file_html.split("/")[6:]
                    old_path = repo_path + "/".join(rela_path)
                    # print(complicate_code[file_html][cl][me])
                    content = util.load_file_path(file_path=old_path)
                    # print("content: ", content)

                    for code_pair in complicate_code[file_html][cl][me]:
                        print("code_pair: ",code_pair)
                        abspath=get_path_from_html(file_html, repo_path)
                        file_path_list.append(abspath)
                        code_pair_list.append(code_pair)
                        old_content,new_content=file_replace(abspath, code_pair)
                        print("old_content: ", old_content)
                        print("****************************")
                        print("new_content: ", new_content)

                        # break
                    # content = util.load_file_path(file_path=old_path)
                    # print("content: ",content)
                    # break
                # break
            break
        #
        break
    # if a:
    #     pass
    # elif 1:
    #     pass
#https://github.com/marcwebbie/passpie/tree/master/passpie/process.py
#
    # pool = newPool(nodes=50)
    # pool.map(file_replace, file_path_list,code_pair_list)  # [:3]sample_repo_url ,token_num_list[:1]
    # pool.close()
    # pool.join()




