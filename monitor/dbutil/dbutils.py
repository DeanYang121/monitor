#encoding:utf-8
import pymysql
import dbconfig as dbconf

class Mysql_connection():
    def __init__(self):
        self.__port = dbconf.MYSQL_PORT
        self.__host = dbconf.MYSQL_HOST
        self.__user = dbconf.MYSQL_USER
        self.__pwd = dbconf.MYSQL_PASSWD
        self.__db = dbconf.MYSQL_DB
        self.__charset = dbconf.MYSQL_CHARSET
        self.__socket = dbconf.Unix_socket
        self.__conn = None
        self.__cur  = None
        self.__connect()

    def __connect(self):
        try:
            self.__conn = pymysql.connect(host=self.__host,port=self.__port,user=self.__user,db=self.__db, \
                                    passwd=self.__pwd,charset=self.__charset,unix_socket=self.__socket)
            self.__cur = self.__conn.cursor()
        except BaseException as e:
            print(str(e))


    def execute(self,sql,args=()):
        _cnt = 0
        if self.__cur:
            _cnt = self.__cur.execute(sql,args)

        return _cnt

    def fetch(self,sql,args=()):
        _cnt = 0
        _rt_list = []
        if self.__cur:
            _cnt = self.__cur.execute(sql,args)
            _rt_list = self.__cur.fetchall()
        return _cnt,_rt_list

    def commit(self):
        if self.__conn:
            self.__conn.commit()

    def close(self):
        if self.__cur:
            self.__cur.close()
            self.__cur=None
        if self.__conn:
            self.__conn.close()
            self.__conn=None

    def execute_sql(self,sql,args,fetch=True):
        _cnt = 0
        _rt_list = []
        # print(sql)
        # print(self.__cur)
        # print(fetch)
        if fetch:
            if self.__cur:
                _cnt = self.__cur.execute(sql, args)
                _rt_list = self.__cur.fetchall()
        elif self.__cur:
            _cnt = self.__cur.execute(sql, args)
            self.__conn.commit()

        if self.__cur:
            self.__cur.close()
            self.__cur=None
        if self.__conn:
            self.__conn.close()
            self.__conn=None

        return _cnt, _rt_list


    @classmethod
    def bulker_commit_sql(cls,sql,args_lists=[]):
        _cnt = 0
        _rt_list = []
        _conn = Mysql_connection(host=dbconf.MYSQL_HOST,user=dbconf.MYSQL_DB,\
                                passwd=dbconf.MYSQL_PASSWD,port=dbconf.MYSQL_PORT,\
                                charset=dbconf.MYSQL_CHARSET,db=dbconf.MYSQL_DB, \
                                unix_socket=dbconf.Unix_socket
                                )
        for _args in args_lists:
            _cnt += _conn.execute(sql,_args)
        _conn.commit()

        return _cnt,_rt_list


if __name__=='__main__':
    sql = 'select username,password from user where username=%s and password=md5(%s)'
    args = ('dean','123456')
    t = Mysql_connection()
    _cnt,_rt_list = t.execute_sql(sql,args)
    print(_cnt)
    print(_rt_list)
    # _sql = "update user set password=md5(%s) where id = %s"
    # user_pwd='111111'
    # user_id='3'







