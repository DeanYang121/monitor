#encoding:utf-8

def fun(*args,**kwargs):
    print("*args:",args)
    print("**kwargs",kwargs)



if __name__=="__main__":
    a =[1,2,3,4]
    b = {"a":2,"b":3,"c":4}
    fun(v=1,b=2,c=3)
    sum = 0
    for i in range(6,27):
        sum += i

    print(sum/21)
