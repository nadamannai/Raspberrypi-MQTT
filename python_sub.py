import paho.mqtt.client as paho
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

# Connexion au broker MQTT
if client.connect("localhost", 1883, 60) != 0:
    print("Impossible de se connecter au broker MQTT")
    sys.exit(-1)


# Callback appelé lorsqu'une connexion au broker est établie
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connecté au broker MQTT")
        # S'abonner au topic "test/topic"
        client.subscribe("test/topic")
        print('Abonné au topic "test/topic"')
    else:
        print(f"Échec de la connexion au broker MQTT. Code : {rc}")

# Callback appelé lorsqu'un message est reçu
def on_message(client, userdata, msg):

    msg_byte=msg.payload
   
    try:
        decrypted_msg=rsa.decrypt(msg_byte,private_key)
        decr_str=decrypted_msg.decode('utf-8')
        print(f"decrpted msg:{decr_str}")
    except rsa.DecryptionError:
        print ("decryption failed")

# Configuration du client MQTT
client = paho.Client()

# Associer les callbacks
client.on_connect = on_connect
client.on_message = on_message


# Boucle principale pour attendre les messages
print("Attente des messages...")
client.loop_forever()