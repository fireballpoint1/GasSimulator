def f():
    a=1
    b=2
    #ff()
    #print(p,q)
    def ff():
        p=a*a
        q=b*b
        globals().update(locals())
    ff()
    print(p,q)
f()
