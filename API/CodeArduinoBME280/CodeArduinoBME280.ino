#include <Wire.h>
#include <LiquidCrystal_I2C.h>
#include <Adafruit_BME280.h>
#include <Adafruit_Sensor.h>
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>

const char *ssid = "Mathias";
const char *password = "Mathiasn";
const char *ApiEndPoint = "http://192.168.22.53:5000/Donnees";

Adafruit_BME280 bme;
LiquidCrystal_I2C lcd(0x27, 16, 2);

float temp = 0;
float pres = 0;
float hum = 0;


void ConnexionWifi() {
  Serial.print("Tentative de connexion au WiFi");

  int tentatives = 0;
  while (WiFi.status() != WL_CONNECTED && tentatives < 20) {
    delay(500);
    Serial.print(".");
    tentatives++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("WiFi connecté !");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("Échec de la connexion WiFi. Veuillez vérifier les paramètres.");
    // Vous pourriez ajouter ici une logique de récupération ou de redémarrage.
  }
}

void RSD() {
  if (!bme.begin()) {
    Serial.println("Impossible de trouver le capteur BME280 !");
    // Vous pourriez ajouter ici une logique de récupération ou de redémarrage.
    return;
  }

  temp = bme.readTemperature();
  pres = bme.readPressure() / 100.0F;
  hum = bme.readHumidity();
}

void PSD() {
  lcd.clear();
  lcd.setCursor(0, 0);
  lcd.print("Temperature: " + String(temp) + " °C");

  lcd.setCursor(0, 1);
  lcd.print("Pression: " + String(pres) + " hPa");

  lcd.setCursor(0, 2);
  lcd.print("Humidite: " + String(hum) + " %");
}

void SSD() {
  if (WiFi.status() != WL_CONNECTED) {
    Serial.println("Erreur de connexion WiFi");
    // Vous pourriez ajouter ici une logique de récupération ou de redémarrage.
    return;
  }

  HTTPClient http;

  String data = "&temp=" + String(temp) +
                "&pres=" + String(pres) +
                "&hum=" + String(hum);

http.begin(ApiEndPoint);
http.addHeader("Content-Type", "application/x-www-form-urlencoded");
  
  int httpCode = http.POST(data);

  if (httpCode > 0) {
    Serial.println("Données envoyées avec succès à l'API");
  } else {
    Serial.println("Erreur lors de l'envoi des données à l'API");
    // Vous pourriez ajouter ici une logique de récupération ou de redémarrage.
  }

  http.end();
}

void setup() {
  Serial.begin(115200);
  while(!Serial) {} // Wait
  Wire.begin(0,2);
  while(!bme.begin())
  {
    Serial.println("Could not find BME280 sensor!");
    delay(1000);
  }
  ConnexionWifi();
}

void loop() {
  RSD();
  PSD();
  SSD();

  delay(1000);
}