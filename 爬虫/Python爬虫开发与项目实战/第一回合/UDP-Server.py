# UDP 服务器端
"""
UDP是面向无连接的协议。使用UDP协议时，不需要建立连接，只需要直到对方的IP地址和端口号，就可以直接发数据包。
并不关心能够到达目的端。对于不要求可靠到达的数据，就可以使用UDP协议。
"""
"""
服务端创建过程：
    1. 创建Socket，绑定指定的ip和端口
    2. 直接发送数据和接收数据
    3. 关闭Socket
"""
import socket

# 创建Socket,绑定指定IP和端口
# SOCK_DGRAM指定了这个Socket的类型是UDP，绑定端口和TCP示例一样
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.bind(('127.0.0.1', 9999))
print('Bind UDP on 9999...')
while True:
    # 直接发送数据和接收数据
    data, addr = s.recvfrom(1024)
    print('Received from %s:%s. ' %(addr,data.decode('utf-8')))
    s.sendto(b'Hello,!', addr)
