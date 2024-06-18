

def print_code_object(f):
    print('-' * 100)
    code = f.__code__
    # print('co_argcount:', code.co_argcount)
    # print('co_posonlyargcount:', code.co_posonlyargcount)
    # print('co_kwonlyargcount:', code.co_kwonlyargcount)
    
    # print('co_stacksize:', code.co_stacksize)
    # print('co_flags:', code.co_flags)
    # print('co_code:', code.co_code)
    # print('co_name:', code.co_name)
    # print('co_filename:', code.co_filename)
    # print('co_lnotab:', code.co_lnotab)
    
    print('co_nlocals:', code.co_nlocals)
    print('co_varnames:', code.co_varnames)
    print('co_names:', code.co_names)
    print('co_cellvars:', code.co_cellvars)
    print('co_freevars:', code.co_freevars)
    print('co_consts:', code.co_consts)


def f(*, a, b=1, **kwargs):
    print('hello world')


class E:
    def __init__(self):
        pass


if __name__ == '__main__':
    # a = 0
    # b = 'bbb'
    print_code_object(f)
