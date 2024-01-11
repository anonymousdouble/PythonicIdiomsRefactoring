import sys, ast, os,random

code_dir = "/".join(os.path.abspath(__file__).split("/")[:-2]) + "/"
print("code_dir: ", code_dir)
sys.path.append(code_dir)
import util
'''
a=[[1,2,3]]
for e,*b,*c in a:
    print("come")
#         ^
# SyntaxError: multiple starred expressions in assignment
'''
import ast


def func(*a):
    print(a)
    d=b,c=a
    a,b=1,2,(3,4)
def func_ret():
    a=[1,2,3]
    return *a,
print(func_ret())
'''
a=0
b=1
try:
    while b:
        try:
            b/a
            print("I come to the while stmt")
        except:
            print("while has try")
    else:
        print("I come to the else substmt of while")
except:
    print("has errors")
'''
a=[1,2,3]
b=[5,6,7]
result = b if not a else (*b,)
result = b if not a else tuple(b)
print("result: ",result)
print("zip(a,b): ",zip(a,b))
print("zip(a,b): ",[*zip(a,b)])
print("zip(a,b): ",list(zip(a,b)))
print("list('123'): ",list("123"))
# a={1,2,3}
# func(*a)
# func(*"1,2,3")
# a=12
# func(*f"sin({a}) is {a}")
import dis
dis.dis(func)
code='''
def test_aggregate_duplicate_columns(self):
        # Regression test for #17144

        results = Author.objects.annotate(num_contacts=Count("book_contact_set"))

        # There should only be one GROUP BY clause, for the `id` column.
        # `name` and `age` should not be grouped on.
        _, _, group_by = results.query.get_compiler(using="default").pre_sql_setup()
        self.assertEqual(len(group_by), 1)
        self.assertIn("id", group_by[0][0])
        self.assertNotIn("name", group_by[0][0])
        self.assertNotIn("age", group_by[0][0])
        self.assertEqual(
            [(a.name, a.num_contacts) for a in results.order_by("name")],
            [
                ("Adrian Holovaty", 1),
                ("Brad Dayley", 1),
                ("Jacob Kaplan-Moss", 0),
                ("James Bennett", 1),
                ("Jeffrey Forcier", 1),
                ("Paul Bissex", 0),
                ("Peter Norvig", 2),
                ("Stuart Russell", 0),
                ("Wesley J. Chun", 0),
            ],
        )
upper_bounds = np.asarray([replace_none(i.max, 1) for i in self.params.values()])[varying]
a=[i for i in a]+[2]
bs['connected_to'] = sorted([d for d in bs['connected_to'] if not masterid or masterid == d['masterid']])
metrics_list = [torch.tensor(v, device=runner.device, dtype=torch.float32) if not isinstance(v, torch.Tensor) else v.float() for v in metrics_list]
value_width = max([len(bench.format_value(bucket * value_k)) for bucket in range(bucket_min, bucket_max + 1)])
msg = f"Invalid 'classifier_type': {classifier_type}. Allowed types are: {[_class.ALLOWED_CLASSIFIER_TYPES for _class in CLASSES]}"
assert 'My Appliance' in [c.__json__()['name'] for c in controller.appliance_manager.appliances.values()]
np.asarray([replace_none(i.max, 1) for i in self.params.values()])[varying]
Assign	keyword----->pycoin	https://github.com/richardkiss/pycoin/tree/master/tests/who_signed_test.py	WhoSignedTest	test_sign_pay_to_script_multisig$64	[key.sec() for key in keys[:N]]	underlying_script = network.contract.for_multisig(m=M, sec_keys=[key.sec() for key in keys[:N]])	sec_keys=[key.sec() for key in keys[:N]]
'''
'''
tree=ast.parse(code)

for node in ast.walk(tree):
    for child in ast.iter_child_nodes(node):
        if isinstance(child,ast.ListComp):
            print(">>>>>>>>>>>>>>>>parent is : ",node.__dict__,node,ast.unparse(node),node.__class__,node.__repr__(),node.__str__(),type(node))
            # print(">>>>>>>>>>>>>>>>stmt: ",node,ast.unparse(node))
            import re
            type_node=str(node.__class__)
            result = re.search('\'ast.(.*)\'', type_node)
            print(result.group(1))
'''

a=[]
for e in a:
    print("come the loop stmt")
else:
    print("come the else of loop")


a=[1]
for e in a:
    print("come the loop stmt")
else:
    print("come the else of loop")


a={1:1,2:2}
print(a)
print(list(a.items()))

dict_num_parent= {'Assign': 71612, 'Call': 31015, 'Return': 10725, 'BinOp': 2022, 'Compare': 1852,
                      'Subscript': 1380, 'keyword': 1617, 'Starred': 1874, 'ListComp': 947, 'Lambda': 201, 'Dict': 1612,
                      'AugAssign': 983, 'Assert': 57, 'AnnAssign': 302, 'List': 393, 'Yield': 67, 'BoolOp': 137,
                      'Tuple': 525, 'DictComp': 157, 'IfExp': 566, 'FormattedValue': 54, 'comprehension': 53,
                      'Attribute': 235, 'GeneratorExp': 29, 'YieldFrom': 6, 'UnaryOp': 20}
util.save_csv(util.data_root + "rq_1/list_comprehension_idiom_code_new.csv",
                  list(dict_num_parent.items()),
                  ["key", "value"])

print("os.listdir: ",sorted(os.listdir(util.data_root)))
def func(a):
    return a+1
b=func
print("function def: ",b(1))
# val_list=[]
# for val in run:
#       val_list.append(val-1)
def func(a):
    return [1]
repo_name_list=list(range(20))

def visit_vars(target, list_vars,filter_str=""):
    # print(">>>>>>>ast.unparse(target): ",ast.unparse(target),filter_str,ast.unparse(target)!=filter_str)
    if ast.unparse(target)!=filter_str:
        # print(">>>>>>>continue ")
        # print(">>>>>>>target: ",target.__dict__)
        if isinstance(target, (ast.Name, ast.Subscript, ast.Attribute,ast.arg)):
            list_vars.append(target)

            # list_vars.append(ast.unparse(target))
            # print(">>>>>>>>the node: ",ast.unparse(target))
            for e in ast.iter_child_nodes(target):
                # print("the child is: ", ast.unparse(e))

                visit_vars(e, list_vars,filter_str)
        elif isinstance(target, ast.Call):
            if isinstance(target.func, ast.Attribute):
                # list_vars.append(
                #     target.func.value)
                visit_vars(target.func.value, list_vars, filter_str)
                for e in target.args:
                    visit_vars(e, list_vars,filter_str)
            else:
                for e in target.args:
                    visit_vars(e, list_vars,filter_str)
        else:
            for e in ast.iter_child_nodes(target):
                visit_vars(e, list_vars,filter_str)
def visit_large_vars(target, list_vars,filter_str=""):
    if ast.unparse(target) != filter_str:
        # print(">>>>>>>target: ",target.__dict__)
        if isinstance(target, (ast.Name, ast.arg)):
            # list_vars.append(ast.unparse(target))
            # if hasattr(target,"value"):
            #     visit_large_vars(target.value, list_vars, filter_str)
            # else:
            list_vars.append(target)

        else:
            for e in ast.iter_child_nodes(target):

                visit_large_vars(e, list_vars,filter_str)
def visit_filter_vars(target,list_vars,filter_node_attr=["target","targets"]):
    # if ast.unparse(target) != filter_str:
        # print(">>>>>>>target: ",target.__dict__)
    for e in ast.walk(target):
        for attr_str in filter_node_attr:
            if hasattr(e,attr_str):

                for var in ast.walk(getattr(e,attr_str)):
                    if isinstance(var, (ast.Name, ast.arg)):
                        list_vars.append(var)
def visit_large_vars(target, list_vars,filter_str=""):
    if ast.unparse(target) != filter_str:
        # print(">>>>>>>target: ",target.__dict__)
        if isinstance(target, (ast.Name, ast.arg)):
            # list_vars.append(ast.unparse(target))
            # if hasattr(target,"value"):
            #     visit_large_vars(target.value, list_vars, filter_str)
            # else:
            list_vars.append(target)

        else:
            for e in ast.iter_child_nodes(target):

                visit_large_vars(e, list_vars,filter_str)
code='''
# a=[e for e in j]
# self.b.func(a,b)
deps = removed = {RequirementSummary(t) for t in self.their_constraints} - {RequirementSummary(t) for t in theirs}
# return lambda *a, **kw: [f(*a, **kw) for f in extended_fs]
# self.a[u]=[e[w] for e in self.b] if c.split().strip() else self1.self2.func(x.y)
# return _convert_dict_keys(original, {}, lambda s: re.sub('^_', '', ''.join(['_' + c.lower() if c.isupper() else c for c in s]))) 
'''
code_node=ast.parse(code)
list_vars=[]
# visit_vars(code_node, list_vars,"['_' + c.lower() if c.isupper() else c for c in s]")
visit_large_vars(code_node, list_vars,"{RequirementSummary(t) for t in self.their_constraints}")
print("*****visit_large_vars*****")
# print(list_vars)
print({ast.unparse(e) for e in list_vars})

list_vars=[]
visit_vars(code_node, list_vars)
print("*****visit_large_vars*****")
print({ast.unparse(e) for e in list_vars})
'''
list_vars=[]
# visit_filter_vars(code_node, list_vars)
print("*****visit_filter_vars*****")
# print({ast.unparse(e) for e in list_vars})
'''
a=[i for i in range(10)]
probs=[]
for b in a:
    probs.append(b/sum(a))
print(probs)
probs=[b/sum(a) for b in a]
print(probs)
a=lambda x:x+1
print(a(1))
a=lambda *x:x
print(a(1,2,3))
def func(x):
    return x
a=lambda *x:func(x)
print(a(1,2,3))
y=[1,2,3]
for y in y:
    print(y)
print("old y: ",y)
code='''
for i in e:
    print(i)
else:
    print(else_1)
    print(else_1)
'''
tree=ast.parse(code)
for node in ast.walk(tree):
    if isinstance(node,ast.For):
        print(node.orelse)
        print([ast.unparse(e) for e in node.orelse])
        break
aa=[1,2]
b=[yy for yy in aa]
# print("yy: ",yy)
b=[]
for yy in aa:
    b.append(yy)
print("yy: ",yy)

def star_unpack(*f):
    print("f: ",f)

# star_unpack(*1)
a=[]
detect_spec=[[(1,2), 'hi'], [(1,3),'h']]
for ((first_checked_oid, *_rest1), *_rest2) in detect_spec:
    a.append(_rest1)
print("a: ",a)

'''
def has_permission_for_user(x, option):
    return args[0]


ret = has_permission_for_user("alice", *["read"])
print("ret: ",ret)
ret = has_permission_for_user("alice", "read")
print("ret: ",ret)
'''

def loop_else():
    for i in range(10):
        break
        return 1
    else:
        return 0
def loop_without_else():
    for i in range(10):
        break
        return 1
    return 0
import dis
dis.dis(loop_else)
dis.dis(loop_without_else)
code="[i for i in a]"
print("**********************")
code=ast.parse(code)
for node in ast.walk(code):
    for child in ast.iter_child_nodes(node):
        if isinstance(child, ast.ListComp):
            direct_parent = node
            print("node: ",ast.unparse(direct_parent),direct_parent, child)
            break
    else:
        continue
# for node in ast.walk(ast.parse(code)):
#     print(node,ast.unparse(node))
from pathos.multiprocessing import ProcessingPool as newPool
# pool = newPool(nodes=50)
# results=pool.map(func, repo_name_list)  # [:3]sample_repo_url ,token_num_list[:1]
# print("results: ",results)
# outputs = [result[0] for result in results]
# print("outputs: ",outputs)
# pool.close()
# pool.join()