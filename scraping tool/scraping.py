from built_functions import *
import threading
import numpy as np




product_name=input("Enter the name of product =")
if " " in product_name:
    product_name.replace(" ","+")




#Thread concept
#for the first thread
f_thred_start,f_thred_end=map(int,input("Enter the first thread value=").split(" "))
s_thred_start,s_thred_end=map(int,input("Enter the second thread value=").split(" "))
t_thred_start,t_thred_end=map(int,input("Enter the third thread value=").split(" "))
if __name__=="__main__":
    t1=threading.Thread(target=main,args=(f_thred_start,f_thred_end,product_name))
    t2=threading.Thread(target=main,args=(s_thred_start,f_thred_end,product_name))
    t3=threading.Thread(target=main,args=(t_thred_start,t_thred_end,product_name))
    

    t1.start()
    t2.start()
    t3.start()
    

    t1.join()
    t2.join()
    t3.join()
    


    print("Done Sucessfully")


