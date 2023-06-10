# 问题
# 你想通过 format() 函数和字符串方法使得一个对象能支持自定义的格式化。

# 解决方案
# 为了自定义字符串的格式化，我们需要在类上面定义 __format__() 方法。例如：
_formats = {
    'ymd' : '{d.year}-{d.month}-{d.day}',
    'mdy' : '{d.month}/{d.day}/{d.year}',
    'dmy' : '{d.day}/{d.month}/{d.year}'
}

class Date:
    def __init__(self, y, m, d):
        self.year = y
        self.month = m
        self.day = d
    def __format__(self, code):
        if code=='':
            code = 'ymd'
        fmt = _formats[code]
        return fmt.format(d=self)
    
d = Date(2023, 6, 10)
print(format(d))
print('The date is {:mdy}'.format(d))

# 讨论
# __format__() 方法给Python的字符串格式化功能提供了一个钩子。 
# 这里需要着重强调的是格式化代码的解析工作完全由类自己决定。
# 因此，格式化代码可以是任何值。 
# 例如，参考下面来自 datetime 模块中的代码：
from datetime import date
d = date(2023, 6, 10)
print(format(d))
print(format(d, '%A %B %d, %Y'))
print('The end is {:%d %b %Y}. Goodbye'.format(d))

# 对于内置类型的格式化有一些标准的约定。 可以参考 string模块文档 说明。
