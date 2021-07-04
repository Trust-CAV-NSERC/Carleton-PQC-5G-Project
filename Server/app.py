from flask import Flask, request
from flask_jwt import JWT, jwt_required, current_identity
from werkzeug.security import safe_str_cmp
import oqs
import base64
import datetime
import json
from Crypto.Cipher import AES
import hashlib
sigalg = "Dilithium5"
kemalg = "Saber-KEM"

class User(object):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password

    def __str__(self):
        return "User(id='%s')" % self.id

users = [
    User(1, 'user1', 'user1')
]

username_table = {u.username: u for u in users}
userid_table = {u.id: u for u in users}

def generateKEMKey():
    with oqs.KeyEncapsulation(kemalg) as signer:
        signer_public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
    return base64.b64encode(signer_public_key),base64.b64encode(secret_key)

def generateSignerKey():
    with oqs.Signature(sigalg) as signer:
        signer_public_key = signer.generate_keypair()
        secret_key = signer.export_secret_key()
    return base64.b64encode(signer_public_key),base64.b64encode(secret_key)

def authenticate(username, password):
    user = username_table.get(username, None)
    if user and safe_str_cmp(user.password.encode('utf-8'), password.encode('utf-8')):
        return user

def identity(payload):
    user_id = payload['identity']
    return userid_table.get(user_id, None)

app = Flask(__name__)
app.debug = False
app.config['SECRET_KEY'] = 'super-secret'
jwt = JWT(app, authenticate, identity)
signer_keys = generateSignerKey()
kem_keys = generateKEMKey()

@app.route('/server-signer-pubkey')
@jwt_required()
def returnSingerPubKey():
    pubKey_b64 = signer_keys[0]
    return {"key":str(pubKey_b64,'utf-8')}

@app.route('/cipher_text',methods=['POST'])
@jwt_required()
def cipher_text():
    message = {"time":str(datetime.datetime.timestamp(datetime.datetime.utcnow()))}
    pubkeyJSON = request.json
    pubkey = base64.b64decode(pubkeyJSON["pubkey"])
    #print (pubkey)
    server = oqs.KeyEncapsulation(kemalg, base64.b64decode(kem_keys[1]))
    #secret_key = server.export_secret_key()
    ciphertext, shared_secret_server = server.encap_secret(pubkey)
    #print (str(base64.b64decode(ciphertext),'utf-8'))
    #return "yay"
    obj = AES.new(shared_secret_server, AES.MODE_ECB)
    message = base64.b64encode((json.dumps(message)).encode())
    length = 16 - (len(message) % 16)
    message += bytes([length])*length
    encrypted_message = obj.encrypt(message)
    return {"key": str(base64.b64encode(ciphertext),'utf-8'),"encrypted_message":str(base64.b64encode(encrypted_message),"utf-8")}

@app.route('/cleartexttestmessage')
@jwt_required()
def generateCleartextTestMessage():
    message = {"time":str(datetime.datetime.timestamp(datetime.datetime.utcnow()))}
    message = base64.b64encode((json.dumps(message)).encode())
    #message = "This is the message to sign"
    with oqs.Signature(sigalg) as signer:
        signer = oqs.Signature(sigalg, base64.b64decode(signer_keys[1]))
        signature = signer.sign(message)
    return {"signed_message":str(base64.b64encode(signature),'utf-8'),"message":str(message,'utf-8')}

@app.route('/protected')
@jwt_required()
def protected():
    return {"msg":"Valid JWT!"}

@app.route('/status')
def status():
    return {"status":"ok"}

if __name__ == '__main__':
    app.run(host="0.0.0.0")