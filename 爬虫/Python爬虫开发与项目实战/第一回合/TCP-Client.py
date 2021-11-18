
#TCP客户端

"""
1.创建Socket，连接远端地址
2.连接后发送数据和接收数据
3.传输完毕后，关闭Socket
"""
import socket
#初始化Socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
#连接目标的ip和端口
s.connect(('127.0.0.1',9999))
#接收消息
print('--->>>'+s.recv(1024).decode('utf-8'))
#发送消息
s.send(b'Hello,I am Client')
print('--->'+s.recv(1024).decode('utf-8'))
s.send(b'exit')
#关闭Socket
s.close()