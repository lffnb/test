# -*- coding: UTF-8 -*-
import os

routes = []

def search(curpath, s):
    L = os.listdir(curpath)  #列出当前目录下所有文件
    for subpath in L:  #遍历当前目录所有文件
        if os.path.isdir(os.path.join(curpath, subpath)):  #若文件仍为目录，递归查找子目录
            newpath = os.path.join(curpath, subpath)
            search(newpath, s)
        elif os.path.isfile(os.path.join(curpath, subpath)):  #若为文件，判断是否包含搜索字串
            if s in subpath:
                routes.append(os.path.join(curpath, subpath))


# -*- coding: utf-8 -*-
# 1.读取客户端发来的文件名
# 2.查找文件是否存在
# 3.打开该文件
# 4.检测文件大小
# 5.发送大小给客户端
# 6.等待客户端确认
# 7.开始边读边发
# 8.发送md5校验

import socket
import os
import hashlib

def server():
    server = socket.socket()
    server.bind(('192.168.1.11', 8080))
    server.listen(5)
    while True:
        conn, addr = server.accept()
        print('等待指令：')
        while True:
            data = conn.recv(1024)
            if not data:
                print('客户端断开')
                break

            # 第一次接收的是命令，包括get和文件名，用filename接受文件名
            cmd, filename = data.decode().split(' ')
            print(filename)
            search('/home', str(filename))
            print(routes)
            conn.send(str(len(routes)))   #发送文件数

            for file in routes:
                # 接收到的文件名判断是不是一个文件
                if os.path.isfile(file):

                    # 如果是，读模式打开这个文件
                    f = open(file, 'rb')

                    # 将文件大小赋值给file_size
                    file_size = os.stat(file).st_size

                    # 发送文件大小
                    conn.send(str(file_size).encode())

                    # 接收确认信息
                    conn.recv(1024)

                    # 发送文件名
                    conn.send(file)

                    # 接收确认信息
                    conn.recv(1024)

                    # 开始发文件
                    for line in f:

                        # 一行一行发送
                        conn.send(line)

                    # 关闭文件
                    f.close()

                print('send done')
        break
    server.close()

#main函数
if __name__ == '__main__':
    print("dameon开始运行！")
    server()

