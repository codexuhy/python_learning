#  参考链接：https://pymotw.com/2/shutil/index.html
from distutils.archive_util import make_archive
import glob
import os
from loguru import logger
import shutil
import time

# 1、shutil.copyfileobj(fsrc, fdst[, length=16*1024])：fsrc，fdst都是使用open()方法打开后的文件对象。

dir_name = os.path.abspath("test/")
source = f'{dir_name}/file.txt'
fsrc = open(source, 'r')
dest = f'{dir_name}/file_copy.txt'
fdst = open(dest, 'w')
shutil.copyfileobj(fsrc, fdst)
fsrc.close()
fdst.close()

# 2、shutil.copyfile：拷贝文件，

dir_name = os.path.abspath("test/")
source = f'{dir_name}/f1.log'
dest = f'{dir_name}/f1.log.copy'
shutil.copystat(source, dest)  # 目标文件无需存在

# 3、shutil.copymode(src, dst)：仅拷贝权限。内容、组、用户均不变

dir_name = os.path.abspath("test/")
source = f'{dir_name}/f1.log'
dest = f'{dir_name}/f2.log'
shutil.copymode(source, dest)  #目标文件必须存在

# 4、shutil.copystat(src, dst)：仅拷贝状态的信息，包括：mode bits, atime, mtime, flags

def show_file_info(filename):
    stat_info = os.stat(filename)
    print('\tMode    :', stat_info.st_mode)
    print('\tCreated :', time.ctime(stat_info.st_ctime))
    print('\tAccessed:', time.ctime(stat_info.st_atime))
    print('\tModified:', time.ctime(stat_info.st_mtime))

dir_name = os.path.abspath("test/")
source = f'{dir_name}/f1.log'
dest = f'{dir_name}/f2.log'
show_file_info(source)
shutil.copystat(source, dest)
show_file_info(dest)

# 5、shutil.copy(src, dst)：拷贝文件和权限
dir_name = os.path.abspath("test/")
source = f'{dir_name}/f1.log'
dest = f'{dir_name}/f2_copy.log'
shutil.copy(source, dest)

# 6、shutil.copy2(src, dst)：拷贝文件和状态信息
dir_name = os.path.abspath("test/")
source = f'{dir_name}/f1.log'
dest = f'{dir_name}/f2_copy2.log'
shutil.copy2(source, dest)

# 7、shutil.copytree(src, dst, symlinks=False, ignore=None)：递归的去拷贝文件夹
src = os.path.abspath("test/")
dst = os.path.abspath("test1/")  # 该文件夹会自动创建，需保证此文件夹不存在，否则将报错
shutil.copytree(src, dst, symlinks=False, ignore=None)
shutil.copytree(src, dst, ignore=shutil.ignore_patterns(
    "file.txt", "f1.log"))  # 将"abc.txt","bcd.txt"忽略

# 8、shutil.rmtree(path[, ignore_errors[, onerror]])：递归的去删除文件
shutil.rmtree(dst)

# 9、shutil.move(src, dst):递归的去移动文件，它类似mv命令，其实就是重命名
src = os.path.abspath("test1/")
dst = os.path.abspath("test_rename/")
shutil.move(src, dst)

# 10、shutil.make_archive(base_name, format[, root_dir[, base_dir, verbose, dry_run, owner, group, logger])：
# 在python_learning目录下生成test1.tar 压缩包，压缩路径/data/hongyuan/github_repo/python_learning/test
base_name = "/data/hongyuan/github_repo/test"  # 压缩包位置
root_dir = '/data/hongyuan/github_repo/python_learning/test'  # 需要压缩的目录
shutil.make_archive(base_name=base_name, format='tar',
                    root_dir=root_dir)  # format 为压缩格式
# shutil.unpack_archive("要解压的压缩文件", "解压后文件存在哪个位置")
shutil.unpack_archive(filename=f'{base_name}.tar', extract_dir='aaa')
