//DTH11
//------------------
#include <DHT.h>
#include <DHT_U.h>
//------------------

// Motor -----------
int IN1 = 11;
int IN2 = 10;
int IN3 = 6;
int IN4 = 5;
//------------------

// Ultrasonico -----
int TRIG = A0;     
int ECO = A1;   
int DURACION;
int DISTANCIA;
//------------------

// DTH11 -----------
int SENSOR = 7;
float TEMPERATURA;
float HUMEDAD;
DHT dht(SENSOR, DHT11);
//------------------

// Rpm -------------
unsigned int rpm;
volatile int contador;

int sampleTime = 500;
unsigned long lastTime = 0;
//-------------------

// Buffer -----------
char elbuffer[50];
//-------------------

// Opcion prender motor
char option = ' ';
//---------------------

void setup(){  

Serial.begin(9600);

  // Motor---------------
  pinMode(IN1,OUTPUT);
  pinMode(IN2,OUTPUT);
  pinMode(IN3,OUTPUT);
  pinMode(IN4,OUTPUT);
  //---------------------

  // Ultrasonico ---------
  pinMode(TRIG, OUTPUT);
  pinMode(ECO, INPUT); 
  //----------------------
  
  // Tracker ------------
  pinMode(2,INPUT);
  attachInterrupt(0,interrupcion,FALLING);
  //----------------------

  // DTH11 ---------------
  dht.begin();
  //----------------------

  rpm=0;
  contador=0; 

}

void loop() {

  //digitalWrite(IN1, HIGH);
  //digitalWrite(IN2, LOW);

  imprimirTodo();

  if(Serial.available()!=0){

    option = Serial.read();

   
    if(option == 'e')
    {
      digitalWrite(IN1, HIGH);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, HIGH);
      digitalWrite(IN4, LOW);
      option = ' ';  
    }
    if(option == 'a')
    {
      digitalWrite(IN1, LOW);
      digitalWrite(IN2, LOW);
      digitalWrite(IN3, LOW);
      digitalWrite(IN4, LOW);
      option = ' '; 
    }
 }
}

void calculoUltrasonico()
{
  if(millis()-lastTime>sampleTime)
  { 
    digitalWrite(TRIG, HIGH);     // generacion del pulso a enviar
    delay(1);       // al pin conectado al trigger
    digitalWrite(TRIG, LOW);    // del sensor
    
    DURACION = pulseIn(ECO, HIGH);  // con funcion pulseIn se espera un pulso
    
    DISTANCIA = DURACION / 58.2;    // distancia medida en centimetros
    lastTime = millis();
  }
}

void calculoRpm()
{
  if(millis()-lastTime>sampleTime)
  { 
    detachInterrupt(0);
    rpm = (60*1000 / contador )/(millis() - lastTime) * contador;
    lastTime = millis();
    contador = 0;
    Serial.println(rpm);
    
    attachInterrupt(0, interrupcion, FALLING);
  }
}

void interrupcion()
{
  contador++;
}

void imprimirTodo()
{ 
  if(millis()-lastTime>sampleTime)
  {
    // Ultrasonico -----------------------
       
    digitalWrite(TRIG, HIGH);     // generación del pulso a enviar
    delay(1);       // al pin conectado al trigger
    digitalWrite(TRIG, LOW);    // del sensor
    
    DURACION = pulseIn(ECO, HIGH);  // con función pulseIn se espera un pulso
              // alto en Echo
    DISTANCIA = DURACION / 58.2;    // distancia medida en centimetros
 
    //-------------------------------------

    // Rpm --------------------------------
    
    detachInterrupt(0);
    rpm = contador*(0.281283422459893/(millis() - lastTime))*(60000/20);

    
    lastTime = millis();
    contador = 0;

    // TEMPERATURA
    TEMPERATURA = dht.readTemperature();
    HUMEDAD = dht.readHumidity();
    
    String t = String(TEMPERATURA);
    String h = String(HUMEDAD);
    String d = String(DISTANCIA);
    String r = String(rpm);
    
    Serial.println(t+","+h+","+d+","+r);
    attachInterrupt(0, interrupcion, FALLING);
    
  }
}
