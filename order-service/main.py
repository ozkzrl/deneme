from fastapi import FastAPI
import pika
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Order Service Running"}

# RabbitMQ'dan mesaj al
def consume_order():
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='product_queue')

    def callback(ch, method, properties, body):
        data = json.loads(body)
        print(f"Received Order: {data}")

    channel.basic_consume(queue='product_queue', on_message_callback=callback, auto_ack=True)
    channel.start_consuming()

if __name__ == "__main__":
    consume_order()
