from fastapi import FastAPI
import pika
import json

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Product Service Running"}

@app.post("/create_product/")
def create_product(name: str):
    message = {"name": name}
    
    # RabbitMQ'ya mesaj gönder
    connection = pika.BlockingConnection(pika.ConnectionParameters('rabbitmq'))
    channel = connection.channel()
    channel.queue_declare(queue='product_queue')
    channel.basic_publish(exchange='', routing_key='product_queue', body=json.dumps(message))
    connection.close()

    return {"message": f"Product '{name}' created and sent to Order Service"}
