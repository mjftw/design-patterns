from functools import wraps


def logger1(msg):
    print(f'logger1: {msg}')


def logger2(msg):
    print(f'logger2: {msg}')


def logged_function(log_func):
    def decorator(func):
        @wraps(func)
        def inner(*args):
            log_func(f'{func.__name__}({", ".join(str(a) for a in args)})')

            return func(*args)

        return inner

    return decorator


@logged_function(logger1)
def foo(a, b, c):
    print('Hello foo')


@logged_function(logger2)
def bar(x, y):
    print('Hello bar')


def main():
    foo(1, 2, 3)
    bar('x', 'y')


if __name__ == '__main__':
    main()