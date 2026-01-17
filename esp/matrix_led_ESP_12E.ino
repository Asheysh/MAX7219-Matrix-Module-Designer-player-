#include <MD_MAX72xx.h>
#include <SPI.h>

#define HARDWARE_TYPE MD_MAX72XX::FC16_HW
#define MAX_DEVICES 4

#define CLK_PIN D5
#define DATA_PIN D7
#define CS_PIN D4

MD_MAX72XX mx(HARDWARE_TYPE, DATA_PIN, CLK_PIN, CS_PIN, MAX_DEVICES);

void setup() {
  Serial.begin(115200);
  delay(2000);

  Serial.println("BOOT OK");
  mx.begin();
  mx.clear();

  Serial.println("PIXEL SERVER READY");
  Serial.println("Format: x y state");
}

void loop() {
  if (Serial.available()) {
    int x = Serial.parseInt();
    int y = Serial.parseInt();
    int s = Serial.parseInt();

    Serial.print("CMD: ");
    Serial.print(x); Serial.print(" ");
    Serial.print(y); Serial.print(" ");
    Serial.println(s);

    if (x >= 0 && x < 32 && y >= 0 && y < 8) {
      mx.setPoint(y, x, s);
    }

    while (Serial.available()) Serial.read();
  }
}
