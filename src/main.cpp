#include <Arduino.h>
#include <Hyperparameter.h>

/// Thư viện bổ trợ
#include <Wire.h>

/// Cảm biến + Động cơ
#include <Adafruit_Sensor.h>
#include <Adafruit_HMC5883_U.h>
#include <Servo.h>

typedef unsigned long ul;
ul current = 0;
int barrier_pins[3] = { LEFT_BARRIER, FORWARD_BARRIER, RIGHT_BARRIER };
bool barriers[3] = { false };

Adafruit_HMC5883_Unified mag = Adafruit_HMC5883_Unified(12345);
Servo left, right;

/*** Thuộc về phần xử lý Serial */
String __iterate_command(String command, int &pos);
void extract_speed(int &speed1, int &speed2, String command);
void filter_code(String command, int &pos);

/*** Thuộc về phần cảm biến */
bool read_barriers();
void send_barrier();
int compass();
float round_to_dp(float in_value, int decimal_place);
float measure_ntu();
float measure_tds();

/*** Phần chương trình chính */
void forward(String command);
void turn(String command);
void __turn_detail(int angle, bool dir);
void run_brushless(int speed1 = STOP_MOTOR, int speed2 = STOP_MOTOR);
void interept(String command);

void setup()
{
  Serial.begin(9600);

  // -------------------------------------------------------------------
  // Cài đặt kết nối với esc
  pinMode(ESC_PIN1, OUTPUT);
  pinMode(ESC_PIN2, OUTPUT);
  // -------------------------------------------------------------------

  // -------------------------------------------------------------------
  // Cài đặt cho cảm biến vật cản
  for (int i = 0; i < 3; i++)
    pinMode(barrier_pins[i], INPUT);
  // -------------------------------------------------------------------

  /**** Kết nối tới raspberry pi */
  if (DEBUG_SERIAL) Serial.println("Lắng nghe kết nối từ RASPBERRY_PI");
  while (true)
  {
    String package = String(ASK_RECEVIER) + SPLIT_PACKAGE + END_OF_PACKAGE;
    Serial.println(package);
    delay(2000);
    String response = Serial.readStringUntil(END_OF_PACKAGE);
    // if (DEBUG_SERIAL) Serial.println("Chưa kết nối được tới RASPBERRY_PI");
    if (response == String(ANSWER))
    {
      if (DEBUG_SERIAL) Serial.println("Đã kết nối tới raspberry pi");
      break;
    }
  }
  /**** ---------------------------------------------------------- */
  
  /// Gửi giá trị độc vật cản mặc định sang cho raspberry pi
  read_barriers();
  send_barrier();

  /*** Kết nối tới la bàn */
  // if(!mag.begin()) {
  //   Serial.println(String(ERROR_COMPASS) + END_OF_PACKAGE);
  //   while(1);
  // }
  // Serial.println(String(SUCCESS_COMPASS) + END_OF_PACKAGE);
  mag.begin();
  /*** ------------------------------------------------ */

  /// @brief  Lệnh delay để đợi kết nối tới motor
  delay(5000);

  /*** Kết nối tới động cơ */
  left.attach(ESC_PIN1, MIN_THROTTLE, MAX_THROTTLE);
  right.attach(ESC_PIN2, MIN_THROTTLE, MAX_THROTTLE);
  /**** --------------------------- */

  current = millis();
}

void loop()
{
  /// Nhận lệnh từ raspberry pi
  if (Serial.available())
  {
    String response = Serial.readStringUntil(END_OF_PACKAGE);
    if (response.length() > 0) {
      if (DEBUG_SERIAL)
      {
        Serial.print("Chuỗi lệnh nhận được là ");
        Serial.println(response);
      }
      interept(response);
      // Serial.println(String(RESPONSE_CONTROL) + SPLIT_PACKAGE + response[0] + END_OF_PACKAGE);
    }
  }

  /// Gửi tín hiệu cảm biến
  if ((ul)millis() - current > (ul)TIME_FOR_MEASURE)
  {
    current = (ul)millis();
    float ntu = measure_ntu();
    float tds = measure_tds();
    String command = String(SEND_DATA) + SPLIT_PACKAGE + String(ntu) + SPLIT_PACKAGE + String(tds) + SPLIT_PACKAGE + END_OF_PACKAGE;
    Serial.println(command);
  }

  /// Đọc tín hiệu vật cản
  if (read_barriers()) send_barrier();
}

// -----------------------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------

/***
 * Thuộc về phần serial
 * 
*/
String __iterate_command(String command, int &pos)
{
  /// @brief
  /// @param command
  /// @param pos
  /// @return trả về chuỗi kết quả được ngăn cách bởi <SPK>, đồng thời vị trí trỏ sẽ đi sang gói tin tiếp theo
  String temp;
  while (command[pos] != SPLIT_PACKAGE)
  {
    temp += command[pos];
    pos++;
  }
  pos++;
  return temp;
}

void extract_speed(int &speed1, int &speed2, String command)
{
  /// Skip for SPLIT_PACKAGE
  /// Structure code<SPK>speed1<SPK>speed2<SPK><EPK>
  int pos;
  filter_code(command, pos);
  String sp1 = __iterate_command(command, pos);
  String sp2 = __iterate_command(command, pos);
  speed1 = sp1.toInt();
  speed2 = sp2.toInt();
  if (speed1 == ERROR_COMMAND_SPEED)
    speed1 = DEFAULT_SPEED;
  if (speed2 == ERROR_COMMAND_SPEED)
    speed2 = DEFAULT_SPEED;
}

void filter_code(String command, int &pos)
{
  pos = 0;
  while (command[pos] != SPLIT_PACKAGE)
    pos++;
  pos++;
}
// -----------------------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------

/***
 * Thuộc về phần cảm biến
 * 
*/

bool read_barriers()
{
  bool stranger = false;
  for (int i = 0; i < 3; i++)
  {
    bool signal = digitalRead(barrier_pins[i]) == SIGNAL;
    if (barriers[i] != signal)
      stranger = true;
    barriers[i] = signal;
  }
  return stranger;
}

void send_barrier()
{
  String package = String(BARRIER_CODE);
  for (int i = 0; i < 3; i++)
  {
    package = package + SPLIT_PACKAGE + String( (int) barriers[i]);
  }
  package = package + SPLIT_PACKAGE + END_OF_PACKAGE;
  Serial.println(package);
}

int compass() 
{
  /* Get a new sensor event */ 
  sensors_event_t event; 
  mag.getEvent(&event);

  float heading = atan2(event.magnetic.y, event.magnetic.x);
  float declinationAngle = 0.22;
  heading += declinationAngle;
  
  // Correct for when signs are reversed.
  if(heading < 0)
    heading += 2*PI;
    
  // Check for wrap due to addition of declination.
  if(heading > 2*PI)
    heading -= 2*PI;
   
  // Convert radians to degrees for readability.
  return heading * 180/M_PI; 
}

float round_to_dp(float in_value, int decimal_place)
{
  float multiplier = powf(10.0f, decimal_place);
  in_value = roundf(in_value * multiplier) / multiplier;
  return in_value;
}

float measure_ntu()
{
  float volt = 0;
  for (int i = 0; i < LOOP_READ_VALUE_SENSOR_NTU; i++)
  {  
    volt += ((float)analogRead(NTU_SENSOR) / 1023) * 5;
    // Serial.println(analogRead(NTU_SENSOR));
  }
  volt /= LOOP_READ_VALUE_SENSOR_NTU;
  volt = round_to_dp(volt, 2);
  float ntu = 0;
  if (volt < 2.5)
    ntu = 3000;
  else
    ntu = -1120.4 * square(volt) + 5742.3 * volt - 4353.8;
  return ntu;
}

float measure_tds()
{
  int sensor_value = 0;
  for (int i = 0; i < LOOP_FOR_READING_TDS_SENSOR; i++) {
    // Serial.println(String(analogRead(TDS_SENSOR)));
    sensor_value += analogRead(TDS_SENSOR);
  }
  sensor_value /= LOOP_FOR_READING_TDS_SENSOR;
  float voltage = sensor_value * 5 / 1024;
  float tds = (133.42 * voltage * voltage * voltage - 255.86 * voltage * voltage + 857.39 * voltage) * 0.5;
  return tds;
}

// -----------------------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------
/***
 * Phần chương trình DEBUG cho chương trình chính
 * 
*/
void test_speed(int speed1, int speed2)
{
  Serial.print("Tốc độ động cơ đọc được lần lượt là: ");
  Serial.print(String(speed1));
  Serial.print(' ');
  Serial.print(String(speed2));
  Serial.println();
}

void test_angle(int angle, bool is_left)
{
  if (is_left) Serial.print("Tiến hành rẽ trái với tốc độ góc là ");
  else Serial.print("Tiến hành rẽ phải với tốc độ góc là ");
  Serial.print(String(angle));
  Serial.println();
}

// -----------------------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------
// -----------------------------------------------------------------------------------------------------------

/****
 * Phần chương trình chính
 * 
*/
void run_brushless(int speed1 = STOP_MOTOR, int speed2 = STOP_MOTOR)
{
  int speed_1 = map(speed1, 0, 100, MIN_SPEED, MAX_SPEED);
  int speed_2 = map(speed2, 0, 100, MIN_SPEED, MAX_SPEED);
  left.write(speed_1);
  right.write(speed_2);
}

void forward(String command)
{
  int speed1, speed2;
  extract_speed(speed1, speed2, command);
  if (DEBUG_SERIAL) test_speed(speed1, speed2);
  Serial.println(command[0] + SPLIT_PACKAGE + String(speed1) + SPLIT_PACKAGE + END_OF_PACKAGE);
  run_brushless(speed1, speed2);
}

void turn(String command)
{
  int pos;
  filter_code(command, pos);
  String angle = __iterate_command(command, pos);
  int real_angle = angle.toInt();
  if (DEBUG_SERIAL) test_angle(real_angle, command[0] == LEFT);
  Serial.println(String(RESPONSE_CONTROL) + command[0] + SPLIT_PACKAGE + String(real_angle) + SPLIT_PACKAGE + END_OF_PACKAGE);
  __turn_detail(real_angle, command[0] == RIGHT);
}

void __turn_detail(int angle, bool dir)
{
  int de, temp=compass();
  if (dir) //right
  {
    //Serial.println(temp);
    de=temp+angle;
    if (de>=360) de-=360;  
    while (1)
    {
      if (temp >= de-RANGE_DEG && temp <= de+RANGE_DEG)
        break;      
      run_brushless(0,50);
      temp=compass();
    }
    delay(100);
    run_brushless();
  }
  else //left 
  {
    de=temp-angle;
    if (de<0) de+=360;
      
    while (1)
    {
      if (temp >= de-RANGE_DEG && temp <= de+RANGE_DEG)
        break;
      run_brushless(50,0);
      temp=compass();
    }
    delay(100);
    run_brushless();    
  }
}

void interept(String command)
{
  switch (command[0])
  {
    case FORWARD:
      forward(command);
      break;
    case LEFT:
    case RIGHT:
      turn(command);
      break;
    default:
      run_brushless();  
      break; 
  }
}