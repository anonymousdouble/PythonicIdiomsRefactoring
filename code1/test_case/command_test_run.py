import subprocess
total_cmd=["cd /data1/zhangzejun/; echo 'hello';python3.7 /data1/zhangzejun/mnt/zejun/smp/code1/test_case/a.py"]#["conda activate; python3.9 /data1/zhangzejun/mnt/zejun/smp/code1/test_case/a.py"]
result = subprocess.run(total_cmd, shell=True, timeout=15 * 60, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
std_out_res = result.stdout.decode("utf-8")
# print("std_out_res: \n", std_out_res)
std_error = result.stderr.decode("utf-8") if result.stderr else ""
std_args = result.args
print("\n".join(result.stdout.decode("utf-8").split("*************************test*************************")))

print("std_error: \n", std_error)
print("std_args: \n", std_args)