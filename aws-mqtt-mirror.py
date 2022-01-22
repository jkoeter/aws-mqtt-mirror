"""
MIT License

Copyright (c) 2022 Jeroen Koeter

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

"""
AWS-MQTT-Mirror

This script, when adapted to contain the correct credentials, will print all MQTT messages posted to the topic '#'
to the console. It is used for debugging MQTT/message problems with AWS MQTT (IoT-Thing) connections.

It works with an AWS IAM account. For ease of debugging I give the account all rights but you might want to limit
the account if it is used with multiple tools/persons."""

import json
from time import sleep
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient

CLIENT_ID = "MQTT-mirror"
AWS_ENDPOINT = "XXXXX.iot.eu-west-1.amazonaws.com"
AWS_ENDPOINT_PORT = 443
AWS_ACCESS_KEY = "XXXXX"
AWS_ACCESS_SECRET = "XXXXX"
ROOT_CA_PATH = "certificates\\AmazonRootCA1.pem"


def mqtt_callback(_unused_client, _unused_userdata, message):
    mqtt_message = json.loads(message.payload)
    print('{} : {}'.format(int(message.timestamp), mqtt_message))


if __name__ == '__main__':
    print('AWS MQTT mirror')

    aws_iot_mqtt = AWSIoTMQTTClient(CLIENT_ID, useWebsocket=True)
    aws_iot_mqtt.configureEndpoint(AWS_ENDPOINT, AWS_ENDPOINT_PORT)
    aws_iot_mqtt.configureCredentials(ROOT_CA_PATH)
    aws_iot_mqtt.configureIAMCredentials(AWS_ACCESS_KEY, AWS_ACCESS_SECRET)
    result = aws_iot_mqtt.connect()

    result = aws_iot_mqtt.subscribe("#", 1, mqtt_callback)

    print("Press CTRL+C to abort")

    try:
        while True:
            sleep(60)
    except KeyboardInterrupt:
        print("Aborted by user")
    finally:
        aws_iot_mqtt.disconnect()
