from fileinput import close
from platform import release
import socket, threading
import math

mahdismutex=threading.Lock()
allowed_actions=[]
allowed_actions.append("ViewSold")
allowed_actions.append("ViewTR")
allowed_actions.append("ViewF")
allowed_actions.append("Deposit")
allowed_actions.append("Withdraw")
current_threads=[]
msgsize=1024
facts="facture.txt"
accs="accounts.txt"
hist="history.txt"
class ClientThread(threading.Thread):
    def __init__(self,clientAddress,clientsocket):
        threading.Thread.__init__(self)
        self.csocket = clientsocket
        print ("New connection added: ", clientAddress)
    def run(self):
        #found the definition for this in here https://docs.python.org/3/library/threading.html#threading.Thread.run    :
        #You may override this method in a subclass. 
        #The standard run() method invokes the callable object passed to the object’s constructor as the target argument, 
        #if any, with positional and keyword arguments taken from the args and kwargs arguments, respectively.
        print ("Connection from : ", clientAddress)
        self.csocket.send(bytes("hello",'utf-8'))
        rsp = ''
        while True:
            try:
                data = self.csocket.recv(3072)          
            except socket.error as e:
                print("socket disconnected")
                break
            rsp = data.decode()
            if rsp!="hello":
                print("communication from client required action:",rsp.split(",")[0])
                keyword=rsp.split(",")[0]
                if keyword in allowed_actions:
                    notify(clientAddress,rsp,self.csocket)
                elif rsp=='bye':
                    break
                #print ("from client:", msg)
                else:
                    msg="Not a known action"
                    self.csocket.send(bytes(msg,'UTF-8'))
            else:
                self.csocket.send(bytes("hello",'UTF-8')) 

        print("Client at ", clientAddress , " disconnected...")   
#end of class
def notify(ip,message,csock):
    elements=message.split(",")
    if elements[0] == "ViewSold":
        msg=GetSold(elements[1])

        csock.send(bytes(msg,'UTF-8'))
    if elements[0] == "ViewTR":
        msg=GetTransactions(elements[1])

        csock.send(bytes(msg,'UTF-8'))
    if elements[0] =="ViewF":
        msg=GetFacture(elements[1])
        csock.send(bytes(msg,'UTF-8'))  
    if elements[0] == "Deposit":
        mahdismutex.acquire()
        if(Deposit(int(elements[1]),int(elements[2]))):
            
            msg="successful deposit"
            csock.send(bytes(msg,'UTF-8'))
        else:
            msg="wrong account reference"
            csock.send(bytes(msg,'UTF-8'))
        mahdismutex.release()
    if elements[0] == "Withdraw":
        mahdismutex.acquire()
        if(Withdraw(int(elements[1]),int(elements[2]))):
            msg="successfull withdrawal"
            csock.send(bytes(msg,'UTF-8'))
        else:
            msg="withdrawal failed"
            csock.send(bytes(msg,'UTF-8'))          
        mahdismutex.release()





def GetSold(ref):
    accounts =open("accounts.txt",'r') 
    ac_list_of_lines = accounts.readlines()
    for i in ac_list_of_lines:
        columns=i.split(',')
        if int(columns[0])==int(ref):
            sign = -1 if columns[2]=="Negativ"  else 1
            accounts.close()
            msg="\nyour balance is:{}".format(int(columns[1])*sign)   
            return  msg
    return "account not found!"

def GetTransactions(ref):
    response=""
    history =open("history.txt",'r') 
    hs_list_of_lines = history.readlines()
    for i in hs_list_of_lines:
        columns=i.split(',')
        if int(columns[0])==int(ref):
            response+="Transaction:\nType:{}   Value:{}   Result:{}   Account-Status-After-Transactions:{}\n".format(columns[1],columns[2],columns[3],columns[4])
    history.close()
    if response=="":
        response="No transactions made under this accounts reference"
    return response

def GetFacture(ref):
    facture =open("facture.txt",'r') 
    fs_list_of_lines = facture.readlines()
    for i in fs_list_of_lines:
        columns=i.split(',')
        if int(columns[0])==int(ref):
            return "Facture to pay next time:"+columns[1]
    return "account not found!"

def AcountExists(ref):
    accounts=open(accs,"r")
    ac_list_of_lines = accounts.readlines()
    facturedamount=0
    for i in range(len(ac_list_of_lines)):
        columns=ac_list_of_lines[i].split(',')
        if int(columns[0])==ref:
            return True
    return False

def UpdateBill(ref,value):#ref mta3 l compte , val hiya li valeur li jbedha
    accounts=open(accs,"r")
    ac_list_of_lines = accounts.readlines()
    facturedamount=0
    for i in range(len(ac_list_of_lines)):
        columns=ac_list_of_lines[i].split(',')
        if int(columns[0])==ref:
            if(columns[2]=="Negativ"):
                facturedamount=value*0.02
            else:
                amount=int(columns[1])
                if ((amount-value)<0 ):
                    facturedamount=-(amount-value)*0.02
                    print("a facture is due")
                    break
                else:
                    break
    facture=open("facture.txt","r")
    fa_list_of_lines = facture.readlines()

    for i in range(len(fa_list_of_lines)):
        columns=fa_list_of_lines[i].split(',')
        if columns[0]=="\n":
            break
        if int(columns[0])==ref:
            print("factured amount:",facturedamount)
            columns[1]=math.trunc(facturedamount + int(columns[1]))
            if (i< len(fa_list_of_lines)-1):
                fa_list_of_lines[i]="{},{}\n".format(columns[0],columns[1])
                facture.close()
            else :
                fa_list_of_lines[i]="{},{}\n".format(columns[0],columns[1])
                facture.close()
            break
    open('facture.txt', 'w').close()
    facture=open("facture.txt","a")
    #PRINT ZAYEDA
    print(fa_list_of_lines)
    for i in fa_list_of_lines:
        facture.write(i)

def Withdraw(ref,amount):
    success=False
    isNegative=False
    if amount<0:
        print("cannot withdraw negativ money nice try XD")
        return False
    if AcountExists(ref):
        accounts=open(accs,"r")
        ac_list_of_lines = accounts.readlines()
        for i in range(len(ac_list_of_lines)):
            columns=ac_list_of_lines[i].split(',')
            if int(columns[0])==ref:
                if(columns[2]=="Negativ"):
                    isNegative=True
                    
                    if (int(columns[1])+amount)<=int(columns[3]):
                        UpdateBill(ref,amount)
                        columns[1]=int(columns[1])+amount
                        ac_list_of_lines[i]="{},{},Negativ,{}".format(columns[0],columns[1],columns[3])
                        accounts.close()
                        success=True
                        break

                        
                if(columns[2]=="Positiv"):
                    if (int(columns[1])-amount)>0:
                        columns[1]=int(columns[1])-amount
                        ac_list_of_lines[i]="{},{},Positiv,{}".format(columns[0],columns[1],columns[3])
                        accounts.close()
                        success=True
                        break
                    elif abs(int(columns[1])-amount)<= int(columns[3]):
                        UpdateBill(ref,amount)
                        ac_list_of_lines[i]="{},{},Negativ,{}".format(columns[0],abs(int(columns[1])-amount),columns[3])
                        accounts.close()
                        success=True
                        isNegative=True
                        break
        open('accounts.txt', 'w').close()  
        accounts=open(accs,"a")
        for i in ac_list_of_lines:
            accounts.write(i)
        history =open(hist,'a') 
        if success:
            if isNegative:
                history.write("\n{},Withdrawal,{},Success,Negativ".format(ref,amount))
            else:
                history.write("\n{},Withdrawal,{},Success,Positiv".format(ref,amount))
        else:
            if isNegative:
                history.write("\n{},Withdrawal,{},Failure,Negativ".format(ref,amount))
            else:
                history.write("\n{},Withdrawal,{},Failure,Positiv".format(ref,amount))
        history.close()
        return success              
    else:
        return False

def Deposit(ref,amount):
    if(AcountExists(ref)):
        #file opened
        facture=open(facts,"r") ##time to pay your debt buddy
        fa_list_of_lines=facture.readlines()
        facture.close()
        accounts=open(accs,"r")
        ac_list_of_lines=accounts.readlines()
        accounts.close()
        history=open(hist,"a")
        for i in range(len(fa_list_of_lines)):
            columns=fa_list_of_lines[i].split(',')
            if int(columns[0])==ref:
                if(int(columns[1])>=amount):
                    columns[1]=int(columns[1])-amount
                    amount=0
                    fa_list_of_lines[i]="{},{}".format(columns[0],columns[1])
                else:
                    amount-=int(columns[1])
                    columns[1]=0
                    if(i!=len(fa_list_of_lines)-1):
                        fa_list_of_lines[i]="{},{}\n".format(columns[0],columns[1])
                    else:
                        fa_list_of_lines[i]="{},{}".format(columns[0],columns[1])

                #updating the accounts after paying debts
                #file opened
                for i in range(len(ac_list_of_lines)):
                    columns=ac_list_of_lines[i].split(',')
                    if int(columns[0])==ref:
                        if(columns[2]=="Negativ"):
                            if  int(columns[1])>amount:
                                columns[1]= int(columns[1])-amount
                                ac_list_of_lines[i]="{},{},{},{}".format(columns[0],columns[1],columns[2],columns[3]) 
                                #156,Withdrawal,100,Success,Negativ format
                                history.write("\n{},Deposit,{},Success,Negativ".format(columns[0],amount)) 
                                
                            else:
                                history.write("\n{},Deposit,{},Success,Positiv".format(columns[0],amount)) 
                                columns[1]= amount-int(columns[1])
                                columns[2]=="Positiv"
                                ac_list_of_lines[i]="{},{},{},{}".format(columns[0],columns[1],"Positiv",columns[3])   
                                

                            
                        else:
                            columns[1]= int(columns[1])+amount
                            history.write("\n{},Deposit,{},Success,Positiv".format(columns[0],amount)) 
                            ac_list_of_lines[i]="{},{},{},{}".format(columns[0],columns[1],columns[2],columns[3])  
                            

        print(ac_list_of_lines)
        history.close()
        open(accs,'w').close()  
        open(facts,'w').close() 
        accounts=open(accs,"a")
        factures=open(facts,"a")
        for i in ac_list_of_lines:
            accounts.write(i)        
        for i in fa_list_of_lines:
            factures.write(i)
        accounts.close()
        factures.close() 
        return True
    else:
        return False       
        
              
LOCALHOST = "127.0.0.1"
PORT = 8080
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#type=socket.SOCK_DGRAM for udp

server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

server.bind((LOCALHOST, PORT))

print("Server is up")
print("Waiting for client request..")
while True:#main boucle XD
    server.listen(1)
    clientsock, clientAddress = server.accept()# returns  a couple (sock,address)
    newthread = ClientThread(clientAddress, clientsock)
    newthread.start()
    current_threads.append(newthread)