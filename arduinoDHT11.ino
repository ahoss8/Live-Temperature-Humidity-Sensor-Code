#include <DHT.h>
#define Type DHT11

int sensorPin = 9;
float temperature;
int humidity; 
int delaytime = 1000;

DHT HT(sensorPin, Type);

void setup() {
  Serial.begin(115200);
  HT.begin();
}


void loop() {
  temperature = HT.readTemperature();
  humidity = HT.readHumidity();
  Serial.print(temperature);
  Serial.print(", ");
  Serial.println(humidity);
  delay(delaytime);

  
}
