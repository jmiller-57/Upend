
const unsigned long interval = 10;
unsigned long lastSample = 0;

void setup() {
  Serial.begin(115200);
}

void loop() {
  unsigned long now = millis();
  unsigned long diff = now - lastSample;

  if (diff >= interval) {
    lastSample = now;
    Serial.println(sin(5 * 2 * PI * (now / 1000.0)), 4);
  }
}
