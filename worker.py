import pika
from classification import Classifier

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost'))

channel = connection.channel()

channel.queue_declare(queue='rpc_queue')


def classify(data):
    cls = Classifier()
    cls.prod_cat_classifier(data,1)
    return "Success"



def on_request(ch, method, props, body):
    n = body
    # print(" [.] fib(%s)" % n)
    response = classify(n)
    print(" [.] calculated (%s)" % response)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_qos(prefetch_count=1)
channel.basic_consume(queue='rpc_queue', on_message_callback=on_request)

print(" [x] Awaiting RPC requests")
channel.start_consuming()