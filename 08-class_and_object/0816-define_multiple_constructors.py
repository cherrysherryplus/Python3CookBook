# 问题
# 你想实现一个类，除了使用 __init__() 方法外，还有其他方式可以初始化它。
import time
# 解决方案
# 为了实现多个构造器，你需要使用到类方法。例如：
class Date:
    """方法一：使用类方法"""
    # Primary constructor
    def __init__(self, y, m, d) -> None:
        self.y = y
        self.m = m
        self.d = d
    # Alternate constructor
    @classmethod
    def today(cls):
        t = time.localtime()
        return cls(t.tm_year, t.tm_mon, t.tm_mday)
    def __str__(self):
        return '{0.y!r}-{0.m!r}-{0.d!r}'.format(self)
    
# 直接调用类方法即可，下面是使用示例：
a = Date(2023, 6, 15) # Primary
print(a)
b = Date.today() # Alternate
print(b)

# 讨论
# 类方法的一个主要用途就是定义多个构造器。它接受一个 class 作为第一个参数(cls)。 
# 你应该注意到了这个类被用来创建并返回最终的实例。在继承时也能工作的很好：
class NewDate(Date):
    pass
d = NewDate.today()
print(d)
