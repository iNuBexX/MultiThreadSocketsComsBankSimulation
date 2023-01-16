
import os
import socket

clear = lambda: os.system('cls')
def viewsold_c(client):
  clear()
  print("enter the rib account to view your sold:",end="")
  rib=input()
  #print("ViewTR,{}".format(rib))
  client.sendall(bytes("ViewSold,{}".format(rib),'UTF-8'))  

def viewtr_c(client):
  clear()
  print("enter the rib account to view your transactions")
  rib=input()
 # print("ViewTR,{}".format(rib))
  client.sendall(bytes("ViewTR,{}".format(rib),'UTF-8'))  

def viewfa_c(client):
  clear()
  print("enter the rib account to view your factures")
  rib=input()
  client.sendall(bytes("ViewF,{}".format(rib),'UTF-8'))  

def transaction_c():
  clear()
  print("enter 1 for making a deposit")
  print("enter 2 for withdrowal")
  print("enter 3 to exit")
  rsp=input()
  while(int(rsp) not in [1,2,3]):
    print("enter a valid option(1, 2 or 3)!")
    rsp=input()
  msg=""
  if int(rsp)==1:
    print("enter your bank account reference")
    rib=input()
    print("enter your amount")
    amount=input()
    msg="Deposit,{},{}".format(rib,amount)
    client.sendall(bytes(msg,'UTF-8'))  

  if int(rsp)==2:
    print("enter your bank account reference")
    rib=input()
    print("enter your amount")
    amount=input()
    msg="Withdraw,{},{}".format(rib,amount)
    client.sendall(bytes(msg,'UTF-8'))  

  if int(rsp)==3:
    queryuser(client)
    
def queryuser(client):
  clear()
  response=0
  print("enter 1 for viewing ur sold")
  print("enter 2 for viewing ur transactions history")
  print("enter 3 for viewing ur factures")
  print("enter 4 for making a transaction")
  print("enter Desired Action:",end="")
  response=input()
  while int(response)not in [1,2,3,4]:
    print("please enter a valid action:")
    response=input()
  if(int(response) ==1):
    viewsold_c(client)
  if(int(response) ==2):
    viewtr_c(client)
  if(int(response) ==3):
    viewfa_c(client)
  if(int(response) ==4):
    transaction_c()
#def withdraw():
#  client.sendall(bytes(out_data,'UTF-8'))  
SERVER = "127.0.0.1"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER, PORT))
client.sendall(bytes("hello",'UTF-8'))
in_data =  client.recv(30720)
while True:

  queryuser(client)
  #if out_data=="":
   # while out_data=="":
     # print("Desired action cannot be null!\nenter Desired Action :",end="")
    #  queryuser()
      #out_data = input()
  
  #client.sendall(bytes(out_data,'UTF-8'))
  in_data =  client.recv(5072)
  if(in_data.decode()!="hello"):
    clear()
    print("From Server :" ,in_data.decode())
    input("Press Enter to continue...")
  #if out_data=='bye':
  #  break
  if(in_data.decode()=="bye"):

    break
client.close()