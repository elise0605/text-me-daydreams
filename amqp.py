import pika, os, urlparse, sys
from Adafruit_Thermal import *

printer = Adafruit_Thermal("/dev/ttyAMA0", 19200, timeout=5)

url_str = os.environ.get('CLOUDAMQP_URL','amqp://YOUR_CLOUDAMQP_URL')
url = urlparse.urlparse(url_str)
params = pika.ConnectionParameters(host=url.hostname, virtual_host=url.path[1:],
    credentials=pika.PlainCredentials(url.username, url.password))

connection = pika.BlockingConnection(params)
channel = connection.channel() 
channel.queue_declare(queue='texts') 

def callback(ch, method, properties, body):

    printer.inverseOn()
    printer.println(' ' + '{:<31}'.format("TXT MESSAGE"))
    printer.inverseOff()

    printer.println(body)
    printer.feed(3)

    print("complete")
    print " [x] Received %r" % (body)

channel.basic_consume(callback,
    queue='texts',
    no_ack=True)

try:

    channel.start_consuming()

except KeyboardInterrupt:

    print "Break detected"
    channel.stop_consuming()

connection.close()

sys.exit()