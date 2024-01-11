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

save_complicated_code_feature_dir_pkl = util.data_root + "usage_context/"
dict_list_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "list_compre")
dict_set_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "set_compre")
dict_dict_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "dict_compre")
dict_chain_compare=util.load_pkl(save_complicated_code_feature_dir_pkl, "chain_compare")
dict_truth_test=util.load_pkl(save_complicated_code_feature_dir_pkl, "truth_value_test")
dict_star=util.load_pkl(save_complicated_code_feature_dir_pkl, "starred")
# util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_targets_object", dict_tar_type)
#     util.save_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object", dict_value_type)

# dict_ass_multi_tar_value=util.load_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_value_object")
# dict_for_multi_tar=util.load_pkl(save_complicated_code_feature_dir_pkl, "for_multi_tar_object")


all_keys=set(dict_list_compre.keys())|set(dict_set_compre.keys())|set(dict_dict_compre.keys())|\
         set(dict_chain_compare.keys())|set(dict_truth_test.keys())|set(dict_star.keys())
print("dict_list_compre: ",dict_list_compre.keys())
print("dict_set_compre: ",dict_set_compre.keys())
print("dict_dict_compre: ",dict_dict_compre.keys())
print("dict_chain_compare: ",dict_chain_compare.keys())
print("dict_truth_test: ",dict_truth_test.keys())
print("dict_star: ",dict_star.keys())
print("all_keys: ",all_keys)
result=[dict_list_compre,dict_set_compre,dict_dict_compre,dict_chain_compare,
        dict_truth_test,dict_star]
# ,dict_loop_else,dict_ass_multi_tar_value,
#         dict_for_multi_tar

colum=["node","list_compre","set_compre","dict_compre","chain_compare",
        "truth_test","starred"]
colum=["node","list-compre","set-compre","dict-compre","chain-compare",
        "truth-test","star"]
# ,"loop_else","ass_multi_tar",
#         "for_multi_tar"
result_csv=[]
if 'Expr' not in all_keys:
    for ind_idiom, dict_idiom in enumerate(result):
        result[ind_idiom]['Expr']=0
all_keys=['Assign','Call',
'Return','Starred','BinOp','Compare','Dict',
'keyword','Subscript','AugAssign','ListComp','Expr',
'IfExp','Tuple','AnnAssign','Lambda','List',
'DictComp','Attribute','BoolOp','Yield','Assert',
'FormattedValue','comprehension','GeneratorExp','UnaryOp','YieldFrom',
'ClassDef','FunctionDef','For','If','Set',
'While','SetComp']
print("old_keys: ",len(all_keys))
for ind_context,key in enumerate(all_keys):

    row_data=[key]
    for ind_idiom,dict_idiom in enumerate(result):
        # if ind_context in [1,2]:
        #     print("ind_context: ",ind_context,ind_idiom,result[ind_idiom])
        total=sum(dict_idiom.values())
        if key=='ListComp' and ind_idiom==0:
            result[ind_idiom]['Expr'] = dict_idiom['ListComp']
            result[ind_idiom]['ListComp']=0
        if key=='SetComp' and ind_idiom==1:
            result[ind_idiom]['Expr'] = dict_idiom['SetComp']
            result[ind_idiom]['SetComp'] = 0
        if key=='DictComp' and ind_idiom==1:
            result[ind_idiom]['Expr'] = dict_idiom['DictComp']
            result[ind_idiom]['DictComp'] = 0
        if key=='SetComp':
            continue
        if key in dict_idiom:
            row_data.append(dict_idiom[key]/total)
        else:
            row_data.append(0)
    print("each idiom result: ",row_data)
    result_csv.append(row_data)


# util.save_csv(util.data_root + "rq_1/all_idioms_usage_context.csv",
#                   result_csv,
#                   colum)
# print("new_keys: ",len(result_csv),len(result_csv[0]))
# '''

import matplotlib.pyplot as plt
# https://blog.csdn.net/weixin_34613450/article/details/80678522 Python绘图问题：Matplotlib中指定图片大小和像素 width, height
plt.figure(figsize=(16,4))
all_keys=all_keys[:-1]
name_list=all_keys
all_keys_list=list(range(len(all_keys)))
large=1
x=all_keys_list
x=[i*large for i in x]
# x = list(range(len(num_list)))
total_width, n = 0.8*large, len(colum)-1
width = total_width / n

all_row_data=[]
for key in all_keys:
    row_data=[]
    for ind_idiom,dict_idiom in enumerate(result):
        total=sum(dict_idiom.values())

        if key in dict_idiom:
            row_data.append(dict_idiom[key]/total)
        else:
            row_data.append(0)
    all_row_data.append(row_data)
new_row_data=[[0 for j in range(len(all_keys))] for i in range(len(colum)-1)]
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

color_list=['C'+str(i) for i in range(len(colum)-1)]
# ['C0','C1','C2','C3','C4','C5','C6','C8','C9']
for ind_idiom,e_idiom_node in enumerate(new_row_data):
    e_idiom_node=transform_y(e_idiom_node)
    if ind_idiom==1:
        plt.bar(x, e_idiom_node, width=width,tick_label=all_keys, fc=color_list[ind_idiom],label=colum[ind_idiom+1])
        # break
    else:
        plt.bar(x, e_idiom_node, width=width,   fc=color_list[ind_idiom],label=colum[ind_idiom+1])
    # tick_label=all_keys_name_list, label='list_compre',
    x = [x[i] + width for i in range(len(x))]

    print("ind_idiom: ",ind_idiom,color_list[ind_idiom],e_idiom_node)
#
# plt.tight_layout()
plt.axhline(y=0.5, color='C7', lw=1, linestyle="--")
# https://blog.csdn.net/corleone_4ever/article/details/111314048 matplotlib去掉图例边框
# https://blog.csdn.net/weixin_38314865/article/details/115182900 matplotlib设置多个图例横向水平放置
plt.legend(ncol=9,loc=9,bbox_to_anchor=(0.5,1.15),frameon=False)
plt.xlim(-0.4, 33.1)# 使用该指令可调整坐标轴最左/最右刻度到两边的距离 https://www.cnblogs.com/xiao-qingjiang/p/15934443.html
plt.xticks(rotation=35)
plt.yticks([i*0.1 for i in range(15)],['0', '0.00001', '0.0001', '0.001', '0.01'] + ['0.'+str(i) for i in range(1,10)]+['1.0'])
plt.subplots_adjust(left=0.05,bottom=0.23)
# https://blog.csdn.net/AI_ShortLegCork/article/details/121392685
plt.show()



