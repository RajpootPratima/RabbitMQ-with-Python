import pika
import sys
credentials=pika.PlainCredentials("guest","guest")
connection = pika.BlockingConnection(pika.ConnectionParameters('localhost',5672,'/',credentials))
channel = connection.channel()

channel.queue_declare(queue="hello1", durable=True)

#Worker concept added
message = ' '.join(sys.argv[1:]) or "Hello World!"
channel.basic_publish(exchange='',
                      routing_key='hello1',
                      body=message,
                      properties=pika.BasicProperties(
                      delivery_mode = 2,# make message persistent
                      ))
print(" [x] Sent %r" % message)
# channel.basic_publish(exchange="",routing_key="hello",body="Hello World")

# print("sent hello world")

connection.close()