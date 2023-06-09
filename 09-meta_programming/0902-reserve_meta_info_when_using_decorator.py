# 问题
# 你写了一个装饰器作用在某个函数上，但是这个函数的重要的元信息比如名字、文档字符串、注解和参数签名都丢失了。
import time
from functools import wraps

def timeit_nowraps(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(func.__name__, time.time()-start)
        return res
    return wrapper
    
@ timeit_nowraps
def countdown(n):
    '''
    docstring
    '''
    while n>0:
        n-=1

# 使用这个被包装后的函数并检查它的元信息：
# wrapper
# None
# {}
print(countdown.__name__)
print(countdown.__doc__)
print(countdown.__annotations__)

# 解决方案
# 任何时候你定义装饰器的时候，都应该使用 functools 库中的 @wraps 装饰器来注解底层包装函数。例如：
def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(func.__name__, time.time()-start)
        return res
    return wrapper

@timeit
def countdown2(n:int):
    '''docstring'''
    while n>0:
        n-=1


# 使用这个被包装后的函数并检查它的元信息：
# countdown2
# docstring
# {'n': <class 'int'>}
print(countdown2.__name__)
print(countdown2.__doc__)
print(countdown2.__annotations__)

# @wraps 有一个重要特征是它能让你通过属性 __wrapped__ 直接访问被包装函数
# Nothing
countdown2.__wrapped__(10)

# __wrapped__ 属性还能让被装饰函数正确暴露底层的参数签名信息
from inspect import signature
# (n: int)
print(signature(countdown))
# (*args, **kwargs)
print(signature(countdown2))

# 一个很普遍的问题是怎样让装饰器去直接复制原始函数的参数签名信息， 
# 如果想自己手动实现的话需要做大量的工作，最好就简单的使用 @wraps 装饰器。 
# 通过底层的 __wrapped__ 属性访问到函数签名信息。更多关于签名的内容可以参考9.16小节。
