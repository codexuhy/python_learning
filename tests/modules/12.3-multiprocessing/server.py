#encoding:utf-8
from socket import *
from multiprocessing import Process
 
def talk(conn,client_addr):
    while True:
        try:
            msg=conn.recv(1024)
            print('客户端消息>>',msg)
            if not msg:break
            conn.send(msg.upper())
            #在这里有同学可能会想，我能不能在这里写input来自己输入内容和客户端进行对话？朋友，是这样的，按说是可以的，但是需要什么呢？需要你像我们用pycharm的是一样下面有一个输入内容的控制台，当我们的子进程去执行的时候，我们是没有地方可以显示能够让你输入内容的控制台的，所以你没办法输入，就会给你报错。
        except Exception:
            break
 
if __name__ == '__main__': #windows下start进程一定要写到这下面
    server = socket(AF_INET, SOCK_STREAM)
    # server.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)  # 如果你将如果你将bind这些代码写到if __name__ == '__main__'这行代码的上面，那么地址重用必须要有，因为我们知道windows创建的子进程是对整个当前文件的内容进行的copy，前面说了就像import，如果你开启了子进程，那么子进程是会执行bind的，那么你的主进程bind了这个ip和端口，子进程在进行bind的时候就会报错。
    server.bind(('127.0.0.1', 8080))
    #有同学可能还会想，我为什么多个进程就可以连接一个server段的一个ip和端口了呢，我记得当时说tcp的socket的时候，我是不能在你这个ip和端口被连接的情况下再连接你的啊，这里是因为当时我们就是一个进程，一个进程里面是只能一个连接的，多进程是可以多连接的，这和进程之间是单独的内存空间有关系，先这样记住他，好吗？
    server.listen(5)
    while True:
        conn,client_addr=server.accept()
        p=Process(target=talk,args=(conn,client_addr))
        p.start()