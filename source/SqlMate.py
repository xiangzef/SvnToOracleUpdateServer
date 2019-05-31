# -*- coding:utf-8 -*-

import sys, os, time,subprocess

# 1.Get SVN Code(In the building)
# 0.Tools Setup(In the building)
# 9.SmartCode(In the building)
strDes = '''
====================================================================
		HUNDSUN Valuation System SOP Tools Build(90109) 
		1.智能数据库升级 - Smart DataBase UPgrade
		2.版本信息创建 - Valuation System Version Create
		Python By 3.7.1
====================================================================
	'''


# 入口函数
def main():
    strInput = input(strDes + "\r\nPlease Input Number(Default Enter With Number 1):")
    if (strInput == '1'):
        print('快速将估值系统版本目录中的所必要sql更新至数据库中.可在版本任意目录中调用')
        hsDatabaseUpgrade('')  # E:\估值V2.6\Release\基金3.0版本\FD20170731\Patch\FD20170731-B27
    elif (strInput == '2'):
        strFile = input("请输入版本名称:")
        hsTools(strFile)
    elif (strInput == ''):
        print('快速将估值系统版本目录中的所必要sql更新至数据库中.可在版本任意目录中调用')
        hsDatabaseUpgrade('')  # E:\估值V2.6\Release\基金3.0版本\FD20170731\Patch\FD20170731-B27


# 数据库升级（原理,将指定目录的相关后台sql打入到数据库中，智能排序）
def hsDatabaseUpgrade(strFolder):
    sUser = ''
    strLocalFolder = ''
    sSyntax = ''
    sType = '1'
    # 确定目录
    strLocalFolder = os.getcwd()
    if (strFolder != ''):
        strLocalFolder = strFolder
    # 截取目录名称到Hsfa3.0_FD的上级版本目录
    if (strLocalFolder.find("Hsfa3.0_FD") > 0):
        strLocalFolder = strLocalFolder[0:strLocalFolder.find("Hsfa3.0_FD") - 1]
    sUser = f_ret_sop_user(strLocalFolder)
    strLocalFolder = strLocalFolder + "\\Hsfa3.0_FD\\"
    # print("调试->找到目录:"+strLocalFolder)
    # 后期可以智能分解拆分找到用户名
    # inStrUser = input("请输入用户名(默认回车{0}):".format(sUser))
    # inStrPwd = input("请输入密码(默认回车{0}):".format(sUser))
    # inStrDB = input("请输入监听服务名(默认回车orcl):")
    if (sUser.find('FD20180816') >= 0) or (sUser.find('Sources')) is True:
       inStrUser = 'FD20180816C'
    elif (sUser.find('I') >= 0) is True:
       inStrUser = 'FD20170307A'
    else:
       inStrUser = sUser
    if (sUser.find('FD20180816') >= 0) or (sUser.find('Sources')) is True:
       inStrPwd = 'FD20180816C'
    elif (sUser.find('I') >= 0) is True:
       inStrPwd = 'FD20170307A'
    else:
       inStrPwd = sUser
    inStrDB = 'orcl'
    # 数据库升级
    f_sqlplus_bat(inStrUser, inStrPwd, inStrDB, '0', strLocalFolder, '', '')
    sqlplusexec(inStrUser, inStrPwd, inStrDB, '1', strLocalFolder, sType)
    sqlplusexec(inStrUser, inStrPwd, inStrDB, '2', strLocalFolder, sType)
    sqlplusexec(inStrUser, inStrPwd, inStrDB, '3', strLocalFolder, sType)
    sqlplusexec(inStrUser, inStrPwd, inStrDB, '4', strLocalFolder, sType)
    sqlplusexec(inStrUser, inStrPwd, inStrDB, '5', strLocalFolder, sType)
    f_sqlplus_bat(inStrUser, inStrPwd, inStrDB, '2', strLocalFolder, '', '')
    f_sqlplus_bat(inStrUser, inStrPwd, inStrDB, '3', strLocalFolder, '', '')
    # p=subprocess.Popen(strLocalFolder + 'HsTools.bat', stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell = True)
    os.system('chcp 65001')
    os.system(strLocalFolder + 'HsTools.bat')
    f_anti_compile_list(inStrUser)
    # os.system('more ' + strLocalFolder + 'anti_compile_list.txt')
    # os.system('pause')
    # f_del_cache_file(strLocalFolder + 'anti_compile_list.txt', '0') 文件删除
    # f_del_cache_file(strLocalFolder + 'HsTools.bat', '0') 文件删除
    # f_del_cache_file(strLocalFolder + 'HsTools.txt', '0')文件删除
    # f_del_cache_file(strLocalFolder + 'HsTools.log', '0')文件删除
    # f_del_cache_file(strLocalFolder + 'HsTools.sql', '0')文件删除
    # f_del_cache_file(strLocalFolder + 'ErrorLine.txt', '0')文件删除


def f_ret_sop_user(sPath):
    sRet = ''
    # sPath = "E:\\估值V2.6\\Release\\基金3.0版本\\FD20170731\\Patch\\FD20170731-B27"
    intCount = sPath.count('\\')
    iPos = findSubStr('\\', sPath, intCount)
    sUser = sPath[iPos + 1:len(sPath)]
    if (sUser.find('-') > 0):
        sUser = sUser[0:sUser.find('-') + 2]
        sUser = sUser.replace('-', '')
    sRet = sUser

    return sRet


def f_anti_compile_list(inStrUser):
    f = open('D:\git\SvnToOracleUpdateServer\output\{0}.log'.format(inStrUser), "r" , encoding='utf-8')
    f1 = open('D:\git\SvnToOracleUpdateServer\output\{0}anti_compile_list.txt'.format(inStrUser), "w", encoding='utf-8')
    # f1 = open(sPath+'ErrorLine.txt',"w+")
    data = f.readlines()

    # 读数据进data
    # 循环data 找编译报错
    i = 0  # 初始化第一行
    for line in data:
        if line.find('创建的包体带有编译错误') >= 0:
            f1.write('编译错误:' + data[i - 5].strip('\n').strip('\'*') + '\n')
        if line.find('创建的函数带有编译错误') >= 0 or line.find('创建的过程带有编译错误') >= 0:
            f1.write('编译错误:' + data[i - 2].strip('\n').strip('\'*') + '\n')
        i = i + 1
    f.close
    f1.close


def f_del_cache_file(sFile, sTag):
    if (os.path.exists(sFile)):
        if (sTag == '1' and os.path.getsize(sFile) == 0) or (sTag != '1'):
            os.remove(sFile)


# sTag 1:执行SQL目录，2.执行DBPackage中的视图,3.执行DBPacakge中的剩下的sql，4.执行DBPackage中剩下的pck包,5.执行DBPackage中剩下的.prc之类的
def sqlplusexec(sUser, sPwd, sDB, sTag, sPath, sType):
    sTmpPath = ''
    sRet = ''
    if (sTag == '1'):
        sTmpPath = 'sql\\'
    else:  # elif (sTag == '2') or (sTag == '3'):
        sTmpPath = 'DBPackage\\'
    strLocalTmp = sPath + sTmpPath
    for root, dirs, files in os.walk(strLocalTmp):
        for file in files:
            if (root == strLocalTmp) and ((os.path.splitext(file)[1] == '.sql') and (sTag == '1') or (sTag != '1')) and \
                    (os.path.splitext(file)[1].find('~') <= 0) and (os.path.splitext(file)[1] != '.txt') and (
                    os.path.splitext(file)[1] != '.log'):
                strFile = os.path.join(root, file)
                if ((strFile.find('sysparam') <= 0) and (sTag == '1')) or \
                        ((file[0:2].upper() == 'V_') and (sTag == '2')) or \
                        ((file[0:2].upper() != 'V_') and (os.path.splitext(file)[1] == '.sql') and (sTag == '3')) or \
                        ((file[0:2].upper() != 'V_') and (os.path.splitext(file)[1] != '.sql') and (
                                os.path.splitext(file)[1] == '.pck') and (sTag == '4')) or \
                        ((file[0:2].upper() != 'V_') and (os.path.splitext(file)[1] != '.sql') and (
                                os.path.splitext(file)[1] != '.pck') and (sTag == '5')):  # 依据SOP排除可选脚本
                    strSql = "sqlplus -S {0}/{1}@{2} @{3}".format(sUser, sPwd, sDB, strFile)
                    if (sType == '0'):
                        print("执行->" + file)
                        b = os.popen(strSql)  # 目前用这个先执行把
                        b = os.popen('Exit')  # 当前记得退出
                    elif (sType == '1'):
                        print("缓冲->" + file)
                        f_sqlplus_bat(sUser, sPwd, sDB, sType, sPath, strFile, file)
                    else:
                        sRet += (strSql + '\r\n')
    return sRet


# Oracle sql执行脚本
def f_sqlplus_bat(sUser, sPwd, sDB, sType, sPath, sFileName, sName):
    sFirst = '''set define off; 
set sqlblanklines on; 
spool D:\git\SvnToOracleUpdateServer\output\{0}.log; 

'''
    sEnd = '''
prompt '**************************10___编译无效对象.sql**************************';
declare
  v_vc_user varchar2(128);
  tmp       varchar2(128);
begin
  select sys.login_user into v_vc_user from dual;
  for v_cur_sql in (select 'alter view ' || t.OBJECT_NAME || ' compile' ssql
                      from user_objects t
                     where t.OBJECT_TYPE = 'VIEW'
                       and t.status = 'INVALID') loop
    begin
      execute immediate v_cur_sql.ssql;
    exception when others then
      tmp := '1';
    end;
  end loop;
  dbms_utility.compile_schema(v_vc_user,false);
end;
/
spool off
Exit;
'''
    strUpdate = '''@echo off
color a
echo *****************************************************************************
echo * 特别特别提醒: 您即将进行数据库升级操作,一旦进行,将不可挽回操作 !!!        * 	
echo * 或者, 您是否需要事先做一次备份呢?                                         *
echo * 您确认继续吗？                                                            *
echo * 如果你完全确认，请回车继续，祝您好运 !                                    *
echo *　　★★★　　　★★★	                                                    *
echo *　★★★★★　★★★★★　     不要经常熬夜,知道吗?家人的幸福依赖您的幸福! *
echo *　★★★★★★★★★★★	                                            *
echo *　　★★★★★★★★★         祝你健康、快乐 !!!                          *
echo *　　　★★★★★★★                                                       *
echo *　　　　★★★★★                                                         *
echo *　　　　　★★★                                                           *
echo *　　　　　　★	                                                            *
echo *****************************************************************************
echo 即将导入到【{0}】
sqlplus {1}/{2}@{3} @{4}
type D:\git\SvnToOracleUpdateServer\output\{1}.log|find /i /n "ora"|more >ErrorLine.txt
cls
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *                       错误信息列示                       *
echo *                                                          *
echo *                                                          *
echo ************************************************************
echo 按任意键显示脚本执行的错误信息

more ErrorLine.txt
echo ************************************************************
echo *                                                          *
echo *                                                          *
echo *                      数据库升级完毕                      *
echo *                                                          *
echo *                                                          *
echo ************************************************************
'''#pause >nul
    if (sType == '0'):
        # 0.头sql文件
        sFile = sPath + 'HsTools.sql'
        f = open(sFile, 'w')  # r只读 w可写 a追加
        f.write(sFirst.format(sUser))
        f.close()
    elif (sType == '1'):
        # 1.追加sql内容文件
        try:
            with open(sFileName, 'r') as f:
                sTxt = f.read()
        except NameError as result:
            print('出错:{0}'.format(result))
        sFile = sPath + 'HsTools.sql'
        # 写入回车,防止串行
        ff = open(sFile, 'a', encoding='utf-8')
        ff.write("\r\nprompt '**************************{0}**************************';\r\n".format(sName))
        ff.close()
        # r只读 w可写 a追加
        fff = open(sFile, 'a', encoding='utf-8')
        fff.write(sTxt)
        fff.close()
    elif (sType == '2'):
        sFile = sPath + 'HsTools.sql'
        f = open(sFile, 'a',encoding='utf-8')  # r只读 w可写 a追加
        f.write(sEnd)
        f.close()
    elif (sType == '3'):
        # 传递进来的必须为最后带\的目录
        sFile = sPath + 'HsTools.bat'
        f = open(sFile, 'w', encoding='utf-8')  # r只读 w可写 a追加
        f.write(strUpdate.format(sUser, sUser, sPwd, sDB, sPath + 'HsTools.sql'))
        f.close()


# hsTools工具
def hsTools(strVerInfo):
    # init
    strFile = ''
    strDate = time.strftime('%Y-%m-%d', time.localtime(time.time()))
    if (strVerInfo != ''):
        strPatch = strVerInfo
    else:
        strPatch = "FD20170731-B15-华金证券资管02-20181217"

    # 分解拼接版本名称
    intCount = strPatch.count('-')
    if (intCount <= 0):
        print("无效的版本信息,应用程式退出")
    iPos = findSubStr('-', strPatch, intCount)
    if (intCount > 1):
        strVer = "Hsfa3.0-" + strPatch[0:iPos]
    else:
        strVer = "Hsfa3.0-" + strPatch
    # Hsfa3.0-FD20170307-E16-增值税通用补丁28-增值税跨年
    # 再次优化,如果有通用补丁字样的,截取通用补丁为止
    if '增值税跨年' in strVer:
        strVer_temp = strVer.split('-')
        strVer = strVer.replace('-' + strVer_temp[-1], '')
    print('截取到版本信息:' + strVer)

    # 拼接版本信息
    strXml = '''<?xml version="1.0" encoding="GB2312"?>
<SystemInfo>
	<Version>
		<ReleaseDate>%s</ReleaseDate>
		<ProductVersion>%s</ProductVersion>
		<Comments></Comments>
	</Version>
</SystemInfo>''' % (strDate, strVer)
    strSql = '''
--版本更新
--================================================================================
update txtcs a
   set VC_CSZ = '%s'
 where a.l_ztbh= 0
   and a.vc_csdm = 'VERSION';
--================================================================================
commit;''' % (strVer)

    # 创建和检查SOP目录
    hsCreateDir(strPatch)

    # 2.创建文件
    strFile = os.getcwd()
    f = open(strFile + '\\' + strPatch + '\\Hsfa3.0_FD\\Bin\\Data\\hsSysInfo.xml', 'w')  # r只读 w可写 a追加
    f.write(strXml)
    f.close()
    # 3.创建sql文件
    f = open(strFile + '\\' + strPatch + '\\Hsfa3.0_FD\\Sql\\HS26-' + strPatch + '.sql', 'a')  # r只读 w可写 a追加
    f.write(strSql)
    f.close()


# input("创建版本信息完成,请按任意键继续......")

# hsTools创建目录
def hsCreateDir(strName):
    strPatch = os.getcwd()
    strPatch += ('\\' + strName + '\\')

    # 创建目录
    mkdir(strPatch)
    # 创建子项目录
    strFile = strPatch + 'Hsfa3.0_FD\\'
    mkdir(strFile)
    mkdir(strFile + 'Bin')
    mkdir(strFile + 'DBPackage')
    mkdir(strFile + 'Detail')
    mkdir(strFile + 'Sql')
    mkdir(strFile + 'Bin\\Data')
    mkdir(strFile + 'Sql\\temp')


def findSubStr(substr, str, i):
    count = 0
    while i > 0:
        index = str.find(substr)
        if index == -1:
            return -1
        else:
            str = str[index + 1:]  # 第一次出现该字符串后后面的字符
            i -= 1
            count = count + index + 1  # 位置数总加起来
    return count - 1


def mkdir(strPath):
    folder = os.path.exists(strPath)
    if not folder:
        os.makedirs(strPath)
    # print('创建%s目录完成'%strPath)


if __name__ == "__main__":
    try:
        exit(main())
    except Exception as exc:
        print(exc)
    else:
        exit()



