import util
import sys
from sklearn.utils import shuffle
from sklearn.feature_selection import SelectKBest
import numpy as np
sys.path.append("../../../")
sys.path.append("/mnt/zejun/pycharm_project_936/new_project/traditional_classfier/")
sys.path.append('/mnt/zejun/pycharm_project_936/')
import util,sys,joblib,os
from scipy.stats import ranksums,mannwhitneyu
import cliffsDelta
import random
from sklearn.linear_model import SGDClassifier
from sklearn import preprocessing
from sklearn.naive_bayes import GaussianNB
from datetime import datetime,timedelta
from sklearn.impute import SimpleImputer
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier, AdaBoostClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix,f1_score,accuracy_score, roc_curve, auc,classification_report,roc_auc_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split

from sklearn.ensemble import ExtraTreesClassifier
from sklearn.feature_selection import SelectFromModel
import pandas as pd
import numpy as np
#from new_project.save_related_data import get_top_repo_url, save_top_repo_all_issues
from sklearn.utils import shuffle
import sys
from scipy.stats import skew, boxcox,yeojohnson
sys.path.append("../../../")
sys.path.append("/mnt/zejun/pycharm_project_936/new_project/traditional_classfier/")
sys.path.append('/mnt/zejun/pycharm_project_936/')
import util,sys,joblib,os
from sklearn_util import get_auc,evaluate_roc,scale,standard,normalize,model_score_df#get_tf_idf, evaluate_roc
from sklearn.inspection import plot_partial_dependence
from matplotlib import pyplot as plt

root_dir="/mnt/zejun/pycharm_project_936/my_GFI/data/selected/"
feature_dir=root_dir+"features/"
#df_feature_name=util.load_json(feature_dir,'feature_name_supplement_feature')
dir_all_features=util.root_dir + "my_GFI/data/selected/features/all_features/"

# dict_feature=util.load_json(dir_all_features,"dict_all_features")
# index=util.load_json(dir_all_features,"index_all_features")
dict_feature=util.load_json(dir_all_features,"dict_all_features_add_GFI_attr")
index=util.load_json(dir_all_features,"index_all_features_add_GFI_attr")
selected_attractive_dir = "/mnt/zejun/pycharm_project_936/my_GFI/data/selected/"
dict_attractive_issue = util.load_json(selected_attractive_dir,
                                       "dict_attractive_commenter_and_event_attracive_isse_new" + "num_commit_" + "1")
csv_data=[]
p_list=[]
print(list(dict_feature.keys()))
top_10_feature=util.load_json(feature_dir,"top_10_feature")
key_feature_list=[]
print("top_10_feature: ",top_10_feature)
for key in dict_feature.keys():
    #i+=1
    #if i>10:
    #    break
    if key not in top_10_feature and key!="issuer_attractive_num":
        continue
    key_feature_list.append(key)
    all_feature_value=dict_feature[key]
    print("----feature---------:", key,len(all_feature_value),len(index))
    attract_values = []
    un_attract_values = []
    for ind,value in enumerate(all_feature_value):
        if dict_attractive_issue[index[ind]][2]:
            attract_values.append(value)
        else:
            un_attract_values.append(value)
    stat,p=ranksums(attract_values, un_attract_values)
    p_list.append(p)
    if p<0.001:
        p="p<0.001"
    d, res = cliffsDelta.cliffsDelta(attract_values, un_attract_values)

    csv_data.append([key,p,d,res[0].upper()])
    print(key,p, d,res[0].upper())
#print("difference: ",set(top_10_feature)-set(key_feature_list))
print("p_list: ",p_list)
from statsmodels.sandbox.stats.multicomp import multipletests
#https://stackoverflow.com/questions/41517159/bonferroni-correction-of-p-values-from-hypergeometric-analysis
p_adjusted = multipletests(p_list, method='bonferroni')
print("p_adjusted: ",p_adjusted)
    #break
# util.save_csv(feature_dir+"each_feature_cliff_delta_now.csv",csv_data)

    #'''
'''
for e in set(corpus):
    if e in attr_count.keys():
        treatment.append(attr_count[e])
    else:
        treatment.append(0)
    if e in unattr_count.keys():
        control.append(unattr_count[e])
    else:
        control.append(0)

print(mannwhitneyu(treatment, control))
print(ranksums(treatment, control))
d, res = cliffsDelta.cliffsDelta(treatment, control)
print(d, res)
'''