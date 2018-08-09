def a():
    while(1):
        print("outer loop")
        while(1):
            p=int(input("p daalo= "))
            print(p,type(p))
            if(p):
                continue
            print("didnt go")

a()