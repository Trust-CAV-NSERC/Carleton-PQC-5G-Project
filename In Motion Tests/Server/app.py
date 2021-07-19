from flask import Flask, request
from werkzeug.security import safe_str_cmp
import oqs
import base64
import datetime
import json
from Crypto.Cipher import AES
import hashlib
import os
SIG_ALG_NUM = os.environ["SIG_ALG_NUM"]
SIG_ALG_NUM = int(SIG_ALG_NUM)
sigalg = ['Dilithium2', 'Dilithium3', 'Dilithium5','Rainbow-I-Classic', 'Rainbow-III-Classic','Rainbow-V-Classic']

print (len(sigalg))
# 0 .. 5
sigalg = sigalg[SIG_ALG_NUM]





def generateSignerKey(sigalg):
    with oqs.Signature(sigalg) as signer:
        signer_public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
    return base64.b64encode(signer_public_key),base64.b64encode(secret_key)

app = Flask(__name__)
app.debug = False
signer_keys = generateSignerKey(sigalg)

@app.route('/server-signer-pubkey')
def returnSingerPubKey():
    pubKey_b64 = signer_keys[0]
    return {"key":str(pubKey_b64,'utf-8')}

@app.route('/cleartexttestmessage')
def generateCleartextTestMessage():
    message = {"time":str(datetime.datetime.timestamp(datetime.datetime.utcnow()))}
    message = base64.b64encode((json.dumps(message)).encode())
    #message = "This is the message to sign"
    with oqs.Signature(sigalg) as signer:
        signer = oqs.Signature(sigalg, base64.b64decode(signer_keys[1]))
        signature = signer.sign(message)
    return {"signed_message":str(base64.b64encode(signature),'utf-8'),"message":str(message,'utf-8')}


@app.route('/status')
def status():
    return {"status":"ok","sigalg":str(sigalg)}

if __name__ == '__main__':
    app.run(host="0.0.0.0")