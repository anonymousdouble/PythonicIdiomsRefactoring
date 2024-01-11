import sys,ast,os,csv,time
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
sys.path.append(code_dir+"test_case/")
sys.path.append(code_dir+"transform_c_s/")
import util,get_test_case_acc_util

from extract_simp_cmpl_data import  ast_util
if __name__ == '__main__':
        sum_test_method_count_dir=util.data_root + "5_10_all_test_cases/test_me_map_api_num/"
        # for key in dict_test_me_map_api_num:
        #     sum_cout += dict_test_me_map_api_num[key]
        # print("sum_count: ", sum_cout, len(dict_test_me_map_api_num.keys()))
        sum_tst=0
        test_method_num=[]
        for e in os.listdir(sum_test_method_count_dir):
                dict_test_me_map_api_num = util.load_pkl(sum_test_method_count_dir, e[:-4])
                for key in dict_test_me_map_api_num:
                        # print(e,dict_test_me_map_api_num[key])
                        if dict_test_me_map_api_num[key][1]<1:
                                # print(e,key)
                                continue
                        if dict_test_me_map_api_num[key][1]==144:
                                print("144: ",e, key)
                                print(key)
                            # continue
                        sum_tst+=dict_test_me_map_api_num[key][1]
                        test_method_num.append(dict_test_me_map_api_num[key][1])
        import numpy as np
        print(sum_tst)
        print("mean, std: ",np.mean(test_method_num),np.std(test_method_num))

        print("max,min,median: ",max(test_method_num),min(test_method_num),np.median(test_method_num))



