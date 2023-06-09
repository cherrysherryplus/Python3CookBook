# 问题
# 你想写一个装饰器来包装一个函数，并且允许用户提供参数在运行时控制装饰器行为。
from functools import wraps, partial
import logging

# 解决方案
# 引入一个访问函数，使用 nonlocal 来修改内部变量。 然后这个访问函数被作为一个属性赋值给包装函数。

# Utility decorator to attach a function as an attribute of obj
def attach_wrapper(obj, func=None):
    if func is None:
        return partial(attach_wrapper, obj)
    setattr(obj, func.__name__, func)
    return func

def logged(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__
        
        @wraps(func)
        def wrapper(*args, **kwargs):
            log.log(level, logmsg)
            return func(*args, **kwargs)
        
        @attach_wrapper(wrapper)
        def set_level(newlevel):
            nonlocal level
            level = newlevel
            
        @attach_wrapper(wrapper)
        def set_message(newmsg):
            nonlocal logmsg
            logmsg = newmsg
        
        # 还能通过使用lambda表达式代码来让访问函数的返回不同的设定值：
        wrapper.get_level = lambda: level
        return wrapper
    return  decorate
    
@logged(logging.DEBUG)
def add(x,y):
    return x+y

@logged(logging.CRITICAL, 'example')
def spam():
    print('Spam!')

logging.basicConfig(level=logging.DEBUG)
print(add(2,3))
add.set_message('Add called')
print(add(2,3))
add.set_level(logging.CRITICAL)
print(add(2,3))

# 讨论
# 这一小节的关键点在于访问函数(如 set_message() 和 set_level() )，它们被作为属性赋给包装器。 
# 每个访问函数允许使用 nonlocal 来修改函数内部的变量。

# 还有一个令人吃惊的地方是访问函数会在多层装饰器间传播(如果你的装饰器都使用了 @functools.wraps 注解)。
# 例如，假设你引入另外一个装饰器，比如9.2小节中的 @timethis ，像下面这样：
import time

def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        print(func.__name__, time.time()-start)
        return res
    return wrapper

@timeit
@logged(logging.DEBUG)
def countdown(n):
    while n > 0:
        n -= 1

countdown(20)

# 你还会发现即使装饰器像下面这样以相反的方向排放，效果也是一样的：
@logged(logging.DEBUG)
@timeit
def countdown(n):
    while n > 0:
        n -= 1
        
countdown(20)

# 还能通过使用lambda表达式代码来让访问函数的返回不同的设定值：
print(countdown.get_level())

# 一个比较难理解的地方就是对于访问函数的首次使用。
# 例如，你可能会考虑另外一个方法直接访问函数的属性，如下：
print("-"*30)
def logged2(level, name=None, message=None):
    def decorate(func):
        logname = name if name else func.__module__
        log = logging.getLogger(logname)
        logmsg = message if message else func.__name__

        @wraps(func)
        def wrapper(*args, **kwargs):
            wrapper.log.log(wrapper.level, wrapper.logmsg)
            return func(*args, **kwargs)
            
        # Attach adjustable attributes
        wrapper.level = level
        wrapper.logmsg = logmsg
        wrapper.log = log
        return wrapper
    return decorate

# 这个方法也可能正常工作，但前提是它必须是最外层的装饰器才行。 
# 如果它的上面还有另外的装饰器(比如上面提到的 @timeit 例子)，
# 那么它会隐藏底层属性，使得修改它们没有任何作用。 
# 而通过使用**访问函数**就能避免这样的局限性。

@timeit
@logged2(logging.DEBUG)
def countdown2(n):
    while n > 0:
        n -= 1

countdown2(20)
# 
countdown2.logmsg='hhhhh'
countdown2(20)

print("+"*30)

@logged2(logging.DEBUG)
@timeit
def countdown2(n):
    while n > 0:
        n -= 1

countdown2(20)
countdown2.logmsg='hhhhh'
countdown2(20)

# 最后提一点，这一小节的方案也可以作为9.9小节中装饰器类的另一种实现方法。
