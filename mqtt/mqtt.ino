#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#define SS_PIN D4  //D2
#define RST_PIN D3 //D1
#define RELAY D8


const char* ssid = "zzz";                   // wifi ssid
const char* password =  "kentanggoreng";         // wifi password
const char* mqttServer = "m15.cloudmqtt.com";    // IP address mqtt sever 
//const char* mqttServer = "54.227.205.125";    // IP adress Raspberry Pi
const int mqttPort = 16657;
const char* mqttUser = "istjtbsk";      // if you don't have MQTT Username, no need input
const char* mqttPassword = "XKgGIiGO7mVr";  // if you don't have MQTT Password, no need input

WiFiClient espClient;
PubSubClient client(espClient);

void setup() {

  Serial.begin(115200);
  
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.println("Connecting to WiFi..");
  }
  Serial.println("Connected to the WiFi network");

  client.setServer(mqttServer, mqttPort);
  client.setCallback(callback);

  while (!client.connected()) {
    Serial.println("Connecting to MQTT...");

    if (client.connect("ESP8266Client", mqttUser, mqttPassword )) {

      Serial.println("connected");

    } else {

      Serial.print("failed with state ");
      Serial.print(client.state());
      delay(2000);

    }
  }

//  client.publish("esp8266", "Hello Raspberry Pi");
//  client.subscribe("esp8266");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {

  Serial.print("Message arrived in topic: ");
  Serial.println(topic);

  Serial.print("Message:");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  if(payload[0] == '1'){
    Serial.println("mantap");
    digitalWrite(led,HIGH);
    client.publish("esp8266", "LED ON");

  }

  //turn the light off if the payload is '0' and publish to the MQTT server a confirmation message
  else if (payload[0] == '0'){
    digitalWrite(led,LOW);
    client.publish("esp8266", "LED OFF");
  }
  Serial.println();
  Serial.println("-----------------------");

}

void loop() {
    client.subscribe("esp8266");
    delay(1000);
    client.loop();
}
