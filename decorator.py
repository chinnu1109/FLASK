from functools import wraps
def check(func):
    @wraps(func)
    def wrapper():
        print("Task done")
        print(f'{func.__name__} function called')
        func()
    return wrapper

@check
def hi():
    print("hi")

@check
def hello():
    print("Hello")

@check
def bye():
    print("Bye")

hi()
# wraps -- to call the original method
print(hello.__name__,"function called 1") 
hello()
bye()


from functools import wraps

def mydecoratr(func):
    @wraps(func)
    def wrapper1(*a, **b):
        func(*a, **b)     # call original function
        print("Hi")
    return wrapper1


@mydecoratr
def hello(a, b, name=""):
    print(a + b)
    print(name)


@mydecoratr
def hello1(a, b, c):
    print(a + b + c)


# function calls
hello(10, 20, name="CHINNU")
hello1(10, 20, 30)
