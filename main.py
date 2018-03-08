##### Title:  Simple Bitcoin Wallet
##### Author: David Kimolo
##### Date:   3/6/2018
##### Programmer at Bithub Africa
##### Email:  mwikyakimolo@gmail.com
##### Mobile: +254 705 123 289

# Libraries / Dependencies

from bitcoin import*
from blockcypher import get_address_overview
from blockchain import pushtx
from coinbase.wallet.client import Client
import nexmo
import smtplib
import json, csv
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

# Login Menu, a simple login menu before tht wallet meu loads.
# This login can be improved to add registration of a new member,
# save to file or database, Check if the username is incorrect,
# format of the password and encryption of the password

print("****LOGIN MENU****")
Username = input("Enter Your Username: ")
Password = ""
Attempt = 0
flag = 0
while (Attempt!=3):
    Password = input("Enter Password: ")
    if ( Password == "Password"):
        flag = 1
        break
    else:
        Attempt = Attempt + 1
    if (Attempt==3):
        print("You Have entered a wrong password mutiple times!")
if flag == 1:
    print("WELCOME BACK ", Username, "HERE IS YOUR MENU \n")
#Main Menu

    print ("Press 1 to generate a random private key")
    print ("Press 2 to generate a random Public key")
    print ("Press 3 to generate a random Wallet Address")
    print ("press 4 to create a multisig address")
    print ("Press 5 to Check Balance")
    print ("Press 6 Hash Address")
    print ("Press 7 to Send Bitcoins")
    print ("Press 8 to Push Transactions to Blockchain")
    print ("Press 9 Send Bitcoin Info to Email")
    print ("Press 10 to Send bitcoin Transtions to Email")
    print ("Press 11 Send Notification to phone Number")
    print ("Press  to Exit")
    print ("-----------------------------------------------")



#Generating a Random Private Key

answer = input()
PrivateVar = random_key()
if answer == "1":
    print (PrivateVar)
    print ("-----------------------------------------------")

#Generating a Random Public Key

PublicVar = privtopub(PrivateVar)
if answer == "2":
    print (PublicVar)


# Generating a Random Wallet Address

WalletAddress = pubtoaddr(PublicVar)
if answer == "3":
    print (WalletAddress)

#Generating a ,Multisig Wallet Address

if answer == "4":
    PrivateVar1 = privtopub(random_key())
    PrivateVar2 = privtopub(random_key())
    PrivateVar3 = privtopub(random_key())
    PrivateVar4 = privtopub(random_key())
    PrivateVar5 = privtopub(random_key())
    MultiSigAddressMaker = mk_multisig_script(PrivateVar2,PrivateVar1,PrivateVar3,PrivateVar4, PrivateVar5, 5,5)
    MultiSigAddress = scriptaddr (MultiSigAddressMaker)
    print(MultiSigAddress)
    SigAddress = str(MultiSigAddress)

#Checking Bitcoin Balance

if answer == "5":
    CheckBalance = input("Enter Your Bitcoin Address: ")
    print("Your Balance Details \n")
    print(get_address_overview(CheckBalance))

#Hashing Address

if answer == "6":
    print("Enter Your Bitcoin Address")
    WalletAddress = input()
    Hashed = txhash(WalletAddress)
    print(Hashed)

# Sending Bitcoins

if answer == "7":
    client = Client('Your API KEY', 'Your Secret Key')
    tx = client.send_money('2bbf394c-193b-5b2a-9155-3b4732659ede',
                           to='1AUJ8z5RuHRTqD1eikyfUUetzGmdWLGkpT',
                           amount='0.1',
                           currency='BTC',
                           idem='9316dd16-0c05')

# Pushing Transactions to Email

if answer == "8":
    HexTransaction = input("Insert your raw transaction: ")
    #example: 0100000001fd468e431cf5797b108e4d22724e1e055b3ecec59af4ef17b063afd36d3c5cf6010000008c4930460221009918eee8be186035be8ca573b7a4ef7bc672c59430785e5390cc375329a2099702210085b86387e3e15d68c847a1bdf786ed0fdbc87ab3b7c224f3c5490ac19ff4e756014104fe2cfcf0733e559cbf28d7b1489a673c0d7d6de8470d7ff3b272e7221afb051b777b5f879dd6a8908f459f950650319f0e83a5cf1d7c1dfadf6458f09a84ba80ffffffff01185d2033000000001976a9144be9a6a5f6fb75765145d9c54f1a4929e407d2ec88ac00000000
    pushtx.pushtx(HexTransaction)

#Sending  info to Email

if answer == "9":
    print("Please enter your Email Address: ")
    EmailAddres = input()
    subject = "Your Bitcoins Info"
    content = "Below Are you Bitcoin Details \n\n" + "Private Key "  + PrivateVar + "\n\n" + "Public Key: " + PublicVar + "\n\n" + "Wallet Address " + WalletAddress + "\n\n"
    mail = smtplib.SMTP("smtp.gmail.com", 587)
    mail.ehlo()
    mail.starttls()
    mail.login("africanbitcoins@gmail.com", "africanbitcoins2018")
    mail.sendmail("africanbitcoins@gmail.com", EmailAddres, content)
    print("Email send Succesfully ")
    mail.close()

#Sending Transactions to  Email

if answer == "10":
    print("Please enter your Email Address: ")
    EmailAddres = input()
    print("Enter Your Bitcoin Address")
    UserAddress = input()
    Transaction = history(UserAddress)
   #You can exclusively print this line to see the results on your Interpreter rather
   #than email
   # print(history(UserAddress))

    with open('Transactions.json', 'w') as outfile:
        json.dump(Transaction, outfile)
    infile = open('Transactions.json', 'r')
    outfile = open('Transactions.csv', 'w')
    writer = csv.writer(outfile)

    for row in json.loads(infile.read()):
        writer.writerow(row)
    with open("Transactions.json") as file:
        data = json.load(file)

    with open("Transactions.csv", "w") as file:
        csv_file = csv.writer(file)
        for item in data:
            csv_file.writerow([item['value'], item['output']])

    email_user = 'africanbitcoins@gmail.com'
    email_password = 'africanbitcoins2018'
    email_send = EmailAddres
    subject = 'YOUR BITCOIN TRANSACTIONS'
    msg = MIMEMultipart()
    msg['From'] = email_user
    msg['To'] = email_send
    msg['Subject'] = subject

    body = ' Hello, \n\n Here is your bitcoin transactions as you had requested. \n\n Bithub Africa \n www.bithub.africa\n +254 705 123 289'
    msg.attach(MIMEText(body,'plain'))
    filename='Transactions.csv'
    attachment  =open(filename,'rb')
    part = MIMEBase('application','octet-stream')
    part.set_payload((attachment).read())
    encoders.encode_base64(part)
    part.add_header('Content-Disposition',"attachment; filename= "+filename)

    msg.attach(part)
    text = msg.as_string()
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.starttls()
    server.login(email_user,email_password)
    server.sendmail(email_user,email_send,text)
    server.quit()

# Sending Notification to Phone Number

if answer == "11":
    print("Please enter phone number e.g +2547XXXXXXXXX: ")
    PhoneNumber = input()
    client = nexmo.Client(key="416abae4",secret="a889301e47be6540")
    client.send_message ({
        'from': 'BitHub Africa',
        'to': PhoneNumber,
        'text': 'Thank you for resgistering with BitHub Africa . '
                '\n Your Bitcoin Address: ' + WalletAddress + '\n' +
                'Your Privatekey: ' + PrivateVar,
        'err-code': "0"
    })

#Incase of any questions or suggestions feel free to contact me