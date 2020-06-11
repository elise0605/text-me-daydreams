from flask import Flask, request, redirect
import twilio.twiml
import pika, os, urlparse

app = Flask(__name__)

@app.route("/", methods=['GET', 'POST'])
def hello():

    from_number = request.values.get('From', None)
    body = request.values.get('Body', None)

    url_str = os.environ.get('CLOUDAMQP_URL','amqp://vzqzdfqo:9FGh3h...@crow.rmq.cloudamqp.com/vzqzdfqo')
    url = urlparse.urlparse(url_str)

    params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
        credentials=pika.PlainCredentials(url.username, url.password))

    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue='texts')

    message = from_number + ": " + body

    channel.basic_publish(exchange='', routing_key='texts', body=message)
    connection.close()

    resp = twilio.twiml.Response()
    resp.message("We're so happy! We got your message and it's currently printing. Tx, Elise T")
    return str(resp)

if __name__ == "__main__":
    app.run(debug=True)
