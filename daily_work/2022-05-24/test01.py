# 2022/05/24 
# 题目: 初始化一个字典，按字典的值从小到大排序，存入列表中，使用lamada表达式
from loguru import logger
"""
方法一：
1、对字典按键(key)进行排序

2、对字典按值(value)进行排序

使用sorted函数进行排序

sorted(iterable,key,reverse)，sorted一共有iterable,key,reverse这三个参数;

其中iterable表示可以迭代的对象，例如可以是dict.items()、dict.keys()等

key是一个函数，用来选取参与比较的元素，reverse则是用来指定排序是倒序还是顺序，reverse=true则是倒序，

reverse=false时则是顺序，默认时reverse=false。
"""
logger.info('方法一：使用lambda表达式')
#初始化字典
dict_data = {'a':10,'c':6,'b':8,'d':7}

# 方法一：使用lambda表达式

# 1、对字典按键(key)进行排序
#对字典按键(key)进行排序(默认由小到大)
test_data_0=sorted(dict_data.keys())
print(test_data_0) #[3, 6, 7, 8, 10]

test_data_1=sorted(dict_data.items(),key=lambda x:x[1])
print(test_data_1) #[(3, 11), (6, 9), (7, 6), (8, 2), (10, 5)]

# 2、对字典按值(value)进行排序
#对字典按值(value)进行排序(默认由小到大)
test_data_2=sorted(dict_data.items(),key=lambda x:x[1])
print(test_data_2) #[('8', 2), ('10', 5), ('7', 6), ('6', 9), ('3', 11)]
# 逆序排列
test_data_3=sorted(dict_data.items(),key=lambda x:x[1],reverse=True)
print(test_data_3) #[('3', 11), ('6', 9), ('7', 6), ('10', 5), ('8', 2)]


# 方法二：使用operator迭代器
logger.info('方法二：使用operator迭代器')
import operator
#初始化字典
dict_data={6:9,10:5,3:11,8:2,7:6}

# 按键(key)进行排序
test_data_4=sorted(dict_data.items(),key=operator.itemgetter(0))
test_data_5=sorted(dict_data.items(),key=operator.itemgetter(0),reverse=True)
print(test_data_4) #[(3, 11), (6, 9), (7, 6), (8, 2), (10, 5)]
print(test_data_5) #[(10, 5), (8, 2), (7, 6), (6, 9), (3, 11)]

#按值(value)进行排序

test_data_6=sorted(dict_data.items(),key=operator.itemgetter(1))
test_data_7=sorted(dict_data.items(),key=operator.itemgetter(1),reverse=True)
print(test_data_6) #[(8, 2), (10, 5), (7, 6), (6, 9), (3, 11)]
print(test_data_7) #[(3, 11), (6, 9), (7, 6), (10, 5), (8, 2)]


