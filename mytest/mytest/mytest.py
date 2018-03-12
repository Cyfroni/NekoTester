import sys
import time





# 2 2 3\///
# 2 4 5\
# 1 4\
# 1 5\
# 0\
# 1')


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


# #
# # class MyTimer(Timer):
# #     def __init__(self, *args):
# #         Timer.__init__(self, *args)
# #         self.ex = None
# #
# #     def run(self):
# #         try:
# #             super(MyTimer, self).run()
# #         except Exception as e:
# #             self.ex = e
#
# @contextmanager
# def timer(seconds):
#     def handler():
#         raise TimeoutException("TIME LIMIT EXCEEDED[" + str(seconds) + " sec]")
#
#     t = Timer(seconds, handler)
#     t.start()
#     try:
#         yield
#     finally:
#         t.cancel()
#


def mytest(files, time_limit=2.0, equal=check, generator=None):
    def fun(f):
        def wrapper(*args, **kwargs):
            tests = range(files) if type(files) is int else files
            FILE_LOCATION = "mytest/"
            IN_FILENAME_SUFFIX = '_in.txt'
            OUT_FILENAME_SUFFIX = '_out.txt'
            COR_FILENAME_SUFFIX = '_cor.txt'
            count = 0
            backup = sys.stdin, sys.stdout

            for test_number in tests:
                _in = FILE_LOCATION + str(test_number) + IN_FILENAME_SUFFIX
                _out = FILE_LOCATION + str(test_number) + OUT_FILENAME_SUFFIX
                _cor = FILE_LOCATION + str(test_number) + COR_FILENAME_SUFFIX
                with open(_in, 'r' if generator is None else 'w+') as file_in, open(_out, 'w+') as file_out, open(
                        _cor) as file_cor:
                    try:
                        sys.stdin, sys.stdout = file_in, file_out

                        if generator is not None:
                            generator(file_in)
                            file_in.seek(0)

                        start = time.time()
                        f(*args, **kwargs)
                        period = time.time() - start

                        if period > time_limit:
                            raise TimeoutException(str(period) + " sec\n")
                        print(f'{test_number}: {equal(file_out, file_cor)}, TIME: {period}', file=sys.stderr)

                    except TimeoutException as e:
                        print(f'{test_number}: TIME LIMIT EXCEEDED\nTIME: {e}\n###Passed[{count}]',
                              file=sys.stderr, end='')
                        break
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
