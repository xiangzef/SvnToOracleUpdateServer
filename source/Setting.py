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

import os,time
import re
import cx_Oracle
import SqlMate
#import svnconfig
# import pandas as pd

os.environ['NLS_LANG'] = 'SIMPLIFIED CHINESE_CHINA.UTF8'
# defaultencoding = 'utf8'

logs = []

setting={
    'svn':r'C:\Program Files\TortoiseSVN\bin',#svn的程序所在路径
    'url':'https://192.168.57.209/fund/dept2/Evaluation2.6/估值V2.6/Release/基金3.0版本',#svn地址
    'dist':u'D:\\Evaluation2.6\\估值V2.6\\Release\\基金3.0版本',#目标地址
    'closeOption': ' /closeonend:1',
    'logFile': 'D:\git\SvnToOracleUpdateServer\source\logFile.txt', #　log文件放置位置
    'version': ['0307-D','0307-C','0307-I','0816-C'],
    'versions': ['0307-C']
    #'interval':15 #更新时间
}

# /closeonend:0 不自动关闭对话框
# /closeonend:1 如果没发生错误则自动关闭对话框
# /closeonend:2 如果没发生错误和冲突则自动关闭对话框
# /closeonend:3如果没有错误、冲突和合并，会自动关闭
# /closeonend:4如果没有错误、冲突和合并，会自动关闭

class list_dir:#递归查询当前目录下的所有目录，对地址进行递归查询出所有的svn本地目录生成一个list
    d = ''
    res = ''
    edition_num = []
    task = {'版本': '', '版本号': '', '本地目录': '', 'svn目录': ''}
    tasks = []
    def __init__(self, dir):
        self.d = dir

    def work_dir(self):#查出所有的版本
         for root, dirs, files in os.walk(self.d):
             for dir in dirs:
                 if re.compile('FD20[0-9]{6}-[A-Za-z]').match(dir) :
                     them = re.findall('FD20[0-9]{6}',dir)
                     it = re.findall('-[A-Za-z][0-9]*',dir)
                     it = it[0].strip('-')
                     url = setting['url']+'/'+them[0]+'/Patch/'+dir
                     self.Append_task(dir,it,root+'\\'+dir,url)
         return self.tasks


    def Append_task(self,a,b,c,d):#自增序列
        self.task['版本']=a
        self.task['版本号']=b
        self.task['本地目录']=c
        self.task['svn目录']=d
        self.tasks.append(dict(self.task))
        return self.task



class svn:
    def svn_update(self,dist_lists):
        i = 0
        for dist in dist_lists:
            for version in setting['versions']:
                if str(dist[2]).find(version) > 0:
                    i+=1
            if i >0 :
                cmd = 'TortoiseProc.exe /command:update /path ' + dist[2] + setting['closeOption']
                # 记录下更新的时间
                log_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())
                log = 'Execute ' + cmd + " --- Time " + log_time + '\n'
                logs.append(log)

                #   执行更新   （这里后面还需要加上对更新失败的处理）
                update_result = os.system(cmd)

                #  更新完毕，添加成功与否的log
                if update_result == 0:
                    log = 'SUCCESS: update ' + dist[2] + ' success' + '\n'
                else:
                    log = 'FAIL: update ' + dist[2] + ' fail' + '\n'
                logs.append(log)
                SqlMate.hsDatabaseUpgrade(dist[2])
            i = 0
            # 将log写入给定的log file

        with open(setting['logFile'], 'a', encoding="utf-8") as f:
            logs.append("******************************************************** next update\r\n")
            for l in logs:
                f.write(l)
        logs.clear()



#主程序入口
if __name__ == '__main__':

    conn = cx_Oracle.connect('FD20180816C/FD20180816C@localhost/orcl')  # 用自己的实际数据库用户名、密码、主机ip地址 替换即可
    curs = conn.cursor()

    if 1==2 :#执行插入语句
        d = list_dir(setting['dist'])
        tasks = d.work_dir()
        for task in tasks :
            sql = 'insert into Tupdate (edition,tversion, dir, turl) select \'{0}\',\'{1}\',\'{2}\',\'{3}\' from' \
                  ' dual t where not exists( select 1 from tupdate t where \'{0}\' = t.edition)'.format(task['版本'],task['版本号'],task['本地目录'],task['svn目录'])
            print(sql)
            rr = curs.execute(sql)

    if 1==1 :#执行查询语句
        v_l_mode = 1#1：更新rn且查询
        return_str = '                  '
        rs1 =  curs.var(cx_Oracle.CURSOR)
        zz = curs.callproc('searchversion', [v_l_mode,return_str,rs1])
        s = svn()
        s.svn_update(zz[2])
    conn.commit()
    curs.close()
    conn.close()