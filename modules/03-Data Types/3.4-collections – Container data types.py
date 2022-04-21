# 参考链接：https://blog.csdn.net/songfreeman/article/details/50502194?spm=1001.2101.3001.6650.8&utm_medium=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-8.pc_relevant_antiscanv2&depth_1-utm_source=distribute.pc_relevant.none-task-blog-2%7Edefault%7EBlogCommendFromBaidu%7ERate-8.pc_relevant_antiscanv2&utm_relevant_index=13

# collections常用的类型：
#     1、计数器(Counter)
#     2、双向队列(deque)
#     3、默认字典(defaultdict)
#     4、有序字典(OrderedDict)
#     5、可命名元组(namedtuple)
# 使用以上类型时需要导入模块 from collections import *

from collections import *

#1、Counter

s = 'abcbcaccbbad'
l = ['a', 'b', 'c', 'c', 'a', 'b', 'b']
d = {'1': 3, '3': 2, '17': 2}

# # Counter 获取各元素的个数,返回字典
print(Counter(s))
print(Counter(l))
print(Counter(d))

# most_common
# most_common(int) 按照元素出现的次数进行从高到低的排序,返回前int个元素的字典
m1 = Counter(s)
print(m1)                 # Counter({'c': 4, 'b': 4, 'a': 3, 'd': 1})
print(m1.most_common(3))  # [('c', 4), ('b', 4), ('a', 3)]

# elements
# elements 返回经过计数器Counter后的元素,返回的是一个迭代器
e1 = Counter(s)
print(e1.elements())  #<itertools.chain object at 0x7f7508b91a90>
print(''.join(sorted(e1.elements())))  # aaabbbbcccc
e2 = Counter(d)
print(sorted(e2.elements())) # 字典返回value个key

# update
# update 和set集合的update一样,对集合进行并集更新
u1 = Counter(s)
u1.update('123a')
print(u1)  # Counter({'a': 4, 'c': 4, 'b': 4, '1': 1, '3': 1, '2': 1})

# substract
# substract 和update类似，只是update是做加法，substract做减法,从另一个集合中减去本集合的元素，
sub1 = 'which'
sub2 = 'whatw'
subset = Counter(sub1)
print(subset)   # Counter({'h': 2, 'i': 1, 'c': 1, 'w': 1})
subset.subtract(Counter(sub2))
print(subset)   # Counter({'c': 1, 'i': 1, 'h': 1, 'a': -1, 't': -1, 'w': -1}) sub1中的h变为2，sub2中h为1,减完以后为1

# iteritems(常用,类似字典的items)
c = Counter(s)
for i in c.items():
    print(i)



# 2、deque

str1 = 'abc123'
dq = deque(str1)
dq.append('right')
dq.appendleft('left')
dq.pop()
dq.popleft()
dq.remove('a')
print(dq.count('3'))
print(dq)
dq.reverse()
print(dq)
dq.rotate()
print(dq)
dq.clear()
print(type(dq)) 
print(dq) 


# 3、defaultdict

dic = defaultdict(dict)
dic['k1'].update({'k2':'aaa'})
print(dic)

lis = defaultdict(list)
lis['k1'].append({'k2':'aaa'})
print(lis)  # {'k1': [{'k2': 'aaa'}]}

b = dict()
b['k1'].append('2')
# TypeError: 'type' object is not iterable  
# 传统字典必须先有键值对应的列表 才可以操作 正确写法即 b = dict({'k1':[]}) 


# 4、OrderedDict

# 传统方式 
# 定义传统字典
dic1 = dict()
# 按顺序添加字典内容
dic1['a'] = '123'
dic1['b'] = 'jjj'
dic1['c'] = '394'
dic1['d'] = '999'
print(dic1)    # 结果： {'a': '123', 'c': '394', 'b': 'jjj', 'd': '999'}
# 排序
dic1_key_list = []
for k in dic1.keys():
    dic1_key_list.append(k)
dic1_key_list.sort()
for key in dic1_key_list:
    print('dic1字典排序结果 %s:%s' %(key,dic1[key]))

# 使用OrderedDict 定义有序字典
dic2 = OrderedDict()
dic2['a'] = '123'
dic2['b'] = 'jjj'
dic2['c'] = 'abc'
dic2['d'] = '999'
for k, v in dic2.items():
    print('有序字典：%s:%s' %(k,v))


# 5、nametuple
# 标准的tuple类型使用数字索引来访问元素
# 参考：https://pymotw.com/2/collections/namedtuple.html
bob = ('Bob', 30, 'male')
print('Representation:', bob)
 
jane = ('Jane', 29, 'female')
print('\nField by index:', jane[0])
 
print('\nFields by index:')
for p in [bob, jane]:
    print('%s is a %d year old %s' % p)


from collections import namedtuple
#创建一个nametuplede 类,类名称为Person，并赋给变量P
P = namedtuple('Person', 'name,age,gender')
print('Type of Person:', P._fields)  # Type of Person: <class 'type'>

#通过Person类实例化一个对象bob
bob = P(name='Bob', age=30, gender='male')
print('\nRepresentation:', bob)  # Representation: Person(name='Bob', age=30, gender='male')

#通过Person类实例化一个对象jane
jane = P(name='Jane', age=29, gender='female')
print('\nField by name:', jane.name)  # Field by name: Jane

print('\nFields by index:')
for p in [bob, jane]:
    print('%s is a %d year old %s' % p)