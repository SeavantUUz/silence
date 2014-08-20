# coding:utf-8

def covert(string,code):
    new_string = string.decode('utf-8')
    lenth = len(new_string)
    return new_string.encode(code), lenth

def line_resize(lines, width, code):
    count = len(lines)
    index = 0
    while index < count:
        line = lines[index].decode('utf-8')
        line_lenth = len(line)
        if line_lenth > width:
            s_width = 0
            while s_width < line_lenth:
                yield line[s_width:s_width+width].encode(code)
                s_width += width
            index += 1
        else:
            yield line.encode(code)
            index += 1

def combine(func):
    def wrapper(*args, **kwargs):
        value = "".join(reversed(list(func(*args, **kwargs))))
        return value
    return wrapper

@combine
def parse(value):
    while value:
        ch = value % 1000
        value /= 1000
        yield chr(ch)
