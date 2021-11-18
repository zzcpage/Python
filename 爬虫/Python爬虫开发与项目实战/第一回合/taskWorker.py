import time
from multiprocessing.managers import  BaseManager

#处理进程

#创建类似的QueueManager
class QueueManager(BaseManager):
    pass
#第一步使用Queuemanager注册用于获取Queueu的方法名称
QueueManager.register('get_task_queue')
QueueManager.register('get_result_queue')
#第二部连接到服务器
server_addr =  '127.0.0.1'
print('Connect to server %s...'%server_addr)
#端口哦和验证口令
m = QueueManager(address=(server_addr,8001),authkey='qiye'.encode('utf-8'))
#从网络链接
m.connect()
#第三步获取Queue的对象
task = m.get_task_queue()
result = m.get_result_queue()
#第四步，从task队列获取任务，把结果写入到result队列
while(not task.empty()):
    image_url = task.get(True,timeout=5)
    print('run task download %s...'%image_url)
    time.sleep(1)
    result.put("%s--->success"%image_url)
#处理结束
print('worker exit .')
