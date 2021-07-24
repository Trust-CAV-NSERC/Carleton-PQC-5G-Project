import json
import pika
import sys
import os
import uuid
def main():
    #connection = pika.BlockingConnection(pika.ConnectionParameters('172.21.30.104'))
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()

    channel.queue_declare(queue='testing')

    def callback(ch, method, properties, body):
        data = json.loads(str(body.decode()))
        #print(json.dumps(data))
        f = open("/opt/data/"+str(uuid.uuid4())+".json", "w")
        f.write(json.dumps(data))
        f.close()

    channel.basic_consume(queue='testing', on_message_callback=callback, auto_ack=True)

    print(' [*] Waiting for messages. To exit press CTRL+C')
    channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)