import pika
from pika.adapters.blocking_connection import ReturnedMessage

connection = pika.BlockingConnection(
  pika.ConnectionParameters(host='192.168.91.151'))
channel = connection.channel()
channel.exchange_declare(exchange='stream_queue', exchange_type='topic', durable=True)
result = channel.queue_declare(queue='stream_queue', durable=True, arguments={"message-ttl": 30000,"x-queue-type": "stream",\
                                                                            "x-max-length-bytes": 100000})
queue_name = result.method.queue
channel.queue_bind(exchange='stream_queue', queue='stream_queue', routing_key="ame.#")
channel.basic_qos(prefetch_count=6)
print(' [*] Waiting for logs. To exit press CTRL+C')
def callback(ch, method, properties, body):
  print(f" [x] {body.decode()}", properties)
  ch.basic_ack(method.delivery_tag)

try:
  channel.basic_consume(
    queue=queue_name, on_message_callback=callback, exclusive=True, auto_ack=False)  # auto_ack不支持stream队列，必须设置false
  channel.start_consuming()
except KeyboardInterrupt as e:
  channel.basic_cancel("id3")
  channel.close()
  print("通过已关闭，有缘再会啊！")