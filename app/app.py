from flask import Flask, request, jsonify
import pika

app = Flask(__name__)

def send_to_rabbitmq(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='message_queue', durable=True)
    channel.basic_publish(exchange='', routing_key='message_queue', body=message)
    connection.close()

@app.route('/send', methods=['POST'])
def send_message():
    data = request.json
    message = data.get('message')
    user = data.get('user')
    if message and user:
        send_to_rabbitmq(f"{user}:{message}")
        return jsonify({"status": "success"}), 200
    return jsonify({"status": "error", "message": "Invalid data"}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)