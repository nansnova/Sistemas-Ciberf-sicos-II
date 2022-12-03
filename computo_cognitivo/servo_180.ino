// Libreria para controlar el servo
#include <Servo.h>

Servo servoMotor;
 
void setup() {
  // Monitor serial para mostrar el resultado
  Serial.begin(9600);
  // Iniciacion del servo en el pin 6
  servoMotor.attach(6);
  // Inicializar el servomotor en el angulo 0 
  servoMotor.write(0);
  delay(1000);
}
 
void loop() {
  // Desplaza a la posición 180º
  servoMotor.write(180);
  // Espera 1 segundo
  delay(1000);
  servoMotor.write(0);
}
