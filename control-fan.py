import os
import time

# Paths to the PWM control and temperature files (replace with your actual paths)
PWM_PATHS = [
    "/sys/class/hwmon/hwmon5/pwm1",
    "/sys/class/hwmon/hwmon5/pwm2",
    "/sys/class/hwmon/hwmon5/pwm3",
    "/sys/class/hwmon/hwmon5/pwm4",
    "/sys/class/hwmon/hwmon5/pwm6",
    "/sys/class/hwmon/hwmon5/pwm7"
]
TEMP_PATH = "/sys/class/hwmon/hwmon5/temp1_input"  # Change based on your temperature sensor
FAN_MANUAL_MODE_PATHS = [
    "/sys/class/hwmon/hwmon5/pwm1_enable",
    "/sys/class/hwmon/hwmon5/pwm2_enable",
    "/sys/class/hwmon/hwmon5/pwm3_enable",
    "/sys/class/hwmon/hwmon5/pwm4_enable",
    "/sys/class/hwmon/hwmon5/pwm6_enable",
    "/sys/class/hwmon/hwmon5/pwm7_enable"
]

# Configuration based on your fan settings
MINTEMP = 20  # Temperature at which the fan starts spinning (in °C)
MAXTEMP = 40  # Temperature at which the fan reaches maximum speed (in °C)
MINSTART = 100  # Minimum PWM value at which the fan starts spinning
MINSTOP = 20  # PWM value at which the fan stops spinning

# Function to set the PWM value (0 to 255)
def set_fan_speed(pwm_path, speed):
    try:
        with open(pwm_path, 'w') as pwm_file:
            pwm_file.write(str(speed))
        print(f"Fan speed set to {speed} for {pwm_path}")
    except Exception as e:
        print(f"Error setting fan speed: {e}")

# Function to set manual control mode for fans (1 = manual, 0 = automatic)
def set_manual_mode(fan_manual_mode_path, mode):
    try:
        with open(fan_manual_mode_path, 'w') as mode_file:
            mode_file.write(str(mode))
        print(f"Fan control mode set to {'manual' if mode == 1 else 'automatic'} for {fan_manual_mode_path}")
    except Exception as e:
        print(f"Error setting fan control mode: {e}")

# Function to get current temperature (in °C)
def get_temperature(temp_path):
    try:
        with open(temp_path, 'r') as temp_file:
            # The temperature is usually in millidegrees Celsius
            return int(temp_file.read().strip()) / 1000
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

# Function to calculate fan speed based on temperature
def calculate_fan_speed(temp, mintemp, maxtemp, minstart, minstop):
    if temp <= mintemp:
        return minstop  # Fan stops at or below MINTEMP
    elif temp >= maxtemp:
        return 255  # Full speed at MAXTEMP or above
    else:
        # Linear scaling of fan speed between MINTEMP and MAXTEMP
        speed = int((temp - mintemp) / (maxtemp - mintemp) * (255 - minstart) + minstart)
        return max(minstart, min(speed, 255))  # Ensure speed is within valid range


if __name__ == "__main__":
    # Set manual control mode for all fans
    for manual_mode_path in FAN_MANUAL_MODE_PATHS:
        set_manual_mode(manual_mode_path, 1)

    while True:
        # Get the current system temperature
        current_temp = get_temperature(TEMP_PATH)
        if current_temp is None:
            print("Unable to read temperature. Skipping fan adjustment.")
            time.sleep(5)
            continue

        print(f"Current temperature: {current_temp}°C")

        # Calculate the appropriate fan speed based on the temperature
        new_fan_speed = calculate_fan_speed(current_temp, MINTEMP, MAXTEMP, MINSTART, MINSTOP)

        # Set the new fan speeds for all PWM controls
        for pwm_path in PWM_PATHS:
            set_fan_speed(pwm_path, new_fan_speed)

        # Wait for a defined interval before checking the temperature again
        time.sleep(10)  # Adjust the interval as needed
