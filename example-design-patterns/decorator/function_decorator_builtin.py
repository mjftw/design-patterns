from functools import wraps


def log(msg):
    print(msg)


def logged_function(func):
    @wraps(func)
    def inner(*args):
        log(f'{func.__name__}({", ".join(str(a) for a in args)})')

        return func(*args)

    return inner


@logged_function
def foo(a, b, c):
    print('Hello World')


def main():
    foo(1, 2, 3)

if __name__ == '__main__':
    main()