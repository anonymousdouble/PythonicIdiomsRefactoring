import sys, ast, os, copy
import tokenize
import sys,shutil

sys.path.append("..")
sys.path.append("../../")
sys.path.append("/mnt/zejun/smp/code1/")
sys.path.append("/mnt/zejun/smp/code1/test_case")
sys.path.append("/mnt/zejun/smp/code1/transform_c_s")
import util#,rq2_performance,test_time


save_test_acc_dir_1 = util.data_root + "test_case_benchmark_dir/for_else_acc_dir/"
# save_test_acc_dir_2 = util.data_root + "test_case_benchmark_dir/truth_value_test_complicated_remove_is_is_not_acc_dir_copy/"
# save_test_acc_dir_3 = util.data_root + "test_case_benchmark_dir/multip_assign_complicated_acc_dir/"
save_test_acc_dir_list=[save_test_acc_dir_1]#,save_test_acc_dir_2,save_test_acc_dir_3]
repo_list=set([])
for dir_one in save_test_acc_dir_list:
    for file in os.listdir(dir_one):
        repo_name = file[:-4]
        repo_list.add(repo_name)

print("len: ",len(repo_list),repo_list)