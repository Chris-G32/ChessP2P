import threading
import multiprocessing

inp_res=None
def input_2():
    global inp_res
    inp_res=input("Input: ")
    

def main():
    print("Main func input on thread")
    inp_proc=threading.Thread(target=input_2)
    inp_proc.start()
    
    inp_proc.join()
    print(inp_res)
    
if __name__=="__main__":
    main()
    print("doen")