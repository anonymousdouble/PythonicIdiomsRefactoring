import os,sys
code_dir="/".join(os.path.abspath(__file__).split("/")[:-2])+"/"
sys.path.append(code_dir)
import util

from extract_simp_cmpl_data import ast_util
# from code1.extract_simp_cmpl_data import ast_util
from extract_transform_complicate_code_new.extract_compli_fstring import get_nonidiom_fstring
from tokenize import tokenize
import ast,traceback
def refactor_fstring(file_path):

    content = util.load_file_path(file_path)
    new_code_list=[]
    try:
        tree=ast.parse(content)
        new_code_list = get_nonidiom_fstring(tree)

    except:
        traceback.print_exc()
    return new_code_list


def refactor_fstring_by_method(tree):

    new_code_list=[]
    try:
        new_code_list = get_nonidiom_fstring(tree)

    except:
        traceback.print_exc()
    return new_code_list

if __name__ == '__main__':
    #return '<a href="%s">%s</a>' % (quote(url.encode('utf-8')), anchor)
    code='''
def _do_update(self, amount_read):
        etime = self.re.elapsed_time()
        fread = format_number(amount_read)

        ave_dl = format_number(self.re.average_rate())

        # Include text + ui_rate in minimal
        tl = TerminalLine(8, 8 + 1 + 8)
        # For big screens, make it more readable.
        use_hours = bool(tl.llen > 80)
        ui_size = tl.add(' | %5sB' % fread)
        if self.size is None:
            ui_time = tl.add('  %s' % format_time(etime, use_hours))
            ui_end = tl.add(' ' * 5)
            ui_rate = tl.add(' %5sB/s' % ave_dl)
            out = '%-*.*s%s%s%s%s\r' % (tl.rest(), tl.rest(), self.text,
                                        ui_rate, ui_size, ui_time, ui_end)
        else:
            rtime = self.re.remaining_time()
            frtime = format_time(rtime, use_hours)
            frac = self.re.fraction_read()

            ui_time = tl.add('  %s' % frtime)
            ui_end = tl.add(' ETA ')

            ui_pc = tl.add(' %2i%%' % (frac * 100))
            ui_rate = tl.add(' %5sB/s' % ave_dl)
            # Make text grow a bit before we start growing the bar too
            blen = 4 + tl.rest_split(8 + 8 + 4)
            ui_bar = _term_add_bar(tl, blen, frac)
            out = '\r%-*.*s%s%s%s%s%s%s\r' % (
                tl.rest(), tl.rest(), self.text,
                ui_pc, ui_bar,
                ui_rate, ui_size, ui_time, ui_end
            )

        self.output.write(out)
        self.output.flush()
'''
    tree=ast.parse(code)
    new_list=refactor_fstring_by_method(tree)
    print("**********")
    for e1,e2 in new_list:
        print(">>>>unparse: ",ast.unparse(e1),"\n>>>>\n",e2)
