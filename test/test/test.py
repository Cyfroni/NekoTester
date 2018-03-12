import sys
from contextlib import contextmanager
from threading import Timer


def check(file_out, file_cor):
    file_out.seek(0)
    for x, y in zip(enumerate(file_cor), enumerate(file_out)):
        if x[1] != y[1]:
            raise WrongAnswerException(f"Different in line {x[0]}:\nExpected:\t{x[1]}Got:\t\t{y[1]}")
    return 'OK'


class WrongAnswerException(Exception):
    pass


class TimeoutException(Exception):
    pass


@contextmanager
def time_limit(seconds):
    def handler():
        raise TimeoutException("TIMED OUT[" + str(seconds) + " sec]")

    t = Timer(seconds, handler)
    t.start()
    try:
        yield
    finally:
        t.cancel()


def test(files, equal=check):
    def fun(f):
        def wrapper(*args, **kwargs):
            tests = range(files) if type(files) is int else files
            FILE_LOCATION = "test/"
            IN_FILENAME_SUFFIX = '_in.txt'
            OUT_FILENAME_SUFFIX = '_out.txt'
            COR_FILENAME_SUFFIX = '_cor.txt'
            count = 0
            backup = sys.stdin, sys.stdout
            for test_number in tests:
                _in = FILE_LOCATION + str(test_number) + IN_FILENAME_SUFFIX
                _out = FILE_LOCATION + str(test_number) + OUT_FILENAME_SUFFIX
                _cor = FILE_LOCATION + str(test_number) + COR_FILENAME_SUFFIX
                with open(_in) as file_in, open(_out, 'w+') as file_out, open(_cor) as file_cor:
                    try:
                        sys.stdin, sys.stdout = file_in, file_out
                        # start = time.time()
                        with time_limit(4.0):
                            f(*args, **kwargs)
                        # end = time.time()
                        print(f'{test_number}: {equal(file_out, file_cor)}', file=sys.stderr)
                    except WrongAnswerException as e:
                        print(f'{test_number}: WRONG ANSWER\n{e}\n###Passed[{count}]',
                              file=sys.stderr, end='')
                        break
                    except Exception as e:
                        print(f'{test_number}: RUNTIME ERROR\n{type(e)}\n{e}\n###Passed[{count}]',
                              file=sys.stderr, end='')
                        break
                    finally:
                        count += 1
            else:
                print(f'###SUCCEED[{count}]', file=sys.stderr, end='')
            sys.stdin, sys.stdout = backup

        return wrapper

    return fun
