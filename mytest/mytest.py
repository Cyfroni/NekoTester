import os
import sys
import time


def check(file_out, file_cor):
    file_out.seek(0)

    for i, lines in enumerate(zip(file_cor, file_out)):
        if lines[0] != lines[1]:
            raise WrongAnswerException(f"Different in line {i + 1}:\nExpected:\t{lines[0]}Got:\t\t{lines[1]}")

    return "OK"


class WrongAnswerException(Exception):
    pass


class TimeoutException(Exception):
    pass


IN_FILENAME_SUFFIX = '_in.txt'
OUT_FILENAME_SUFFIX = '_out.txt'
COR_FILENAME_SUFFIX = '_cor.txt'


def neko_tester(files, time_limit=2.0, equal='standard', generator=None, brute=None, path='0'):
    if equal == 'standard':
        equal = check

    elif equal == 'no_check':
        def equal(x, y):
            return True

    if type(files) is list:
        generator = None

    def fun(f):
        def wrapper(*args, **kwargs):
            tests_directory = "tests/" + path + "/"
            tests = range(files) if type(files) is int else files
            if not os.path.exists("tests/" + path):
                os.makedirs("tests/" + path)
            count = 0
            backup = sys.stdin, sys.stdout

            for test_number in tests:
                _in = tests_directory + str(test_number) + IN_FILENAME_SUFFIX
                _out = tests_directory + str(test_number) + OUT_FILENAME_SUFFIX
                _cor = tests_directory + str(test_number) + COR_FILENAME_SUFFIX

                with open(_in, 'r' if generator is None else 'w+') as file_in:
                    with open(_out, 'w+') as file_out:
                        with open(_cor, 'r' if brute is None else 'w+') as file_cor:
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

                                count += 1

                            except TimeoutException as e:
                                print(f'{test_number}: TIME LIMIT EXCEEDED\nTIME: {e}\n###Passed[{count}]',
                                      file=sys.stderr, end='')
                                break
                            except WrongAnswerException as e:
                                print(f'{test_number}: WRONG ANSWER\n{e}\n###Passed[{count}]',
                                      file=sys.stderr, end='')
                                break
                            except TimeoutException as e:
                                print(f'{test_number}: RUNTIME ERROR\n{type(e)}\n{e}\n###Passed[{count}]',
                                      file=sys.stderr, end='')
                                break
            else:
                print(f'###SUCCESS[{count}]', file=sys.stderr, end='')
            sys.stdin, sys.stdout = backup

        return wrapper

    return fun
