import pika

def scream_message(ch, method, properties, body):
    user, message = body.decode().split(':', 1)
    upper_message = message.upper()
    ch.basic_publish(exchange='', routing_key='publish_queue', body=f"{user}:{upper_message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='screaming_queue', durable=True)
    channel.queue_declare(queue='publish_queue', durable=True)
    channel.basic_consume(queue='screaming_queue', on_message_callback=scream_message)
    channel.start_consuming()

if __name__ == '__main__':
    main()