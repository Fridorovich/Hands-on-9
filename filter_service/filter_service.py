import pika

STOP_WORDS = ["bird-watching,", "ailurophobia", "mango"]

def filter_message(ch, method, properties, body):
    user, message = body.decode().split(':', 1)
    if any(word in message for word in STOP_WORDS):
        print(f"Filtered message from {user}: {message}")
    else:
        ch.basic_publish(exchange='', routing_key='screaming_queue', body=f"{user}:{message}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='message_queue', durable=True)
    channel.queue_declare(queue='screaming_queue', durable=True)
    channel.basic_consume(queue='message_queue', on_message_callback=filter_message)
    channel.start_consuming()

if __name__ == '__main__':
    main()