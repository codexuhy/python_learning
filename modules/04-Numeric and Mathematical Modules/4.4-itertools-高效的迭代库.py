# 参考链接：https://blog.csdn.net/neweastsun/article/details/51965226
# 总结：
#   迭代器 在python 中是一种常用的数据结构，比如说列表，迭代器的最大优势就是延迟计算，按需使用，从而提高开发和运行效率
#   以至于在python3中map,filter等返回的不再是迭代器。而通过iter函数把列表对象转化为迭代器对象又有点多此一举，这时候itertools就派上用场了
#   itertools中的函数大多是返回各种迭代器对象，其中很多函数的作用我们平时要写很多代码才能达到，而在运行效率上反而更低
from ast import Mult, Set, operator
import itertools
from loguru import logger
from typing import List

def for_loop(args: classmethod) -> List:
    a = []
    for i in args:
        a.append(i)
    return a

letters = ['a', 'b', 'c', 'd', 'e', 'f']
nums = [0, 10, 20, 30, 40,50,60]
booleans = [1, 0, 1, 0, 0, 1]


logger.warning("一、组合生成器")
# product(iter1,iter2, ... iterN, [repeat=1]);创建一个迭代器，生成表示item1，item2等中的项目的笛卡尔积的元组，repeat是一个关键字参数，指定重复生成序列的次数
logger.info("product()")
print(for_loop(itertools.product("ABCD", "xy")))  # --> Ax Ay Bx By Cx Cy Dx Dy
print(for_loop(itertools.product(
    range(2), repeat=3)))  # --> 000 001 010 011 100 101 110 111
print(for_loop(itertools.product([1, 2, 3], [4, 5], [6, 7])))

# permutations(p[,r]);返回p中任意取r个元素做排列的元组的迭代器
print(for_loop(itertools.permutations([1, 2, 3], 3)))

# combinations(iterable,r);创建一个迭代器，返回iterable中所有长度为r的子序列，返回的子序列中的项按输入iterable中的顺序排序
# note:不带重复
print(for_loop(itertools.combinations([1, 2, 3],
                                      2)))  # --> [(1, 2), (1, 3), (2, 3)]
# combinations_with_replacement()
# 同上，带重复
print(for_loop(itertools.combinations_with_replacement(
    [1, 2, 3], 2)))  # --> [(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 3)]


logger.warning("二、无限迭代器")
logger.info("2.1 count()")
print(for_loop(zip(itertools.count(1),['a','b','c'])))
# count():  生成无界限序列，count(start=0, step=1) ，示例从100开始，步长为2，循环5，打印对应值；必须手动break，count()会一直循环。
logger.info("count()")
i = 0
for item in itertools.count(100, 2):
    i += 1
    if i > 5:
        break
    print(item)

# cycle()：将迭代器进行无限迭代
logger.info("2.2 cycle()")
from itertools import *
i = 0
for item in cycle(['a', 'b', 'c']):
    i += 1
    if i == 10:
        break
    print (i, item)
logger.info("2.3 repeat()")
print(for_loop(itertools.repeat(10, 3)))  # 10 10 10
import operator
logger.warning("三、有限迭代器")
logger.info("3.1 accumlate()")
print(for_loop(itertools.accumulate([1,2,3,4,5]))) # 默认是累加
print(for_loop(itertools.accumulate([1,2,3,1,5],max)))# [1, 2, 3, 3, 5]
print(for_loop(itertools.accumulate([1,2,3,4,5], operator.mul)))

# chain():给它一个列表如 lists/tuples/iterables，链接在一起；返回iterables对象
logger.info("3.2 chain()")
print(list(itertools.chain(letters, nums)))
print(tuple(itertools.chain(letters, nums[3:])))
print(set(itertools.chain(letters, nums[3:])))
print(list(itertools.chain(letters, nums[3:])))
# chain.from_iterable() 输入iterable的所有元素也应该是可迭代的，返回包含输入iterable的所有元素的展品的iterable
logger.info("3.3 chain.from_iterable()")
print(for_loop(chain.from_iterable(['geeks', 'for', 'fafa', ['w', 'i', 'n', 's']])))

# compress (a,b) :返回我们需要使用的元素，根据b集合中元素真值，返回a集中对应的元素。
logger.info("3.4 compress()")
print(list(itertools.compress(letters, booleans)))

# dropwhile(func, seq );当函数f执行返回假时, 开始迭代序列
logger.info("3.5 dropwhile()")
print(for_loop(itertools.dropwhile(lambda x: x < 5, [1, 4, 6, 4, 1])))  # 6 4 1

# filterfalse(): filterfalse(contintion,data) 迭代过滤条件为false的数据。如果条件为空，返回data中为false的项；
logger.info("3.6 filterfalse()")
print(list(itertools.filterfalse(None, booleans)))
print(list(itertools.filterfalse(lambda x: x < 20, nums)))

# https://www.cnblogs.com/piperck/p/7219037.html
logger.info("3.7 groupby()")
L = [("a", 1), ("a", 2), ("b", 3), ("b", 4)]  
for key, group in itertools.groupby(L, lambda x:x[0] ):
    print(key + ":", list(group))
from operator import itemgetter
x = [(1, 2), (2, 3), (1, 4), (5, 5), (3, 4), (2, 6)]
soooo = sorted(x, key=lambda x:x[0]) # 必须先排序  itemgetter(0) 等价于lambda x:x[0]
p = itertools.groupby(soooo, key=itemgetter(0))
for i in p:
    print (i[0], [_[1] for _ in i[1]])

# islice(seq[, start], stop[, step]);返回序列seq的从start开始到stop结束的步长为step的元素的迭代器
logger.info("3.8 islice()")
print(for_loop(itertools.islice("abcdef", 0, 4, 2)))  #a, c

# starmap() :   针对list中的每一项，调用函数功能。starmap(func,list[]) ;
logger.info("3.9 starmap()")
print(for_loop(itertools.starmap(pow, [(2, 5), (3, 2),
                                       (10, 3)])))  # --> 32 9 1000
print(for_loop(itertools.starmap(
    max, [[5, 14, 5], [2, 34, 6], [3, 5, 2]])))  # --> 14 34 5

# takewhile(predicate, iterable)；返回序列，当predicate为true是截止。
logger.info("3.10 takewhile()")
print(for_loop(itertools.takewhile(lambda x: x < 5, [1, 4, 6, 4, 1])))  # 1 4


logger.info("3.11 tee()")
from itertools import *
r = islice(count(), 5)
i1, i2 = tee(r)
print('i1:',for_loop(i1),'i2:',for_loop(i2))

# zip_longest()返回一个迭代器，它将多个迭代器的元素组合成元组。它像内置函数zip()一样工作，只是它返回一个迭代器而不是一个列表。
logger.info("3.12 zip_longest()")
print(for_loop(itertools.zip_longest([1, 2, 3], ['a', 'b', 'c'])))
print(for_loop(zip([1, 2, 3], ['a', 'b', 'c'])))


logger.warning("求2-100之间质数")
max = 5
ll = [x for x in range(2, max + 1)]
print(ll)

for i in range(max):
    if i > len(ll) - 1:
        break
    else:
        item = ll[i]
        ll = [x for x in ll if item == x or x % item != 0]
print(len(ll))

import itertools
for item in itertools.combinations(ll, 2):
    if sum(item) == 35:
        print(item)