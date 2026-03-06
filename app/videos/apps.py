import pika
from django.apps import AppConfig
import threading

class VideosConfig(AppConfig):
    name = 'videos'

    def ready(self):
        # Define a function to run the RabbitMQ consumer
        def start_consumer():
            from videos.consumers import process_video

            try:
                # Establish connection to RabbitMQ
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(
                        host='rabbitmq',
                        credentials=pika.PlainCredentials('admin', 'admin'), # TODO - add to main.py and .env
                    )
                )
                channel = connection.channel()

                # Start consuming messages from the queue
                channel.basic_consume(queue='video_to_process', on_message_callback=process_video, auto_ack=True)

                print('Waiting for messages. To exit press CTRL+C')
                channel.start_consuming()
            except Exception as e:
                print(f"Error connecting to RabbitMQ: {e}")

        # Run the consumer in a separate thread
        consumer_thread = threading.Thread(target=start_consumer, daemon=True)
        consumer_thread.start()
