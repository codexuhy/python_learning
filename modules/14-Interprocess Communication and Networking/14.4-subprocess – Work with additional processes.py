from pickletools import bytes1
import subprocess
from loguru import logger
from typing import Union, List, Optional, Tuple
from loguru import logger
# 可参考学习：https://blog.csdn.net/imzoer/article/details/8678029?spm=1001.2101.3001.6650.1&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_antiscanv2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7ECTRLIST%7ERate-1.pc_relevant_antiscanv2&utm_relevant_index=2
# 将cmd输出的结果写入aa.txt文件中
# cmd = "ls -l"
# fhandle = open(r"aa.txt", "w")
# pipe = subprocess.Popen(cmd, shell=True, stdout=fhandle).stdout
# fhandle.close()

def popen(
        cmd: Union[str, List[str]],
        *,
        dir: Optional[str] = None,
        verbose: bool = True,
) -> Tuple[int, str, str]:
    if isinstance(cmd, (list, tuple)):
        cmd = ' '.join(cmd)
    if dir:
        cmd = f'cd {dir} && {cmd}'
    if verbose:
        logger.info(f'$ {cmd}')
    p = subprocess.Popen(cmd,
                         shell=True,
                         stdin=subprocess.DEVNULL,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    out, err = p.communicate()
    return p.returncode, str(out, 'utf-8'), str(err, 'utf-8')


cmd = "ls -l"
returncode, out, err = popen(cmd)
print(returncode, out, err)


# subprocess.call用于代替os.system
# call()的返回值是程序的退出代码
# logger.info(f"\ncall():\n")
# subprocess.call(['ls', '-1'], shell=True)  # function  modules  README.md  test
# subprocess.call('echo $HOME', shell=True)  #/home/hongyuan
# # check_call ()函数的工作方式与call()类似，只是检查出来退出代码，如果指示发生错误，则会引发CalledProcessError异常
# subprocess.check_call(['echo $HOME'],
#                       shell=True)  # /bin/sh: 1: True: not found
# # subprocess.check_call(['false']) # raise CalledProcessError

# output = subprocess.check_output(['ls', '-1'])
# print('Have %d bytes in output' % len(output))
# print(output)

# import subprocess
# output = subprocess.check_output(
#     'echo to stdout; echo to stderr 1>&2; exit 1',
#     shell=True,
#     )
# print ('Have %d bytes in output' % len(output))
# print (output)

# 为了防止通过 check_output()运行的命令的错误消息被写入控制台，请将 stderr参数设置为常量STDOUT
# 现在错误和标准输出通道合并在一起，所以如果命令打印错误消息，它们会被捕获而不是发送到控制台
# output = subprocess.check_output(
#     'echo to stdout; echo to stderr 1>&2; exit 1',
#     shell=True,
#     stderr=subprocess.STDOUT
#     )
# print ('Have %d bytes in output' % len(output))
# print (output)


# # popen

# import subprocess
# logerr.info(f"\npopen")
# print('\nread:')
# proc = subprocess.Popen(
#     ['echo', '"to stdout"'],
#     stdout=subprocess.PIPE,
# )
# stdout_value = proc.communicate()[0]
# print('\tstdout:', repr(stdout_value))
# # 打印
# # read:
# #         stdout: b'"to stdout"\n'

# import subprocess
# print('\nwrite:')
# proc = subprocess.Popen(
#     ['cat', '-'],
#     stdin=subprocess.PIPE,
# )
# # 把str转换成bytes类型
# data = '\tstdin: to stdin\n'
# proc.communicate(bytes(data, 'utf-8'))
# # proc.communicate( str.encode(data,'utf-8'))


# # popen2

# import subprocess
# logger.info(f'\npopen2:')
# proc = subprocess.Popen(
#     ['cat', '-'],
#     stdin=subprocess.PIPE,
#     stdout=subprocess.PIPE,
# )
# stdout_value = proc.communicate(b'through stdin to stdout')[0]
# print('\tpass through:', repr(stdout_value))

# #popen3
# import subprocess
# logger.info ('\npopen3:')
# proc = subprocess.Popen('ls -l; echo "to stderr333" 1>&2',
#                         shell=True,
#                         stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.PIPE,
#                         )
# stdout_value, stderr_value = proc.communicate(b'through stdin to stdout')
# print ('\tpass through:', repr(stdout_value))
# print ('\tstderr      :', repr(stderr_value))


# # TODO 没太理解
# # import subprocess

# logger.info ('\npopen4:')
# proc = subprocess.Popen('ls -l; echo "to stderr444" 1>&2',
#                         shell=True,
#                         stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE,
#                         stderr=subprocess.STDOUT,
#                         )
# stdout_value, stderr_value = proc.communicate(b'through stdin to stdout\n')
# print ('\tcombined output:', repr(stdout_value))
# print( '\tstderr value   :', repr(stderr_value))


# import subprocess
# logger.info('Connecting Segments of a Pipe:')
# # ps -ef | grep xuhongyuan | grep 0419
# ls = subprocess.Popen(['ps', '-ef'], 
#                         stdout=subprocess.PIPE,
#                         )

# grep = subprocess.Popen(['grep', 'xuhongyuan'],
#                         stdin=ls.stdout,
#                         stdout=subprocess.PIPE,
#                         )

# grep1 = subprocess.Popen(['grep', '0419'],
#                         stdin=grep.stdout,
#                         stdout=subprocess.PIPE,
#                         )

# end_of_pipe = grep.stdout
# print(end_of_pipe)
# print ('Included files:')
# for line in end_of_pipe:
#     print ('\t', line.strip())


# import sys

# sys.stderr.write('repeater.py: starting\n')
# sys.stderr.flush()

# while True:
#     next_line = sys.stdin.readline()
#     if not next_line:
#         break
#     sys.stdout.write(next_line)
#     sys.stdout.flush()

# sys.stderr.write('repeater.py: exiting\n')
# sys.stderr.flush()


# 打印信息没显示出来，待修改
# import subprocess
# logger.info("Interacting with Another Command")
# print ('One line at a time:')
# proc = subprocess.Popen('python repeater.py', 
#                         shell=True,
#                         stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE,
#                         )
# for i in range(10):
#     proc.stdin.write('%d\n' % i)
#     output = proc.stdout.readline()
#     print (output.rstrip())
# remainder = proc.communicate()[0]
# print (remainder)

# print
# print ('All output at once:')
# proc = subprocess.Popen('python repeater.py', 
#                         shell=True,
#                         stdin=subprocess.PIPE,
#                         stdout=subprocess.PIPE,
#                         )
# for i in range(10):
#     proc.stdin.write('%d\n'% i)

# output = proc.communicate()[0]
# print (output)