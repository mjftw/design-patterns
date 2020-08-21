def log(msg):
    print(msg)


def logged_function(func):
    # kwargs omitted for simplicity
    def inner(*args):
        log(f'{func.__name__}({", ".join(str(a) for a in args)})')

        return func(*args)

    return inner


def foo(a, b, c):
    print('Hello World')
foo = logged_function(foo)

def main():
    foo(1, 2, 3)


if __name__ == '__main__':
    main()