// #ifndef SYSTEM_EVENT_CUSTOM
//   #define SYSTEM_EVENT_CUSTOM 1
//   #define SYSTEM_EVENT_STA_CONNECTED 4
//   #define SYSTEM_EVENT_STA_GOT_IP 7
//   #define SYSTEM_EVENT_STA_DISCONNECTED 5
// #endif
#include <IoTaaP_OS.h>
// #include "../../iot-os/src/IoTaaP_OS.h"

IoTaaP_OS iotaapOs("1.0.2");
char sharedBuffer1[100];
char sharedBuffer2[50];

void callback(char *topic, byte *message, unsigned int length)
{
  Serial.println("---------------------------");
  Serial.println("Received data on topic:");
  Serial.println(topic); // Print topic

  Serial.println("Data:");

  for (int i = 0; i < length; i++) // Print message
  {
    Serial.print((char)message[i]);
  }
  Serial.println();
  Serial.println("---------------------------");
}

void setup()
{
  char deviceId[30];     // Char array used to store system parameter

  iotaapOs.start(); // Start IoTaaP OS

  iotaapOs.startWifi(); // Connect to WiFi
  iotaapOs.startMqtt(callback); // Connect to MQTT broker

  iotaapOs.writeToSystemLogs("Device started"); // Write data to system log using 'USER' tag

  iotaapOs.getSystemParameter("device_id", deviceId); // Get 'device_id' parameter from 'default.cfg'
  Serial.println("device_id parameter:");
  Serial.println(deviceId);

  iotaapOs.basicSubscribe("device_commands"); // Subscribe to /<username>/dummy_topic

  // iotaapOs.basicSubscribe("receiving_topic"); // Subscribe to /<username>/receiving_topic
  // Every message received on this topic will trigger callback

  // iotaapOs.basicUnsubscribe("dummy_topic"); // Unsubscribe from /<username>/dummy_topic

  iotaapOs.checkForUpdates(); // Manually check for updates at startup

  delay(1000);
}

void loop()
{
  // iotaapOs.deviceCloudPublishParam("temp", random(0, 500) / 10.0); // Publish parameter (to topic: /<username>/devices/<device-id>/params)
  // iotaapOs.deviceCloudPublishParam("humi", random(0, 1000) / 10.0); // Publish parameter (to topic: /<username>/devices/<device-id>/params)
  // iotaapOs.deviceCloudPublishParam("pres", random(0, 15000) / 10.0); // Publish parameter (to topic: /<username>/devices/<device-id>/params)
  // Serial.println("device running...");
  char deviceId[30];     // Char array used to store system parameter
  iotaapOs.getSystemParameter("device_id", deviceId); // Get 'device_id' parameter from 'default.cfg'
  sprintf(sharedBuffer1, "{\"deviceId\":\"%s\",\"time\":%llu}", deviceId, iotaapOs.getSystemTimeEpoch());
  // sprintf(sharedBuffer1, "{\"deviceId\":\"%s\"}", deviceId);
  iotaapOs.deviceCloudPublish(sharedBuffer1, "sync");  // Publish simple (escaped) JSON to: /<username>/devices/<device-id>/hello_topic
  iotaapOs.basicCloudPublish(sharedBuffer1, "sync");  // Publish simple (escaped) JSON to: /<username>/simple_topic
  Serial.println("basicCloudPublish-1");
  Serial.println(sharedBuffer1);
  delay(60000);
}