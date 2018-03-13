import os
import sys
import time


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

def neko_tester(files, time_limit=2.0, equal=check, generator=None, brute=None, path='0'):
    if equal == 0:
        def equal(x, y):
            return True
    if generator == 0:
        generator = []
    if brute == 0:
        def brute():
            pass
    if type(files) is list:
        generator = None

    def fun(f):
        def wrapper(*args, **kwargs):
            tests = range(files) if type(files) is int else files
            TESTS_LOCATION = "./tests/" + path + "/"
            IN_FILENAME_SUFFIX = '_in.txt'
            OUT_FILENAME_SUFFIX = '_out.txt'
            COR_FILENAME_SUFFIX = '_cor.txt'
            if not os.path.exists(TESTS_LOCATION):
                os.makedirs(TESTS_LOCATION)
            count = 0
            backup = sys.stdin, sys.stdout

            for test_number in tests:
                _in = TESTS_LOCATION + str(test_number) + IN_FILENAME_SUFFIX
                _out = TESTS_LOCATION + str(test_number) + OUT_FILENAME_SUFFIX
                _cor = TESTS_LOCATION + str(test_number) + COR_FILENAME_SUFFIX
                with open(_in, 'r' if generator is None else 'w+') as file_in, \
                        open(_out, 'w+') as file_out, \
                        open(_cor, 'r' if brute is None else 'w+') as file_cor:
                    try:
                        if generator is not None:
                            if type(generator) is list:
                                for line in generator:
                                    line = ''.join([str(x) + ' ' for x in line]) + '\n'
                                    file_in.write(line)
                            else:
                                for line in generator():
                                    file_in.write(str(line) + '\n')
                            file_in.seek(0)
                        if brute is not None:
                            sys.stdin, sys.stdout = file_in, file_cor
                            brute()
                            file_cor.seek(0)
                            file_in.seek(0)

                        sys.stdin, sys.stdout = file_in, file_out

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
                        raise e
                    finally:
                        count += 1
            else:
                print(f'###SUCCEED[{count}]', file=sys.stderr, end='')
            sys.stdin, sys.stdout = backup

        return wrapper

    return fun
