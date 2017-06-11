#encoding: utf-8
from server import generic
from server.data_process import avg,hit

class cpu(generic.BaseService):
    def __init__(self):
        super(cpu,self).__init__()
        self.name = "linux_cpu"
        self.interval = 64
        self.plugin_name = "get_cpu_info"
        self.triggers={
            'idle':{'func':avg,
                    'minutes':5,
                    'operator':'lt',
                    'warning':95,
                    'hit':3,
                    'critical':95,
                    'data_type':'percentage'
            },
            'iowait':{'func':hit,
                    'minutes':5,
                    'operator':'gt',
                    'hit':5,
                    'warning':50,
                    'critical':90,
                    'data_type':'int'
            },
        }

class memory(generic.BaseService):
    def __init__(self):
        super(memory, self).__init__()
        self.name='linux_memory'
        self.interval=10
        self.plugin_name='get_memory_info'
        self.triggers={
            'memory_available':{'func':hit,
                     'minutes':60,
                     'operator':'lt',
                     'hit':3,
                     'warning':2019604,
                     'critical':2019604,
                     'data_type':'percentage'
            }
        }

class network(generic.BaseService):
    def __init__(self):
        super(network, self).__init__()
        self.name = 'nic_network'
        self.interval = 120
        self.plugin_name = 'get_network_info'
        self.triggers={
            'in':{'func':avg,
                  'minutes':15,
                  'operator':'gt',
                  'warning':80,
                  'critical':90,
                  'data_type':'percentage'
            }
        }

if __name__=="__main__":
    c = cpu()
    print(c.name,c.interval,c.plugin_name)

