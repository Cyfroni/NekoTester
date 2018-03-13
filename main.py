try:
    from mytest import mytest
except:
    class mytest:
        def neko_tester(files=0, time_limit=2.0, equal=None, generator=None, brute=None, path='0'):
            def fun(f):
                def wrapper(*args, **kwargs):
                    f(*args, **kwargs)
                return wrapper
            return fun


def brute():
    pass


@mytest.neko_tester(100, equal=0, generator=0, brute=0)
def main():
    pass

if __name__ == "__main__":
    main()
