import sys,ast, copy

sys.path.append("/mnt/zejun/smp/code1/")


def transform_chain_assign(old_ass_list):
    # print("ass_list: ",ass_list)
    ass_list=copy.deepcopy(old_ass_list)
    left=[ast.unparse(e.targets[0]) for e in ass_list]
    return ", ".join(left) + " = " + ast.unparse(ass_list[0].value)




if __name__ == '__main__':
    code='''
# self._tmp_path = tmp_path
# self._config = config
# self.location = str(tmp_path)

# print("split1")
# user_check = self.run_function('file.get_user', [check])
# mode_check = self.run_function('file.get_mode', [check])
# print("split2")
# name = obj.find('name').text.strip()
# bbox = obj.find('bndbox')
# pts = ['xmin', 'ymin', 'xmax', 'ymax']
# bndbox = []
# print("split3")
tmp_real = data[ii]
tmp_imag = data[ii + 1]
data[ii] = data[jj]
data[ii + 1] = data[jj + 1]
data[jj] = tmp_real
data[jj + 1] = tmp_imag
'''
    # 对找到的代码片段不断进行转换直至不可以转换
    code_list=[
        ["user_check = self.run_function('file.get_user', [check])","mode_check = self.run_function('file.get_mode', [check])"],
        ["name = obj.find('name').text.strip()","bbox = obj.find('bndbox')"],
        ["self._tmp_path = tmp_path","self._config = config","self.location = str(tmp_path)"]]
    # while 1:
    ass_list=[]
    tree=ast.parse(code)
    for node in ast.walk(tree):
        if isinstance(node,ast.Assign):
            ass_list.append(node)
    new_code = transform_multiple_assign(ass_list)
    print(new_code)

    # for code_frag in code_list:
    #         new_code=transform_multiple_assign(code_frag)
    #         print(new_code)















