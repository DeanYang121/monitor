#encoding:utf-8
from dbutil.dbutils import Mysql_connection

def data2db(sql,args,fetch=True):
    t = Mysql_connection()
    _cnt = 0
    _rt_list = []
    # print(fetch)
    if fetch:
        _cnt,_rt_list = t.execute_sql(sql,args)
    else:
        _cnt = t.execute_sql(sql,args,fetch=False)

    return _cnt,_rt_list

if __name__=="__main__":
    _cnt = 0
    items = 0
    values = 0
    # _sql = "insert into cpu_info{0} value{1}".format(items,values)
    # _args = ("1","2","3","4","5","6","7")
    # _cnt,_rt_lists = data2db(_sql,_args,fetch=False)
    # print(_cnt,_rt_lists)
    _sql = "select count(id) from cpu_info"
    _cnt,_rt=data2db(_sql,())
    print(_cnt,_rt)

