import os
from multiprocessing import Process,Pool,Queue,Pipe
import os,time,random,threading

from gevent import monkey;monkey.patch_all()
import gevent
import urllib3
### 导入序列化模块
try:
    import cPickle as pickle
except ImportError:
    import pickle

def 序列化():

    """
        pickle实现序列化主要使用dumps方法或dump方法，
        dumps方法可以将任意对象序列化成一个str，然后可以将这个str写入文件进行保存.
        dump方法可以将序列化后的对象直接写入到文件中

        pickle实现反序列化，主要通过loads或load方法，把序列化后的文件从磁盘上读取一个str，然后使用loads方法将str转化位对象
        或者直接使用load方法将文件直接反序列化位对象
    """
    #dumps
    d = dict(url="index.html",title="首页",content="首页")
    str = pickle.dumps(d)
    print(str)

    #dump
    f = open(r'dump.txt','wb')
    pickle.dump(d,f)
    f.close()

    #通过load方法
    f = open(r'dump.txt','rb')
    d = pickle.load(f)
    f.close()
    print(d)

# print('current Process %s start...'%(os.getpid()))
# pid = os.fork()
# if pid<0:
#     print('error in fork')
# elif pid == 0 :
#     print('I am child process(%s)'%(os.getpid()))
# else:
#     print('i am %s'%(os.getpid()))


#multiprocessing模块创建多进程

#通过Process类来描述一个进程对象，创建子进程时，只需要传入一个执行函数和函数参数，
#即可完成一个Process实例的创建，用strt()方法启动进程，用join方法实现进程间的同步

#子进程要执行的代码
def run_proc(name):
    print('Child process %s (%s) Running...'%(name,os.getpid()))

##进程池任务
def run_task(name):
    print('Task %s (pid=%s) is runing...'%(name,os.getpid()))
    time.sleep(random.random()*3)
    print('Task %s end.'%name)
#写数据进程执行的代码
def proc_write(q,urls):
    print('Process(%s) is writing...'%os.getpid())
    for url in urls:
        q.put(url)
        print('Put %s queue...'%url)
        time.sleep(random.random())
#读数据进程执行的代码
def proc_read(q):
    print('Process(%s) is reading'%os.getpid())
    while True:
        url = q.get(True)
        print('Get %s from queue.'%url)
def 多进程():
    # print('Parent process %s.'%os.getpid())
    # for i in range(5):
    #     p = Process(target=run_proc,args=(str(i),))#指定子进程要执行的方法，以及传递的参数
    #     print('Process will start.')
    #     p.start()
    # p.join()
    # print('Process end')

    # 通过进程池创建多个进程
    print('Current process %s.' % os.getpid())
    p = Pool(processes=3)  # 创建进程池，指定进程池中进程的个数，默认位CPU核数
    for i in range(5):
        p.apply_async(run_task, args=(i,))
    print('Waiting for all subprocess done ...')
    p.close()  # g关闭进程池，就不能继续向进程池中添加新的任务
    p.join()  # 使用join表示等待所有子进程结束

    # 进程通信 通过Queue或者Pipe(一般用于两个进程通信)实现进程通信
    # 通过Queue进行get和put操作，可以设置blocked和timeout两个属性，blocked是设定操作是否阻塞
    # timeout是设置操作的等待时间。
    q = Queue()  # 创建消息队列
    proc_write1 = Process(target=proc_write, args=(q, ['url_1', 'url_2', 'url_3']))
    proc_write2 = Process(target=proc_write, args=(q, ['url_4', 'url_5', 'url_6']))
    proc_reader = Process(target=proc_read, args=(q,))
    # 启动子进程proc_writer写入
    proc_write1.start()
    proc_write2.start()
    # 启动子进程读取
    proc_reader.start()
    # 等待写入结束
    proc_write1.join()
    proc_write2.join()
    # 由于读取是死循环，所以只能强行终止
    proc_reader.terminate()

#多线程
def thread_run(urls):
    print('Current %s is running ...'%threading.current_thread().name)
    for url in urls:
        print('%s ------>>> %s'%(threading.current_thread().name,url))
        time.sleep(random.random())
    print('%s ended.'% threading.current_thread().name)

#继承创建线程类
class MyThread(threading.Thread):
    def __init__(self,name,urls):
        threading.Thread.__init__(self,name=name)
        self.urls =urls
    def run(self):
        print('Current %s is running ...' % threading.current_thread().name)
        for url in self.urls:
            print('%s ------>>> %s' % (threading.current_thread().name, url))
            time.sleep(random.random())
        print('%s ended.' % threading.current_thread().name)

def 多线程():
    """"
         多线程，线程类似于执行多个不同的程序，多线程可以将允许时间长的任务放到后台处理。
         Python对多线程的支持，thread和threading，一般我们使用threading模块
     """
    print('%s is running...' % threading.current_thread().name)
    t1 = threading.Thread(target=thread_run, name='Thread_1', args=(['url_1', 'url_2', 'url_3'],))
    t2 = threading.Thread(target=thread_run, name='Thread_2', args=(['url_4', 'url_5', 'url_6'],))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('%s ended.' % threading.current_thread().name)

    # 自定义线程类
    print('%s is running...' % threading.current_thread().name)
    t1 = MyThread(name='Thread_1', urls=(['url_1', 'url_2', 'url_3']))
    t2 = MyThread(name='Thread_2', urls=(['url_4', 'url_5', 'url_6']))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    print('%s ended.' % threading.current_thread().name)

    ##线程同步
    ##一般通过Thread的Lock和RLock实现简单的线程同步，两个对象都有acquire和release方法
    mylock = threading.RLock()  # 创建一个锁
    num = 0

    class myThread1(threading.Thread):
        def __init__(self, name):
            threading.Thread.__init__(self, name=name)

        def run(self):
            global num
            while True:
                mylock.acquire()
                print('%s locked,Number :%d' % (threading.current_thread().name, num))
                if num >= 4:
                    mylock.release()
                    print('%s released, Number: %s' % (threading.current_thread().name, num))
                    break
                num += 1
                print('%s released Number %s' % (threading.current_thread().name, num))
                mylock.release()

    thread1 = myThread1('Thread_1')
    thread2 = myThread1('Thread_2')
    thread1.start()
    thread2.start()

#各个协程执行的任务
def run_task(url):
    print('Visis --> %s'%url)
    try:
        data  = urllib3.connection_from_url(url=url).urlopen(url=url,method="GET").data
        print('%s bytes received from %s.'%(len(data),url))
    except Exception as e:
        print(e)


def 协程():
    # 协程又称微线程(纤程),用户级的轻量级线程
    # 协程能够保留上一次调用时的状态
    # Python对写出的支持通过gevent库，Python通过yield提供对协程的基本支持但是不完全，所以使用
    # gevent更加好
    # gevent实际上是greenlet在实现切换工作。如果出现io阻塞的时候，gevent会自动切换到没有阻塞的代码执行
    # 所以gevent一直保持greenlet在允许
    urls = ['https://github.com/', 'https://www.python.org/', 'http://www.baidu.com/']  # 各个协程访问的网址
    greenlets = [gevent.spawn(run_task, url) for url in urls]  # 这里将各个协程加入到greenlets中
    gevent.joinall(greenlets=greenlets)  # 进行执行各个协程

if __name__ == '__main__':
    print('in')
    """
        分布式进程：分布式也就是将计算任务分布到多个计算机上进行运算，然后将结果返回。分布式进程
        也就是指，将Process进程分不到多台机器，利用多台机器的性能，完成复杂的任务。
        
        对于分布式进程，通过multiprocessing模块的managers子模块，将多线程分布到多台机器上。
        一般我们通过分布式处理任务，将某块的任务分配给某个机器执行，然后某个功能模块给其他模块执行。将任务分成多个
        计算机集群进行处理，提高速度。例如爬取图片，可以一个计算机专门爬取图片链接，然后多个计算机专门根据
        爬取到的图片链接下载图片。
        
        将中间处理的结果，让其他机器进程都能访问的过程称为本地队列的网络化。
        
        创建分布式进程的六个步骤：
        1. 建立消息队列Queue,用于进程间的通信。服务进程创建任务队列task_queue用来作为传递任务给任务进程的通道。
        服务进程创建结果队列result_queue作为任务进程完成任务后回复服务进程的通道。在分布式多进程环境下，
        必须通过Queuemanager获得Queue接口来添加任务
        
        2. 把第一步建立的队列，在网络上注册，暴露给其他进程(主机)，注册后获得网络队列，相当于本地队列的映像。
        
        3.建立一个对象Queuemanager。绑定端口和验证口令
        4.启动第三步的对象实例，监管信道通道
        5.通过管理实例的方法获得通过网络访问的Queue对象，也就是再把网络队列实体化成可以使用的本地队列。
        6.创建任务到本地队列中。自动上传任务到网络队列中，分配给任务进程进行处理。
        
    """

