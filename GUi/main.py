import socket
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.textinput import TextInput
from kivy.uix.label import Label

# Create both screens. Please note the root.manager.current: this is how
# you can control the ScreenManager from kv. Each screen has by default a
# property manager that gives you the instance of the ScreenManager used.
Builder.load_string(
"""
<inputHnadler>
    id:IM
    name:inputmanager


<ScreenManagement>:

    MenuScreen:
        id: name
        name: 'menu'
        
    SettingsScreen:
        id: settings
        name: 'settings'
    TransactionsScreen:
        id:transactions
        name:'transactions'
    MonitoringScreen:
        id:monitoring
        name:'monitoring'
    InfoScreen
        id:info
        name:'info'



<MonitoringScreen>:
    canvas.before:
   
        Rectangle:
    
            pos: self.pos
            size: self.size
            source: 'cartoon.jpg' 
    FloatLayout:
        
        post:0,0
        size: root.width,root.height
        TextInput:
            id: rib
            multiline:False
            pos_hint: {'center_x': 0.7, 'center_y': 0.705}
            size_hint: 0.2, 0.05
            hint_text:'Rib'
        Button:
            id:balancebutton
            size_hint:.2,.1
            text:'Check Balance'
            pos_hint:{'x':0.1,'y':0.6}
            on_release:  
                root.manager.ids.info.showbalance(rib.text)
                root.manager.current='info'
                
        Button:
            id:transactionsbutton
            size_hint:.2,.1
            text:'View Transactions'
            pos_hint:{'x':0.1,'y':0.4}
            on_release:  
                root.manager.ids.info.showTransactions(rib.text)
               
                
        Button:
            id:debtsbutton
            pos_hint:{'x':0.1,'y':0.2}
            size_hint:.2,.1
            text:'View Bank Debts'
            on_release:   
                root.manager.ids.info.showfacture(rib.text)


        Button:
            pos_hint:{'x':0.8,'y':0.9}
            size_hint:.1,.05
            text:'Home'
            on_release:  
                root.manager.current = 'menu'


<InfoScreen>:
    canvas.before:
        Rectangle:
    
            pos: self.pos
            size: self.size
            source: 'télécharger.png' 
    FloatLayout:
  
        post:0,0
        size: root.width,root.height
        TextInput:
            id: transactions
            pos_hint: {'center_x': 0.5, 'center_y': 0.55}
            size_hint: 0.5, 0.7
            hint_text:'transactions'
        Button:
            pos_hint:{'x':0.8,'y':0.9}
            size_hint:.1,.05
            text:'Home'
            on_release:  
                root.manager.current = 'menu'




<TransactionsScreen>:
    canvas.before:
   
        Rectangle:
    
            pos: self.pos
            size: self.size
            source: 'mymoney.png' 
    FloatLayout:
  
        post:0,0
        size: root.width,root.height
        Button:
            size_hint:.2,.1
            text:'Withdraw'
            pos_hint:{'x':0.08,'y':0.8}
            on_release:  
                root.manager.ids.transactions.withdraw(trrib.text,tramount.text)
        Button:
            size_hint:.2,.1
            text:'Deposit'
            pos_hint:{'x':0.3,'y':0.8}
            on_release: 
                root.manager.ids.transactions.deposit(trrib.text,tramount.text) 
        Button:
            pos_hint:{'x':0.8,'y':0.9}
            size_hint:.1,.05
            text:'Home'
            on_release:  
                root.manager.current = 'menu'
                #TextInput(text='Hello world', multiline=False)
        TextInput:
            id: trrib
            multiline:False
            pos_hint: {'center_x': 0.5, 'center_y': 0.6}
            size_hint: 0.2, 0.05
            hint_text:'rib'
        TextInput:
            id: tramount
            multiline:False
            pos_hint: {'center_x': 0.5, 'center_y': 0.5}
            size_hint: 0.2, 0.05
            hint_text:'amount'
        TextInput:
            id: result
            pos_hint: {'center_x': 0.5, 'center_y': 0.2}
            size_hint: 0.002, 0.005
            hint_text:'amount'
            
        
        
   




<MenuScreen>:
    
    canvas.before:
     
        Rectangle:
            pos: self.pos
            size: self.size
            source: 'banker.png' 
    FloatLayout:
    
        post:0,0
        size: root.width,root.height
        TextInput:
            id: serverid
            multiline:False
            pos_hint: {'center_x': 0.2, 'center_y': 0.9}
            size_hint: 0.2, 0.05
            hint_text:'Server ip'
            
        Button:
            id:connexionbutton
            background_color: 1,0,0,1
            text:'Con'
            size_hint:.04,.02
            pos_hint: {'center_x': 0.05, 'center_y': 0.9}
            on_release:
                root.myconnect(serverid.text)

                

                    
        Button:
            background_color: 0.27, 0.89, 0.43,1
            size_hint:.2,.1
            text:'View Transactions'
            pos_hint:{'x':0.094,'y':0.5}
            text: 'Monitor Account'
            on_release: 
                root.manager.current = 'monitoring'

                
        Button:
            background_color: 0.27, 0.89, 0.43,1
            size_hint:.2,.1
            text:'View Transactions'
            pos_hint:{'x':0.705,'y':0.5}
            text: 'Make Transactions'
            on_release: 
                root.manager.current = 'transactions'

<SettingsScreen>:
    BoxLayout:
        Button:
            text: 'My settings button'
        Button:
            text: 'Back to menu'
            on_press: root.manager.current = 'menu'
""")

SERVER = "192.168.1.11"
PORT = 8080
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# Declare both screens
class MenuScreen(Screen):
    def myconnect(self,ip):
        print(ip)
        
        rsp=""
        try:
            client.connect((ip, PORT))
            client.sendall(bytes("hello",'UTF-8'))
            data = client.recv(3072) 
            rsp=data.decode()         
        except socket.error as e:
            print("socket disconnected")
        if(rsp=="hello"):
            data = client.recv(3072) 
            print("i'm all the way up")
            self.ids.connexionbutton.background_color = (0,1,0,1)
            return True
        else:
            print("failed")
            return False
class MonitoringScreen(Screen):
    def myfunction(self,instance):
        print(f"func_abc: Called from Button with text={instance.text}")


    pass
class TransactionsScreen(Screen):
    def updateResult(self,msg):
        self.ids.result.text= msg
        self.ids.result.size_hint = (0.1,0.1)
    def withdraw(self,trib,tvalue):
        client.sendall(bytes("Withdraw,{},{}".format(trib,tvalue),'UTF-8'))
        data =client.recv(3072)
        rsp=data.decode()
        self.updateResult(rsp)
        pass
    def deposit(self,trib,tvalue):
        client.sendall(bytes("Deposit,{},{}".format(trib,tvalue),'UTF-8'))
        data =client.recv(3072)
        rsp=data.decode()
        self.updateResult(rsp)
        pass
    pass

class InfoScreen(Screen):
    def updatetransaction(self,msg):
        self.ids.transactions.text= msg
        print(msg)
        self.manager.current = 'info'
    def showTransactions(self,ref):
        client.sendall(bytes("ViewTR,{}".format(ref),'UTF-8'))
        data =client.recv(3072)
        rsp=data.decode()
        self.updatetransaction(rsp)
    def showbalance(self,ref):
        client.sendall(bytes("ViewSold,{}".format(ref),'UTF-8'))
        data =client.recv(3072)
        rsp=data.decode()
        self.updatetransaction(rsp)
    def showfacture(self,ref):
        client.sendall(bytes("ViewF,{}".format(ref),'UTF-8'))
        data =client.recv(3072)
        rsp=data.decode()
        self.updatetransaction(rsp)


        pass
class SettingsScreen(Screen):
    

    def func_abc(self, instance):
        print(f"func_abc: Called from Button with text={instance.text}")

    def func_xyz(self, instance):
        print(f"func_xyz: Called from Button with text={instance.text}")
    def ack(self, instance):
        print(f"func_abc: Called from Button with text={instance.text}")
    def showtext(self,text):
        print(text)


        
        client.close()

    def showfacture(self,ref):
          
        print("facture of",ref," is:")

# Create the screen manager
class ScreenManagement(ScreenManager):
    pass


class TheLazyBankerApp(App):

    def build(self):
        return ScreenManagement()
class ribinput(TextInput):
    text="gemme sum tarara:"
if __name__ == '__main__':
    TheLazyBankerApp().run()