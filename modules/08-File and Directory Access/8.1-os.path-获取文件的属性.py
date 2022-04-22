from genericpath import exists
import os
from loguru import logger

# 获取当前路径
pwd = os.getcwd()
logger.info(f'当前路径为\n {pwd}')

# split()将路径分成 2 个单独的部分并返回元组
logger.info(f'\nos.path.split(__file__): {os.path.split(__file__)}')
# logger.info(f'os.path.splitext(__file__)\n{os.path.splitext(__file__)}')
# 多种文件路径的split效果
for path in ['filename.txt', 'filename', '/path/to/filename.txt', '/', '']:
    print('"%s" :' % path, os.path.splitext(path))

# join()
logger.info(f"\nos.path.join(__file__): {os.path.join('one', 'two', 'three')}")
for parts in [
    ('one', 'two', 'three'),
    ('/', 'one', 'two', 'three'),
    ('/one', '/two', '/three'),
]:
    print(parts, ':', os.path.join(*parts))

# 获取文件名
logger.info(f'\nos.path.basename(__file__):{os.path.basename(__file__)}')

# 获取文件的绝对路径
logger.info(f'\nos.path.dirname(__file__):{os.path.dirname(__file__)}')

# commonprefix()将路径列表作为参数，并返回一个字符串，该字符串表示所有路径中存在的公共前缀。
# 该值可能表示实际不存在的路径，并且路径分隔符不包括在考虑范围内，因此前缀可能不会停止在分隔符边界上
import os.path

paths = [
    '/one/two/three/four',
    '/one/two/threefold',
    '/one/two/three/',
]
logger.info(f'\n{paths}公共前缀为->{os.path.commonprefix(paths)}')

print(os.path.expanduser('~'))

# Testing Files
# for file in [ __file__, os.path.dirname(__file__), '/', '/data/hongyuan']:
#     print ('Absolute    :', os.path.isabs(file))
#     print ('File        :', file)
#     print ('Is File?    :', os.path.isfile(file))
#     print ('Is Dir?     :', os.path.isdir(file))
#     print ('Is Link?    :', os.path.islink(file))
#     print ('Mountpoint? :', os.path.ismount(file))
#     print ('Exists?     :', os.path.exists(file))
#     print ('Link Exists?:', os.path.lexists(file))

# print( os.path.getatime(__file__) )   # 输出最近访问时间
# print( os.path.getctime(__file__) )   # 输出文件创建时间
# print( os.path.getmtime(__file__) )   # 输出最近修改时间
# print( time.gmtime(os.path.getmtime(__file__)) )  # 以struct_time形式输出最近修改时间
# print( os.path.getsize(__file__) )   # 输出文件大小（字节为单位）
# print( os.path.abspath(__file__) )   # 输出绝对路径
# print( os.path.normpath(__file__) )  # 规范path字符串形式
