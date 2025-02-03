import paho.mqtt.client as paho
import sys
import rsa


try:
    with open("public.pem", "rb")as f:
       public_key = rsa.PublicKey.load_pkcs1(f.read())

except FileNotFoundError:
    print("Error: public.pem file not found.")
    exit(1)

try:
   with open("private.pem", "rb")as f:
       private_key = rsa.PrivateKey.load_pkcs1(f.read())

except FileNotFoundError:
    print("Error: private.pem file not found.")
    exit(1)

client = paho.Client()
if client.connect("localhost",1883,60) !=0:
   print("could not connect to mqtt broker")
   sys.exit(-1)

while True:
   try:
      with open(temperature_file,'r') as f:
           temp=int(f.read())/1000
  except FileNotFoundError:
    print("Error: temperature_file file not found.")
    exit(1)
  try:
     message_tmp=f"Temperature : {temp} C".encode("utf-8")
     temp_encrypted = rsa.encrypt(message_tmp, public_key)
     client.publish("test/topic",temp_encrypted,0)
  except Exception as e:
        print(f"An error occurred while encrypting or publishing: {e}")
        continue 
 try:
      with open(humidity_file,'r') as f:
           hum=int(f.read())/1000
 except FileNotFoundError:
    print("Error: humidity_file file not found.")
    exit(1)
 try:
     message_hum=f"Humidity : {hum} % ".encode("utf-8")
     hum_encrypted = rsa.encrypt(message_hum, public_key)
     client.publish("test/topic",hum_encrypted,0)
 except Exception as e:
        print(f"An error occurred while encrypting or publishing: {e}")
        continue  
 time.sleep(2)

client.disconnect() 