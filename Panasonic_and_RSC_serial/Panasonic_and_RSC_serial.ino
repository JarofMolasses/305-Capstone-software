/*
 * Print the pressure and particle data to Serial stream for analysis.
  circuit:
  pin name     pin number on Arduino
    DRDY         6
    CS_EE        7
    CS_ADC       8
    MOSI (DIN)   11
    MISO (DOUT)  12
    SCK          13
*/

#include "LiquidCrystal_I2C.h"
#include "Honeywell_RSC.h"
#include <Wire.h>
#include "SparkFun_Particle_Sensor_SN-GCJA5_Arduino_Library.h" //Click here to get the library: http://librarymanager/All#SparkFun_Particle_SN-GCJA5
#include "Adafruit_PM25AQI.h"         //hidden library requirement: "Adafruit_BusIO" for some unused I2C stuff
#include <SoftwareSerial.h>
SoftwareSerial pmSerial(2,3);

Adafruit_PM25AQI aqi = Adafruit_PM25AQI();
SFE_PARTICLE_SENSOR myAirSensor;
LiquidCrystal_I2C lcd0(0x27, 16, 2);

// pins used for the connection with the sensor
// the other you need are controlled by the SPI library):
#define DRDY_PIN      6
#define CS_EE_PIN     7
#define CS_ADC_PIN    8
#define ANALOG_INPUT A0
#define DELAY_PERIOD 1000
#define PRESENT 1
#define ABSENT 0

// create Honeywell_RSC instance
Honeywell_RSC rsc(
  DRDY_PIN,   // data ready
  CS_EE_PIN,  // chip select EEPROM (active-low)
  CS_ADC_PIN  // chip select ADC (active-low)
);

volatile double CalibrationValue=0;
unsigned long time=0;
int panastatus = ABSENT;       //panasonic sensor status
int adastatus = ABSENT;       //adafruit sensor status. needs to be set manually in this implementation

void setup() {
  // open serial communication
  Serial.begin(115200);
  // open SPI communication
  SPI.begin();
  // open I2C communication
  Wire.begin();
  // open bitbanged UART 
  pmSerial.begin(9600);
  
  lcd0.begin();
  // allowtime to setup
  delay(1000);

  // initialise pressure sensor
  rsc.init();

  // print sensor information
  Serial.println();
  Serial.print("catalog listing:\t");
  Serial.println(rsc.catalog_listing());
  Serial.print("serial number:\t\t");
  Serial.println(rsc.serial_number());
  Serial.print("pressure range:\t\t");
  Serial.println(rsc.pressure_range());
  Serial.print("pressure minimum:\t");
  Serial.println(rsc.pressure_minimum());
  Serial.print("pressure unit:\t\t");
  Serial.println(rsc.pressure_unit_name());
  Serial.print("pressure type:\t\t");
  Serial.println(rsc.pressure_type_name());

  // measure temperature
  Serial.print("temperature: ");
  Serial.println(rsc.get_temperature());
  delay(5);

  pinMode(ANALOG_INPUT, INPUT);
  CalibrationValue = rsc.get_pressure()*1000;
  
  if (myAirSensor.begin() == false){        //init panasonic sensor
    Serial.println("Panasonic GCJA5 did not respond.");
  } else{
    panastatus = PRESENT;
    Serial.println("GCJA5 Sensor present");
  }

  if (aqi.begin_UART(&pmSerial) == false){
    //presently, the aqi.begin_UART function only returns true, see docs https://github.com/adafruit/Adafruit_PM25AQI/blob/master/Adafruit_PM25AQI.cpp
  }
  if(adastatus == PRESENT){
    Serial.println("ADAFRUIT sensor present");
  }

  Serial.println("Time (s), Pressure, GCJA5 ug/m3: PM1.0, PM2.5, PM10, ADAFRUIT ug/m3: PM1.0, PM2.5, PM10");
  Serial.println("End of Header");    //check for this in the python app
}

int sec = 0;
void loop() {
  Serial.print(sec);
  Serial.print(",");

  double pressure = (rsc.get_pressure()*1000-CalibrationValue)/1.1;
  Serial.print(pressure);
  //Serial.print(rsc.get_pressure());
  Serial.print(",");
  lcd0.home();
  lcd0.print("P (Pa)  "); lcd0.print(pressure);

  if(panastatus == PRESENT){    //print panasonic data if present
    float pm1_0 = myAirSensor.getPM1_0();
    Serial.print(pm1_0, 2); //Print float with 2 decimals
    Serial.print(",");
  
    float pm2_5 = myAirSensor.getPM2_5();
    Serial.print(pm2_5, 2);
    lcd0.setCursor(0,1);
    lcd0.print("PM2.5   "); lcd0.print(pm2_5);
    Serial.print(",");
  
    float pm10 = myAirSensor.getPM10();
    Serial.print(pm10, 2);
   
    Serial.print(",");
  } else {
    Serial.print("n,n,n,");     //otherwise print -1 for sensor absent
  }

  if(adastatus == PRESENT){   //print adafruit data if preesnt. remember: need to manually set adafruit status (it's bad code, sorry)
    PM25_AQI_Data data;

    if(! aqi.read(&data)){
      Serial.println("Could not read from AQI");
      delay(500);
      return;
    }
    Serial.print(data.pm10_standard);
    Serial.print(",");

    Serial.print(data.pm25_standard);
    Serial.print(",");

    Serial.print(data.pm100_standard);
    Serial.print(",");
  } else {
    Serial.print("n,n,n,");     //otherwise print -1 for sensor absent
  }

  Serial.print("\n");
  sec++;
  delay(DELAY_PERIOD);
}
