# 参考链接：https://blog.csdn.net/weixin_43790276/article/details/90903916
from multiprocessing import Process
import time
 
def coding(language):
    """子进程要执行的代码"""
    for i in range(5):
        print("{} coding".format(language), end=' | ')
        time.sleep(1)
 
 
if __name__ == '__main__':
    # 单进程
    start = time.time()
    coding('python')
    for i in range(5):
        print("main program", end=' | ')
        time.sleep(1)
    end = time.time()
    print('\nOne process cost time:', end - start)
 
    # 多进程
    multi_start = time.time()
    p = Process(target=coding, args=('python', ))
    p.start()
    for i in range(5):
        print("main program", end=' | ')
        time.sleep(1)
    multi_end = time.time()
    print('\nMulti process cost time:', multi_end - multi_start)

    
# 参考链接：https://www.cnblogs.com/wangm-0824/p/10267661.html

# 1.process模块介绍

# # 当前文件名称为test.py
# from multiprocessing import Process

# def func():
#     print(12345)

# if __name__ == '__main__': #windows 下才需要写这个，这和系统创建进程的机制有关系，不用深究，记着windows下要写就好啦
#     #首先我运行当前这个test.py文件，运行这个文件的程序，那么就产生了进程，这个进程我们称为主进程

#     p = Process(target=func,) #将函数注册到一个进程中，p是一个进程对象，此时还没有启动进程，只是创建了一个进程对象。并且func是不加括号的，因为加上括号这个函数就直接运行了对吧。
#     p.start() #告诉操作系统，给我开启一个进程，func这个函数就被我们新开的这个进程执行了，而这个进程是我主进程运行过程中创建出来的，所以称这个新创建的进程为主进程的子进程，而主进程又可以称为这个新进程的父进程。
#     # 而这个子进程中执行的程序，相当于将现在这个test.py文件中的程序copy到一个你看不到的python文件中去执行了，就相当于当前这个文件，被另外一个py文件import过去并执行了。
#     # start并不是直接就去执行了，我们知道进程有三个状态，进程会进入进程的三个状态，就绪，（被调度，也就是时间片切换到它的时候）执行，阻塞，并且在这个三个状态之间不断的转换，等待cpu执行时间片到了。
#     print('*' * 10) #这是主进程的程序，上面开启的子进程的程序是和主进程的程序同时运行的，我们称为异步



# # 通过查看子进程和主进程的ID号，验证主进程创建的子进程是异步执行的

# import time
# import os
# #os.getpid()  获取自己进程的ID号
# #os.getppid() 获取自己进程的父进程的ID号
# from multiprocessing import Process
# def func():
#     print('aaaa')
#     time.sleep(1)
#     print('子进程>>',os.getpid())
#     print('该子进程的父进程>>',os.getppid())
#     print(12345)

# if __name__ == '__main__': 
#     #首先我运行当前这个文件，运行的这个文件的程序，那么就产生了主进程
 
#     p = Process(target=func,) 
#     p.start() 
#     print('*' * 10) 
#     print('父进程>>',os.getpid())
#     print('父进程的父进程>>',os.getppid())


import time
import os
from multiprocessing import Process
 
# def func():
#     print('aaaa')
#     time.sleep(1)
#     print('子进程>>',os.getpid())
#     print('该子进程的父进程>>',os.getppid())
#     print(12345)
# if __name__ == '__main__':
#     print('太白老司机~~~~') #如果我在这里加了一个打印，你会发现运行结果中会出现两次打印出来的太白老司机，因为我们在主进程中开了一个子进程，子进程中的程序相当于import的主进程中的程序，那么import的时候会不会执行你import的那个文件的程序啊，前面学的，是会执行的，所以出现了两次打印
# # 其实是因为windows开起进程的机制决定的，在linux下是不存在这个效果的，因为windows使用的是process方法来开启进程，他就会拿到主进程中的所有程序，而linux下只是去执行我子进程中注册的那个函数，不会执行别的程序，这也是为什么在windows下要加上执行程序的时候，
# # 要加上if __name__ == '__main__':，否则会出现子进程中运行的时候还开启子进程，那就出现无限循环的创建进程了，就报错了


# def func(x,y):
#     print(x)
#     time.sleep(2)
#     print(y)
 
# if __name__ == '__main__':
 
#     p = Process(target=func,args=('小鹏','来玩啊'))#这是func需要接收的参数的传送方式。
#     p.start()
#     print('父进程执行结束！')


# def func(x,y):
#     print(x)
#     time.sleep(1)
#     print(y)
 
# if __name__ == '__main__':
 
#     p = Process(target=func,args=('姑娘','来玩啊！'))
#     p.start()
#     print('我这里是异步的啊！')  #这里相对于子进程还是异步的
#     p.join()  #只有在join的地方才会阻塞住，将子进程和主进程之间的异步改为同步
#     print('父进程执行结束！')


# # 需求：开启多个进程可以用for循环。并且所有的子进程异步执行，然后所有的子进程全部执行完之后，我再执行主进程
# # 实现如下：
# #下面的注释按照编号去看，别忘啦！
# import time
# import os
# from multiprocessing import Process
 
# def func(x,y):
#     print(x)
#     time.sleep(2) #进程切换：如果没有这个时间间隔，那么你会发现func执行结果是打印一个x然后一个y，再打印一个x一个y，不会出现打印多个x然后打印y的情况，因为两个打印距离太近了而且执行的也非常快，但是如果你这段程序运行慢的话，你就会发现进程之间的切换了。
#     print(y)
 
# if __name__ == '__main__':
 
#     p_list= []
#     for i in range(10):
#         p = Process(target=func,args=('小李%s'%i,'来玩啊！'))
#         p_list.append(p)
#         p.start()
 
#     [ap.join() for ap in p_list] #4、这是解决办法，前提是我们的子进程全部都已经去执行了，那么我在一次给所有正在执行的子进程加上join，那么主进程就需要等着所有子进程执行结束才会继续执行自己的程序了，并且保障了所有子进程是异步执行的。
 
#         # p.join() #1、如果加到for循环里面，那么所有子进程包括父进程就全部变为同步了，因为for循环也是主进程的，循环第一次的时候，一个进程去执行了，然后这个进程就join住了，那么for循环就不会继续执行了，等着第一个子进程执行结束才会继续执行for循环去创建第二个子进程。
#         # 2、如果我不想这样的，也就是我想所有的子进程是异步的，然后所有的子进程执行完了再执行主进程
#         # p.join() #3、如果这样写的话，多次运行之后，你会发现会出现主进程的程序比一些子进程先执行完，因为我们p.join()是对最后一个子进程进行了join，也就是说如果这最后一个子进程先于其他子进程执行完，那么主进程就会去执行，而此时如果还有一些子进程没有执行完，而主进程执行
#         # 完了，那么就会先打印主进程的内容了，这个cpu调度进程的机制有关系，因为我们的电脑可能只有4个cpu，我的子进程加上住进程有11个，虽然我for循环是按顺序起进程的，但是操作系统一定会按照顺序给你执行你的进程吗，答案是不会的，操作系统会按照自己的算法来分配进
#         # 程给cpu去执行，这里也解释了我们打印出来的子进程中的内容也是没有固定顺序的原因，因为打印结果也需要调用cpu，可以理解成进程在争抢cpu，如果同学你想问这是什么算法，这就要去研究操作系统啦。那我们的想所有子进程异步执行，然后再执行主进程的这个需求怎么解决啊
#     print('啦啦啦~~~~~~~~~~~~~~~~！')


# # 需求：模拟两个应用场景：1、同时对一个文件进行写操作  2、同时创建多个文件
# import time
# import os
# import re
# from multiprocessing import Process
# #多进程同时对一个文件进行写操作
# def func(x,y,i):
#     with open(x,'a',encoding='utf-8') as f:
#         print('当前进程%s拿到的文件的光标位置>>%s'%(os.getpid(),f.tell()))
#         f.write(y)
 
# # #多进程同时创建多个文件
# # def func(x, y):
# #     with open(x, 'w', encoding='utf-8') as f:
# #         print('当前进程%s拿到的文件的光标位置>>%s'%(os.getpid(),f.tell()))
# #         f.write(y)
 
# if __name__ == '__main__':
 
#     p_list= []
#     for i in range(10):
#         p = Process(target=func,args=('can_do_girl_lists.txt','小李%s\n'%i,i)) # args 里面主要放func的参数
#         # p = Process(target=func,args=('can_do_girl_info%s.txt'%i,'姑娘电话0000%s'%i))
#         p_list.append(p)
#         p.start()
 
#     [ap.join() for ap in p_list] #这就是个for循环，只不过用列表生成式的形式写的
#     with open('can_do_girl_lists.txt','r',encoding='utf-8') as f:
#         data = f.read()
#         all_num = re.findall('\d+',data) #打开文件，统计一下里面有多少个数据，每个数据都有个数字，所以re匹配一下就行了
#         print('>>>>>',all_num,'.....%s'%(len(all_num)))
#     #print([i in in os.walk(r'你的文件夹路径')])
#     print('啦啦啦~~~~~~~~~~~~~~~~！')


# 2.Process类的使用

# class MyProcess(Process): #自己写一个类，继承Process类
#     #我们通过init方法可以传参数，如果只写一个run方法，那么没法传参数，因为创建对象的是传参就是在init方法里面，面向对象的时候，我们是不是学过
#     def __init__(self,person):
#         super().__init__()
#         self.person=person
#     def run(self):
#         print(os.getpid())
#         print(self.pid)
#         print(self.pid)
#         print('%s 正在和女主播聊天' %self.person)
#     # def start(self):
#     #     #如果你非要写一个start方法，可以这样写，并且在run方法前后，可以写一些其他的逻辑
#     #     self.run()
# if __name__ == '__main__':
#     p1=MyProcess('Jedan')
#     p2=MyProcess('太白')
#     p3=MyProcess('alexDSB')
 
#     p1.start() #start内部会自动调用run方法
#     p2.start()
#     # p2.run()
#     p3.start()
 
 
#     p1.join()
#     p2.join()
#     p3.join()


# #我们说进程之间的数据是隔离的，也就是数据不共享，看下面的验证
# from multiprocessing import Process
# n=100 #首先我定义了一个全局变量，在windows系统中应该把全局变量定义在if __name__ == '__main__'之上就可以了
# def work():
#     global n
#     n=0
#     print('子进程内: ',n)
 
# if __name__ == '__main__':
#     p=Process(target=work)
#     p.start()
#     p.join() #等待子进程执行完毕，如果数据共享的话，我子进程是不是通过global将n改为0了，但是你看打印结果，主进程在子进程执行结束之后，仍然是n=100，子进程n=0，说明子进程对n的修改没有在主进程中生效，说明什么？说明他们之间的数据是隔离的，互相不影响的
#     print('主进程内: ',n)