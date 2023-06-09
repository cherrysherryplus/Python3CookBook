# 问题
# 一个装饰器已经作用在一个函数上，你想撤销它，直接访问原始的未包装的那个函数。
from functools import wraps

def somedecorator(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decoration')
        res = func(*args, **kwargs)
        return res
    return wrapper

@somedecorator
def add(x,y):
    return x+y

# 解决方案
# 假设装饰器是通过 @wraps来实现的，那么你可以通过访问 __wrapped__ 属性来访问原始函数：
orig_add = add.__wrapped__
print(orig_add(1,2))
print('-'*30)
print(add(1,2))

# 讨论
# 直接访问未包装的原始函数在调试、内省和其他函数操作时是很有用的。 
# 但是我们这里的方案仅仅适用于在包装器中正确使用了 @wraps 
# 或者直接设置了 __wrapped__ 属性的情况。

# 如果有多个包装器，那么访问 __wrapped__ 属性的行为是不可预知的，应该避免这样做。 
# 在Python3.3中，它会略过所有的包装层；在3.4以上的版本中，会略过最外层的装饰器
from functools import wraps

def decorator1(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 1')
        return func(*args, **kwargs)
    return wrapper

def decorator2(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print('Decorator 2')
        return func(*args, **kwargs)
    return wrapper

@decorator1
@decorator2
def sub(x, y):
    return x - y

print(sub(3,2))
print('-'*30)
print(sub.__wrapped__(3,2))
print('-'*30)
print(sub.__wrapped__.__wrapped__(3,2))

# 最后要说的是，并不是所有的装饰器都使用了 @wraps ，因此这里的方案并不全部适用。 
# 特别的，内置的装饰器 @staticmethod 和 @classmethod 就没有遵循这个约定 
# (它们把原始函数存储在属性 __func__ 中)
