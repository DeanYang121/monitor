#encoding: utf-8
import linux
import time

def alert_cpu_jadge():
    cpu = linux.cpu()
    idle_func = cpu.triggers["idle"]["func"]
    idle_minutes = cpu.triggers["idle"]["minutes"]
    idle_operator = cpu.triggers["idle"]["operator"]
    idle_warning = cpu.triggers["idle"]["warning"]
    idle_critical = cpu.triggers["idle"]["critical"]
    idle_hit = cpu.triggers["idle"]["hit"]
    idle_datatype=cpu.triggers["idle"]["data_type"]
     # print(idle_critical,idle_datatype,idle_minutes)

    _sql = "select avg(idle) from cpu_info where time >= %s"
    _args = (time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-60*idle_minutes)))
    #计算五分钟之内idle的平均值
    idle_func(sql=_sql,args=_args,min=idle_minutes,operator=idle_operator,warning=idle_warning,critical=idle_critical)

def alert_memory_jadge(memory_available):
    memory = linux.memory()
    mem_func = memory.triggers["memory_available"]["func"]
    mem_minutes = memory.triggers["memory_available"]["minutes"]
    mem_operator = memory.triggers["memory_available"]["operator"]
    mem_hit = memory.triggers["memory_available"]["hit"]
    mem_warning = memory.triggers["memory_available"]["warning"]
    mem_critical = memory.triggers["memory_available"]["critical"]
    mem_datatype = memory.triggers["memory_available"]["data_type"]

    _sql = "select mem_available from mem_info where time >= %s"
    _args = (time.strftime("%Y-%m-%d %H:%M:%S",time.localtime(time.time()-60*mem_minutes)))

    mem_func(sql=_sql,args=_args,mem_available=memory_available,min=mem_minutes,operator=mem_operator,hit=mem_hit,warning=mem_warning,critical=mem_critical,data_type=mem_datatype)


if __name__=="__main__":
    alert_memory_jadge("111")
