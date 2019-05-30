# -*- coding: utf-8 -*-


# ------------------------文件1
# 模块1 ：
# 控制模块
# setting{输入定时时间，
# svn目录，递归自查询每条线最大的那个目录
# svn url  ，
# svn客户端目录，
# 更新文件存放目录 ，
# 报错信息存放目录，
# html存放目录，
# 邮件发送目标，
# 本地邮件登录信息，}
#
# 功能class {
# 	调用 模块2 功能 1
# 	调用 模块3 功能 1  功能2
# 	调用 模块4 功能 1  功能2
# }
#
# def _main_  ():
# {
# 	class
# }

import os

setting={
    'svn':r'C:\Program Files\TortoiseSVN\bin',#svn的程序所在路径
    'url':'https://192.168.57.209/fund/dept2/Evaluation2.6/估值V2.6/Release/基金3.0版本',#svn地址
    'dist':u'D:\\Evaluation2.6\\估值V2.6\\Release\\基金3.0版本',#目标地址
    'closeOption': ' /closeonend:1'
    #'interval':15 #更新时间
}

# /closeonend:0 不自动关闭对话框
# /closeonend:1 如果没发生错误则自动关闭对话框
# /closeonend:2 如果没发生错误和冲突则自动关闭对话框
# /closeonend:3如果没有错误、冲突和合并，会自动关闭
# /closeonend:4如果没有错误、冲突和合并，会自动关闭

class list_dir:
    d = ''
    res = ''
    def __init__(self,dir):
        self.d = dir

    def work_dir(self):
         for root, dirs, files in os.walk(self.d):
            print('\n========================================')
            print("root : {0}".format(root))
            print("dirs : {0}".format(dirs))
            print("files : {0}".format(files))

if __name__ == '__main__':
    d = list_dir(setting['dist'])
    d.work_dir()
