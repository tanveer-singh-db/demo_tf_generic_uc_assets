import linecache
import sys


def get_exception(debug: bool = True):
    # print 'In # print exception'
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    err_obj = {
        'error_code': str(exc_type),
        'error_message': str(exc_obj),
    }
    if debug:
        err_obj['error_at'] = 'EXCEPTION IN ({}, LINE {} "{}")'.format(filename, lineno, line.strip())
    return err_obj

