import os
import time

# Paths for fan and pwm control
pwm_path = "/sys/class/hwmon/hwmon3/pwm2"
fan_speed_path = "/sys/class/hwmon/hwmon3/fan6_input"
temp_sensor_path = "/sys/class/hwmon/hwmon3/temp1_input"  # Assuming a temperature sensor

# Function to write a value to pwm control
def set_fan_speed(pwm_value):
    try:
        with open(pwm_path, 'w') as pwm_file:
            pwm_file.write(str(pwm_value))
        print(f"Fan speed set to {pwm_value}")
    except IOError:
        print("Error: Unable to set fan speed. Try running as root.")

# Function to read the current fan speed
def get_fan_speed():
    try:
        with open(fan_speed_path, 'r') as fan_file:
            return int(fan_file.read().strip())
    except IOError:
        print("Error: Unable to read fan speed.")
        return None

# Function to read the current temperature
def get_temperature():
    try:
        with open(temp_sensor_path, 'r') as temp_file:
            # Temperature is usually in millidegree Celsius
            temp_millicelsius = int(temp_file.read().strip())
            return temp_millicelsius / 1000.0  # Convert to Celsius
    except IOError:
        print("Error: Unable to read temperature.")
        return None

# Main loop to control fan based on temperature
def control_fan():
    try:
        while True:
            temperature = get_temperature()
            if temperature is None:
                break

            print(f"Current temperature: {temperature}°C")

            # Adjust fan speed based on temperature thresholds
            if temperature > 45:
                set_fan_speed(255)  # Max speed
            elif temperature > 40:
                set_fan_speed(255)
            elif temperature > 35:
                set_fan_speed(255)
            elif temperature > 25:
                set_fan_speed(255)
            else:
                set_fan_speed(30)  # Minimum speed

            fan_speed = get_fan_speed()
            if fan_speed is not None:
                print(f"Current fan speed: {fan_speed} RPM")

            time.sleep(10)  # Check every 10 seconds
    except KeyboardInterrupt:
        print("Fan control interrupted. Restoring automatic control...")
        set_fan_speed(0)  # 0 usually restores automatic control

if __name__ == "__main__":
    control_fan()
