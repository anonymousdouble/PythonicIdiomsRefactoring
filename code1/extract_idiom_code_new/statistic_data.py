import os,sys
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
import util
dict_list_compre={'Call': 51528, 'Name': 22070, 'Subscript': 16067, 'BinOp': 8465, 'Compare': 1190, 'Attribute': 10982, 'Tuple': 6609, 'ListComp': 1385, 'IfExp': 2848, 'JoinedStr': 1174, 'Constant': 1224, 'List': 1718, 'BoolOp': 277, 'UnaryOp': 204, 'Dict': 2536, 'Lambda': 11, 'SetComp': 7, 'DictComp': 127, 'Set': 15, 'Await': 1, 'Yield': 1, 'GeneratorExp': 2}
dict_set_compre={'Attribute': 860, 'Subscript': 704, 'Call': 897, 'BoolOp': 6, 'Name': 958, 'Tuple': 311, 'IfExp': 35, 'BinOp': 94, 'JoinedStr': 24, 'UnaryOp': 1}
dict_dict_compre_key={'Subscript': 1328, 'Name': 11016, 'BinOp': 292, 'Call': 1524, 'Attribute': 1471, 'JoinedStr': 194, 'BoolOp': 5, 'Tuple': 133, 'IfExp': 34, 'Constant': 2, 'UnaryOp': 3}
dict_dict_compre_value={'Subscript': 1909, 'Name': 5895, 'Attribute': 721, 'List': 318, 'Call': 4508, 'Dict': 244, 'IfExp': 697, 'Constant': 584, 'Tuple': 210, 'Set': 10, 'BoolOp': 22, 'ListComp': 159, 'DictComp': 83, 'BinOp': 527, 'SetComp': 25, 'UnaryOp': 25, 'JoinedStr': 21, 'Compare': 41, 'Lambda': 3}

dict_chain_compare={'Attribute': 1822, 'Call': 2364, 'Name': 5657, 'Subscript': 1308, 'BinOp': 534, 'BoolOp': 4, 'Constant': 149, 'Yield': 1, 'Tuple': 24, 'ListComp': 4, 'UnaryOp': 15, 'Compare': 6, 'List': 3, 'Set': 3}
dict_truth_test={'Name': 188893, 'Attribute': 108557, 'UnaryOp': 103459, 'GeneratorExp': 11, 'BinOp': 3060, 'Subscript': 13898, 'ListComp': 110, 'NamedExpr': 550, 'Yield': 34, 'Tuple': 22, 'Await': 27, 'IfExp': 127, 'List': 6, 'YieldFrom': 1, 'Dict': 1}
dict_star={'Subscript': 2420, 'Constant': 92, 'Attribute': 4069, 'ListComp': 2075, 'Name': 52151, 'Call': 4718, 'GeneratorExp': 635, 'Tuple': 106, 'BinOp': 788, 'BoolOp': 74, 'List': 272, 'IfExp': 57, 'SetComp': 2, 'YieldFrom': 1}
dict_loop_else={'Attribute': 423, 'List': 42, 'Name': 761, 'Call': 1212, 'Subscript': 116, 'BoolOp': 22, 'UnaryOp': 13, 'BinOp': 14, 'Compare': 122, 'Tuple': 71, 'IfExp': 1, 'ListComp': 5, 'GeneratorExp': 4, 'Constant': 4}
dict_ass_multi_tar_value={'Attribute': 12237, 'BinOp': 3678, 'Call': 150167, 'Subscript': 14695, 'Constant': 11127, 'Name': 22949, 'UnaryOp': 497, 'Dict': 734, 'ListComp': 1088, 'BoolOp': 205, 'Lambda': 33, 'IfExp': 497, 'Yield': 396, 'GeneratorExp': 314, 'Await': 22, 'JoinedStr': 31, 'Compare': 37, 'YieldFrom': 100, 'Starred': 50, 'DictComp': 12, 'SetComp': 2}
dict_for_multi_tar={'Call': 75448, 'Name': 11170, 'Attribute': 2454, 'BoolOp': 34, 'Subscript': 620, 'GeneratorExp': 59, 'Tuple': 897, 'List': 1047, 'IfExp': 16, 'BinOp': 56, 'ListComp': 62, 'Set': 2, 'SetComp': 1}

save_complicated_code_feature_dir_pkl = util.data_root + "rq_1/"
dict_list_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "list_compre_object")
dict_set_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "set_compre_object")
dict_dict_compre_key=util.load_pkl(save_complicated_code_feature_dir_pkl, "dict_compre_key_object")
dict_dict_compre_value=util.load_pkl(save_complicated_code_feature_dir_pkl, "dict_compre_value_object")
dict_chain_compare=util.load_pkl(save_complicated_code_feature_dir_pkl, "chain_compare_object")
dict_truth_test=util.load_pkl(save_complicated_code_feature_dir_pkl, "truth_test_object")
dict_star=util.load_pkl(save_complicated_code_feature_dir_pkl, "starred_object")
dict_loop_else=util.load_pkl(save_complicated_code_feature_dir_pkl, "loop_else_data")
# util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_targets_object", dict_tar_type)
#     util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object", dict_value_type)

dict_ass_multi_tar_value=util.load_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object")
dict_for_multi_tar=util.load_pkl(save_complicated_code_feature_dir_pkl, "for_multi_tar_object")

dict_dict_compre=dict()
def count_key_value(compa_type,dict_objects,value=1):
    if compa_type not in dict_objects:
        dict_objects[compa_type] = value
    else:
        dict_objects[compa_type] += value
for key in dict_dict_compre_key:
    count_key_value(key,dict_dict_compre,dict_dict_compre_key[key])
for key in dict_dict_compre_value:
    count_key_value(key,dict_dict_compre,dict_dict_compre_value[key])

all_keys=set(dict_list_compre.keys())|set(dict_set_compre.keys())|set(dict_dict_compre.keys())|\
         set(dict_chain_compare.keys())|set(dict_truth_test.keys())|set(dict_star.keys())|\
        set(dict_loop_else.keys())|set(dict_ass_multi_tar_value.keys())|set(dict_for_multi_tar.keys())

result=[dict_list_compre,dict_set_compre,dict_dict_compre,dict_chain_compare,
        dict_truth_test,dict_star,dict_loop_else,dict_ass_multi_tar_value,
        dict_for_multi_tar]

colum=["node","list-compre","set-compre","dict-compre","chain-compare",
        "truth-test","star","loop-else","ass-multi-tar",
        "for-multi-tar"]
all_keys_name_list=list(all_keys)
result_csv=[]
for key in all_keys_name_list:
    row_data=[key]
    for dict_idiom in result:
        total=sum(dict_idiom.values())
        if key in dict_idiom:
            row_data.append(dict_idiom[key]/total)
        else:
            row_data.append(0)
    result_csv.append(row_data)


util.save_csv(util.data_root + "rq_1/all_idioms_data_object_new.csv",
                  result_csv,
                  colum)
import matplotlib.pyplot as plt
# -*- coding: utf-8 -*-
import matplotlib.pyplot as plt
plt.figure(figsize=(16,4))
name_list = ['Monday', 'Tuesday', 'Friday', 'Sunday']
all_keys_name_list=["Await","GeneratorExp","Starred","List",
"Lambda","Compare","Dict","Name",
"Yield","UnaryOp","Set","Constant","YieldFrom",
"BinOp","ListComp","DictComp","Subscript","IfExp",
"BoolOp","Call","SetComp","Attribute","JoinedStr",
"NamedExpr","Tuple"]
name_list=all_keys_name_list
num_list = [1.5, 0.6, 7.8, 6]
num_list1 = [1, 2, 3, 1]
all_keys_list=list(range(len(all_keys_name_list)))
large=1
x=all_keys_list
x=[i*large for i in x]
# x = list(range(len(num_list)))
total_width, n = 0.8*large, 9
width = total_width / n
result_csv=[]
all_row_data=[]
for ind_node,key in enumerate(all_keys_name_list):
    # row_data=[key]
    row_data =[]
    for dict_idiom in result:
        total=sum(dict_idiom.values())
        if key in dict_idiom:
            row_data.append(dict_idiom[key]/total)
        else:
            row_data.append(0)
    all_row_data.append(row_data)
    result_csv.append(row_data)
print("all_row_data: ",len(all_row_data),len(all_row_data[0]))
new_row_data=[[0 for j in range(len(all_keys_name_list))] for i in range(9)]
for ind_row,row in enumerate(all_row_data):
    for ind_col,col in enumerate(row):
        new_row_data[ind_col][ind_row]=all_row_data[ind_row][ind_col]

def transform_y(e_idiom_node):
    for ind,e in enumerate(e_idiom_node):
        if e<10e-6:
            e_idiom_node[ind]=e*10000
        elif e<10e-5:
            e_idiom_node[ind] =  e*1000+0.1
        elif e < 10e-4:
            e_idiom_node[ind] = e*100+0.2
        elif e < 10e-3:
            e_idiom_node[ind] = e*10+0.3
        elif e < 10e-2:
            e_idiom_node[ind] = e*1+0.4
        else:
            e_idiom_node[ind] = e+0.4
    return e_idiom_node

color_list=['C0','C1','C2','C3','C4','C5','C6','C8','C9']
for ind_idiom,e_idiom_node in enumerate(new_row_data):
    e_idiom_node=transform_y(e_idiom_node)
    if ind_idiom==4:
        plt.bar(x, e_idiom_node, width=width,tick_label=all_keys_name_list, fc=color_list[ind_idiom],label=colum[ind_idiom+1])
        # break
    else:
        plt.bar(x, e_idiom_node, width=width,   fc=color_list[ind_idiom],label=colum[ind_idiom+1])
    # tick_label=all_keys_name_list, label='list_compre',
    x = [x[i] + width for i in range(len(x))]

    print("ind_idiom: ",ind_idiom,color_list[ind_idiom],e_idiom_node)
#
# plt.tight_layout()
plt.axhline(y=0.5, color='C7', lw=1, linestyle="--")
plt.legend(ncol=9,loc=9,bbox_to_anchor=(0.5,1.15),frameon=False)
plt.xlim(-0.1, 25.1)
plt.xticks(rotation=30)
plt.yticks([i*0.1 for i in range(14)],['0', '0.00001', '0.0001', '0.001', '0.01'] + ['0.'+str(i) for i in range(1,10)])
plt.subplots_adjust(left=0.05,bottom=0.2)
# https://blog.csdn.net/AI_ShortLegCork/article/details/121392685
plt.show()
# print("new_row_data: ",len(new_row_data),len(new_row_data[0]))
# plt.bar(x, row_data, width=width, label='list_compre', fc='y')
#
#
# plt.bar(x, num_list, width=width, label='list_compre', fc='y')
# for i in range(len(x)):
#     x[i] = x[i] + width
# plt.bar(x, num_list1, width=width, label='set_compre', tick_label=name_list, fc='r')
# plt.legend()
# plt.show()








