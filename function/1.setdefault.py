# setdefault
# setdefault(key[, default]) If key is in the dictionary, return its value. If not, insert key with a value of default and return default. default defaults to None.
# 原文链接：https://blog.csdn.net/u010339879/article/details/79322404
my_dict = {}
my_dict.setdefault('height', '160cm')
my_dict.setdefault('classes', [])
my_dict.setdefault('name')
print(my_dict)

my_dict = {'height': '170cm', 'classes': 'seven', 'name': "Jane"}
my_dict.setdefault('height', '160cm')
my_dict.setdefault('classes', [])
my_dict.setdefault('name')
print(my_dict)