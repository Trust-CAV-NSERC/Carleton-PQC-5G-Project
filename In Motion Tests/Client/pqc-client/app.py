import base64
import requests
import json
import oqs
import sys
import os
import datetime
import pika
import time
import gpsd
from Crypto.Cipher import AES
from pprint import pprint
import uuid
SIG_ALG_NUM = os.environ["SIG_ALG_NUM"]
SIG_ALG_NUM = int(SIG_ALG_NUM)
sigalg = ['Dilithium2', 'Dilithium3', 'Dilithium5','Rainbow-I-Classic', 'Rainbow-III-Classic','Rainbow-V-Classic']
print (len(sigalg))
# 0 .. 5
sigalg = sigalg[SIG_ALG_NUM]
gpsd.connect(host="172.22.0.4", port=2947)
connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
#connection = pika.BlockingConnection(pika.ConnectionParameters("172.21.30.104"))
channel = connection.channel()
channel.queue_declare(queue='testing')
SERVER_PORT = os.environ["SERVER_PORT"]


list_of_servers = [
    #{"server":"172.21.30.104","port":SERVER_PORT,"name":"Georges Home (VPN)"}
    {"server":"172.21.30.10","port":SERVER_PORT,"name":"Georges Home"},
    {"server":"10.213.75.36","port":SERVER_PORT,"name":"Toronto Edge"},
    {"server":"10.213.59.36","port":SERVER_PORT,"name":"Ottawa Edge"},
    #{"server":"209.104.103.66","port":"25115","name":"ott-1-edge-wan"}
    ]
#sigs = oqs.get_enabled_sig_mechanisms()
#print("Enabled signature mechanisms:")
#pprint(sigs, compact="True")

def generateSignerKey(sigalg):
    with oqs.Signature(sigalg) as signer:
        print (signer.details)
        signer_public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
    return base64.b64encode(signer_public_key),base64.b64encode(secret_key)

def getPubKey(server,port):
    URL = "http://"+server+":"+port+"/server-signer-pubkey"
    protected = requests.get(URL)
    return protected.text

def getTestClearTextMessage(server,port):
    URL = "http://"+server+":"+port+"/cleartexttestmessage"
    protected = requests.get(URL)
    return protected.text

def verifyMessage(message,signature,pubkey):
    now = datetime.datetime.utcnow()
    pubkeyB64_bytes = bytes(pubkey,'utf-8')
    pubkeyB64 = base64.b64decode(pubkeyB64_bytes)
    sigBytes = bytes(signature,'utf-8')
    sigB64 = base64.b64decode(sigBytes)
    with oqs.Signature(sigalg) as verifier:
        # verifier verifies the signature
        message = message.encode()
        is_valid = verifier.verify(message, sigB64, pubkeyB64)
        msg = json.loads(base64.b64decode(message.decode()))
        msg_time = datetime.datetime.utcfromtimestamp(float(msg["time"]))
        diff = now - msg_time
        #print("Valid signature?", is_valid)
        #print("The message is ", msg)
        #print("Now ",str(now))
        #print("Msg time",str(msg_time))
        #print (diff.microseconds/1000)

        return is_valid,diff.microseconds/1000

def testClearTextMessage(server,port):
    pubkey = json.loads(getPubKey(server,port))["key"]
    testMessage = json.loads(getTestClearTextMessage(server,port))
    signed_message = testMessage["signed_message"]
    message = testMessage["message"]
    return verifyMessage(message,signed_message,pubkey)

def testServerReachability(server,port):
    URL = "http://"+server+":"+port+"/status"
    try:
        status = requests.get(URL)
        status = json.loads(status.text)
        if status["status"] == "ok":
            return True
        else:
            return False
    except:
        return False

def avg(lst):
    return sum(lst) / len(lst)
signer_keys = generateSignerKey(sigalg)

results = {}
#sys.exit(1)
for server in list_of_servers:
    print ("testing "+str(server))
    status = testServerReachability(server["server"],server["port"])
    if status:
        print ("valid server")
    else:
        print ("invalid server")
        sys.exit(1)
def testServer():
    for server in list_of_servers:
        results={}
        #print ("running PQC Tests against "+str(server))
        srv = server["server"]
        port = server["port"]
        diff_ct_ary = []
        valid, diff_clear = testClearTextMessage(srv,port)
        if valid:
            diff_ct_ary.append(diff_clear)
        packet = gpsd.get_current()
        if packet.mode >=2:
            results = {
                "delay":str(round(avg(diff_ct_ary),3)),
                "server":server,
                "timestamp":str(datetime.datetime.utcnow()),
                "sigalg":sigalg,
                "gps":
                    {
                        "mode":str(packet.mode),
                        "sat":str(packet.sats),
                        "lat":str(packet.lat),
                        "lon":str(packet.lon),
                        "speed":str(packet.hspeed)
                    }
                }
        else:
            results = {
                "delay":str(round(avg(diff_ct_ary),3)),
                "server":server,
                "timestamp":str(datetime.datetime.utcnow()),
                "sigalg":sigalg,
                "gps":"NOT AVAILABLE"
                }
        #print (json.dumps(results))
        putMessage(results)
    #testAsymTextMessage()
def putMessage(msg):
    channel.basic_publish(exchange='',routing_key='testing',body=str(json.dumps(msg)))
    return True
while True:
    testServer()
    time.sleep(0.1)

