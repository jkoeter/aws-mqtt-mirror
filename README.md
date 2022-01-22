# AWS MQTT Mirror

This script, when adapted to contain the correct credentials, will print all MQTT messages posted to the topic '#'
to the console. It is used for debugging MQTT/message problems with AWS MQTT (IoT-Thing) connections.

It works with an AWS IAM account. For ease of debugging I give the account all rights but you might want to limit
the account if it is used with multiple tools/persons.