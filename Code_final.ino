#include <Digital_Light_ISL29035.h>
#include <Digital_Light_TSL2561.h>




/*
 * HDC1080_Arduino_Example.ino
 * Created: July 21st 2017
 * This sketch is released AS-IS into the public domain, no guarantee or warranty is given.
 * This Code is not supported by Texas Instruments.
 * 
 * Description: This sketch configures the HDC1080 and Arduino Uno to read and display the 
 * local temperature and humidty to a standard 1602 LCD display. Please see the associated
 * schematic for setup information. 
 * 
 * Copyright (C) 2017 Texas Instruments Incorporated - http://www.ti.com/ 
 * 
 *  Redistribution and use in source and binary forms, with or without 
 *  modification, are permitted provided that the following conditions 
 *  are met:
 *
 *    Redistributions of source code must retain the above copyright 
 *    notice, this list of conditions and the following disclaimer.
 *
 *    Redistributions in binary form must reproduce the above copyright
 *    notice, this list of conditions and the following disclaimer in the 
 *    documentation and/or other materials provided with the   
 *    distribution.
 *
 *    Neither the name of Texas Instruments Incorporated nor the names of
 *    its contributors may be used to endorse or promote products derived
 *    from this software without specific prior written permission.
 *
 *  THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS 
 *  "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT 
 *  LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
 *  A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT 
 *  OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, 
 *  SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT 
 *  LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
 *  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
 *  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT 
 *  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE 
 *  OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
 *
*/
#include <IRremote.h>
#include <PID_v1.h>
#include <Wire.h>
volatile bool alu= true;
volatile bool alu_prio = false;
volatile bool prio = false;
volatile unsigned long wait = 0;
int constante_wait = 10000; /* 900 000 pour 15 minute */
double temperature;
double humidity;
int state=0;
volatile char order;
int pwm=9;
int mouv=8;
const int RECV_PIN = 7;
IRrecv irrecv(RECV_PIN);
decode_results results;
volatile int ir_command = 0;
volatile unsigned long old_time=0;
volatile unsigned long real_time=0;
volatile bool change_l=false;
volatile int inten=1000;
float gain_p = 80.0;
float gain_i=0.0;
float gain_d=0.0;
double input_led, setpoint_led, output_led;
PID PID_led (&input_led, &output_led, &setpoint_led, gain_p, gain_i, gain_d, DIRECT);

void setup() {
   //Initialize I2C Communication
  Wire.begin();
  Serial.begin(9600);
  Serial1.begin(9600);
  Serial3.begin(9600);
  pinMode(pwm,OUTPUT);
  pinMode(mouv,INPUT);
  TSL2561.init();
  // PID
  PID_led.SetMode(AUTOMATIC);
  PID_led.SetOutputLimits(0,255);
  //IR
  irrecv.enableIRIn();
  
  //Configure HDC1080
  Wire.beginTransmission(0x40);
  Wire.write(0x02);
  Wire.write(0x90);
  Wire.write(0x00);
  Wire.endTransmission();

  //Delay for Startup of HDC1080
  delay(20);
}

void loop() 
{
  real_time=millis();
  if( (real_time - old_time) > 1000){
    old_time= real_time;
    sentdata(temperature);
    
  }
  if(Serial1.available() > 0){
    communication_blue();
  }

  if(Serial3.available() > 0){
    communication_onion();
  }
  mouvement();
  // mettre commentaire si génération de la pwm avec onion
  allumage();
 
}

void IR_commande(){
  if (irrecv.decode(&results)){
        if (results.value == 16754775){
          ir_command = 1;
        }
        if (results.value == 16769055){
          ir_command = 0;
        }
        irrecv.resume();
  }
  Serial.println(ir_command);
}
void communication_blue(){
  
   // Checks whether data is comming from the serial port
   state = Serial1.read(); // Reads the data from the serial port
   
   if (state == 'a') {
    if (prio== true){
        alu_prio=false; // Turn LED OFF
        Serial.println("LED: OFF"); // Send back, to the phone, the String "LED: ON"
        state = 0;
    }
    else{
        state=0;
      }
   }
   else if (state == 'A') {
    if (prio== true){
      alu_prio=true;
      Serial.println("LED: ON");
      state = 0;
    }
    else{
      state=0;
    }
  }
  else if ( state == 'D'){
    prio = true;
    Serial.println("priorité activé");
    state = 0;
  }
  else if ( state == 'd'){
    prio=false;
    Serial.println("priorité désactivé");
    alu_prio=false;
    state = 0;
  }
}
void communication_onion(){
  
    humidity = readSensor(&temperature);
    order = Serial3.read();
    Serial.println("Onion");
    Serial.println((char)order);
  
    if (order == 't'){

      Serial3.write((uint8_t)temperature);
    }
    else if (order == 'h'){
      Serial3.write((uint8_t)humidity);
    }
    else if (order == 'l'){
      Serial3.write((uint8_t)TSL2561.readVisibleLux());
    }
    else if (order == 'm'){
      Serial3.write((uint8_t)mouvement());
    }
    else if (order =='b'){
      Serial.write(alu_prio);
    }
    else if (order == 'i'){
      Serial3.write((uint8_t)ir_command);
    }
    else if (order == 'X'){
      inten=500;
    }
    else if (order == 'Y'){
      inten=1000;
    }
    else if (order == 'Z'){
      inten=2000;
    }
    else if (order =='a'){
      prio=true;
      alu_prio=false;
    }
    else if (order == 'A'){
      prio=true;
      alu_prio=true;
    }
    else if (change_l==true){
      change_l=false;
    }
    else if (order =='L'){
      change_l=true;
    }
    else{
      Serial3.write("erreur");
    }
    
}
void allumage(){
  
  setpoint_led=inten;
  double val= (double)TSL2561.readVisibleLux();
  input_led=val;
  if(prio ==true){
    if (alu == true && alu_prio == true){
      PID_led.Compute();
      analogWrite(pwm,output_led);
    }
  
    else if (alu == false && alu_prio == false) {
      analogWrite(pwm,0);
    }
  
    else if (alu == false && alu_prio == true) {
      PID_led.Compute();
      analogWrite(pwm,output_led);
    }
    else if (alu == true && alu_prio == false) {
      analogWrite(pwm,0);
    }
    
  }
  else{
    if (alu ==true){
      PID_led.Compute();
      analogWrite(pwm,output_led);
    }
    else{
      analogWrite(pwm,0);
    }
  }
}


void sentdata(double temperature){
    
    humidity = readSensor(&temperature);
    Serial.println("temperature");
    Serial.println((uint8_t)temperature);
    Serial.println("humidité");
    Serial.println((int)humidity);
    Serial.println("luminosité");
    Serial.println((int)TSL2561.readVisibleLux());
    Serial.println("détection de mouvement");
    Serial.println(mouvement());
    Serial.println("allumage");
    Serial.println(alu);
    Serial.println("allumage prioritaire");
    Serial.println(alu_prio);

  }

int mouvement(){

  int det = digitalRead(mouv);

  if ( det == 1){
    alu=true;
    wait = millis(); 
  }

  else{
    if ( (real_time - wait) > constante_wait){
      alu= false;
    }
  }
  return det;
}
double readSensor(double* temperature)
{
  //holds 2 bytes of data from I2C Line
  uint8_t Byte[4];

  //holds the total contents of the temp register
  uint16_t temp;

  //holds the total contents of the humidity register
  uint16_t humidity;
  
  //Point to device 0x40 (Address for HDC1080)
  Wire.beginTransmission(0x40);
  //Point to register 0x00 (Temperature Register)
  Wire.write(0x00);
  //Relinquish master control of I2C line
  //pointing to the temp register triggers a conversion
  Wire.endTransmission();
  
  //delay to allow for sufficient conversion time
  delay(20);
  
  //Request four bytes from registers
  Wire.requestFrom(0x40, 4);

  delay(1);
  
  //If the 4 bytes were returned sucessfully
  if (4 <= Wire.available())
  {
    //take reading
    //Byte[0] holds upper byte of temp reading
    Byte[0] = Wire.read();
    //Byte[1] holds lower byte of temp reading
    Byte[1] = Wire.read();
    
    //Byte[3] holds upper byte of humidity reading
    Byte[3] = Wire.read();
    //Byte[4] holds lower byte of humidity reading
    Byte[4] = Wire.read();

    //Combine the two bytes to make one 16 bit int
    temp = (((unsigned int)Byte[0] <<8 | Byte[1]));

    //Temp(C) = reading/(2^16)*165(C) - 40(C)
    *temperature = (double)(temp)/(65536)*165-40;

   //Combine the two bytes to make one 16 bit int
    humidity = (((unsigned int)Byte[3] <<8 | Byte[4]));

    //Humidity(%) = reading/(2^16)*100%
    return (double)(humidity)/(65536)*100;
  }
}
