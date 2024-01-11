import os,sys
code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
import util
import matplotlib.pyplot as plt

save_complicated_code_feature_dir_pkl = util.data_root + "rq_1/"

dict_list_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "list_compre_feature_num")
dict_set_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "set_compre_feature_num")
dict_dict_compre=util.load_pkl(save_complicated_code_feature_dir_pkl, "dict_compre_feature_num")
dict_chain_compare=util.load_pkl(save_complicated_code_feature_dir_pkl, "chain_compare_feature_num")
# dict_truth_test=util.load_pkl(save_complicated_code_feature_dir_pkl, "chain_compare_feature_num")
# dict_star=util.load_pkl(save_complicated_code_feature_dir_pkl, "chain_compare_feature_num")

dict_loop_else=util.load_pkl(save_complicated_code_feature_dir_pkl, "loop_else_feature_num")
dict_ass_multi_tar_value=util.load_pkl(save_complicated_code_feature_dir_pkl, "ass_multi_tar_feature_num")
dict_for_multi_tar=util.load_pkl(save_complicated_code_feature_dir_pkl, "for_multi_tar_feature_num")

'''
all_keys=set(dict_list_compre.keys())|set(dict_set_compre.keys())|set(dict_dict_compre.keys())|\
         set(dict_chain_compare.keys())|set(dict_truth_test.keys())|set(dict_star.keys())|\
        set(dict_loop_else.keys())|set(dict_ass_multi_tar_value.keys())|set(dict_for_multi_tar.keys())

result=[dict_list_compre,dict_set_compre,dict_dict_compre,dict_chain_compare,
        dict_truth_test,dict_star,dict_loop_else,dict_ass_multi_tar_value,
        dict_for_multi_tar]
'''
import numpy as np
column=["idiom","node","max","min","median","codes","%","repos","%"]
result= {
    "list-comprehension":dict_list_compre,"set-comprehension":dict_set_compre,
    "dict-comprehension":dict_dict_compre,"chain-compare":dict_chain_compare,
    # "truth-value-test":dict_truth_test,"starred":dict_star,
    "loop-else":dict_loop_else,"ass-multi-targets":dict_ass_multi_tar_value,
    "for-multi-targets":dict_for_multi_tar
}
result_csv=[]
for key in result:
    if key!="for-multi-targets":
        continue
    idiom_data=result[key]
    repos = idiom_data["repo"]
    file_html = idiom_data["file_html"]
    print("repos, files: ", len(set(repos)),repos[0],len(set(file_html)),len(repos))

    util.save_pkl(save_complicated_code_feature_dir_pkl, "repos_for_multi", repos)
    util.save_pkl(save_complicated_code_feature_dir_pkl, "files_for_multi", file_html)
    for feature in idiom_data:
        if feature in ["repo","file_html"]:
            continue
        row_data = [key]
        row_data.append(feature)
        value=idiom_data[feature]
        median_value=np.median(value)

        e = [np.max(value), np.min(value), np.median(value)]
        repos_filter=[repos[i] for i,e in enumerate(value) if e > median_value]
        file_html_filter = [file_html[i] for i, e in enumerate(value) if e > median_value]
        num_value_larger=len([i for i in value if i > median_value])
        ratio=num_value_larger/len(value)
        print("ratio: ",num_value_larger,ratio)
        print(f"{key}, {feature}, count>{median_value}: ",e,num_value_larger,ratio,num_value_larger/ratio if ratio>1e-6 else None)
        print("repos, files: ",len(set(repos)),len(set(repos_filter)),len(value),len(set(file_html_filter)),len(set(repos_filter))/len(set(repos)),len(set(file_html_filter))/len(set(file_html)))
        e.extend( [ len([i for i in value if i > median_value]),
             len([i for i in value if i > median_value]) / len(value), len(set(repos_filter)),
             len(set(repos_filter)) / len(set(repos))]+[value.count(i) for i in range(0,np.max(value)+1)])
        row_data.extend(e)
        result_csv.append(row_data)
    mixed_types_num = []
    all_features = [idiom_data[feature] for feature in idiom_data if feature not in ["repo", "file_html","num_comprehension","depth"]]
    for i in range(len(repos)):
        num=0
        for e in all_features:
            num+=1 if e[i] else 0
        mixed_types_num.append(num)
    print(f"mixed_types_num of {key}: ", np.max(mixed_types_num), np.min(mixed_types_num), np.median(mixed_types_num))

# util.save_csv(util.data_root + "rq_1/all_idioms_num_node.csv",
#                   result_csv,
#                   column)
'''
step = 0.3
plt.figure()
fig, ax = plt.subplots()
flierprops = {'marker': 'o', 'markersize': 2, 'markeredgecolor': '#7f7f7f'}
i=1

for key in dict_list_compre:
    if key=="num_comprehension":
        continue
    # print(dict_list_compre[key])
    print("count: ",list(dict_list_compre[key]).count(2))
    # ax.boxplot([dict_list_compre[key]], positions=[i*step], flierprops=flierprops)
    ax.violinplot([dict_list_compre[key]], showmedians=True,positions=[i*step],widths=0.1)

    i+=1
    # break

plt.show()
'''






