import os
import time
import subprocess
import re

# Paths to the PWM control and temperature files
PWM_PATHS = [
    "/sys/class/hwmon/hwmon5/pwm1",
    "/sys/class/hwmon/hwmon5/pwm2",
    "/sys/class/hwmon/hwmon5/pwm3",
    "/sys/class/hwmon/hwmon5/pwm4",
    "/sys/class/hwmon/hwmon5/pwm6",
    "/sys/class/hwmon/hwmon5/pwm7"
]
CPU_TEMP_PATH = "/sys/class/hwmon/hwmon5/temp1_input"  # Change based on your CPU sensor
FAN_MANUAL_MODE_PATHS = [
    "/sys/class/hwmon/hwmon5/pwm1_enable",
    "/sys/class/hwmon/hwmon5/pwm2_enable",
    "/sys/class/hwmon/hwmon5/pwm3_enable",
    "/sys/class/hwmon/hwmon5/pwm4_enable",
    "/sys/class/hwmon/hwmon5/pwm6_enable",
    "/sys/class/hwmon/hwmon5/pwm7_enable"
]

# Configuration for fan control
MINTEMP = 20  # Minimum temperature (in °C)
MAXTEMP = 40  # Maximum temperature (in °C)
MINSTART = 100  # Minimum fan speed (PWM value)
MINSTOP = 40  # Minimum stop speed (PWM value)

# Function to set fan speed (0 to 255)
def set_fan_speed(pwm_path, speed):
    try:
        with open(pwm_path, 'w') as pwm_file:
            pwm_file.write(str(speed))
        print(f"Fan speed set to {speed} for {pwm_path}")
    except Exception as e:
        print(f"Error setting fan speed: {e}")

# Function to set manual mode for fans (1 = manual, 0 = automatic)
def set_manual_mode(fan_manual_mode_path, mode):
    try:
        with open(fan_manual_mode_path, 'w') as mode_file:
            mode_file.write(str(mode))
        print(f"Fan control mode set to {'manual' if mode == 1 else 'automatic'} for {fan_manual_mode_path}")
    except Exception as e:
        print(f"Error setting fan control mode: {e}")

# Function to get CPU temperature (in °C)
def get_cpu_temperature(temp_path):
    try:
        with open(temp_path, 'r') as temp_file:
            return int(temp_file.read().strip()) / 1000  # Convert from millidegrees Celsius
    except Exception as e:
        print(f"Error reading CPU temperature: {e}")
        return None

# Function to get GPU temperature using nvidia-smi
def get_gpu_temperature():
    try:
        result = subprocess.run(['nvidia-smi', '--query-gpu=temperature.gpu', '--format=csv,noheader,nounits'],
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # Extract temperatures and select the one for the RTX 3090
        temperatures = result.stdout.strip().split('\n')
        for line in temperatures:
            if 'RTX 3090' in line:
                gpu_temp_str = re.search(r'\d+', line)
                if gpu_temp_str:
                    return int(gpu_temp_str.group(0))
        print("RTX 3090 not found. Make sure it's connected.")
        return None
    except Exception as e:
        print(f"Error reading GPU temperature: {e}")
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
        # Get the current CPU temperature
        current_cpu_temp = get_cpu_temperature(CPU_TEMP_PATH)
        if current_cpu_temp is None:
            print("Unable to read CPU temperature. Skipping fan adjustment.")
            time.sleep(5)
            continue

        # Get the current GPU temperature
        current_gpu_temp = get_gpu_temperature()
        if current_gpu_temp is None:
            print("Unable to read GPU temperature. Skipping fan adjustment.")
            time.sleep(5)
            continue

        print(f"Current CPU temperature: {current_cpu_temp}°C")
        print(f"Current GPU temperature: {current_gpu_temp}°C")

        # Take the maximum of CPU and GPU temperatures to determine fan speed
        max_temp = max(current_cpu_temp, current_gpu_temp)

        # Calculate the fan speed based on the maximum temperature
        new_fan_speed = calculate_fan_speed(max_temp, MINTEMP, MAXTEMP, MINSTART, MINSTOP)

        # Set the new fan speeds for all PWM controls
        for pwm_path in PWM_PATHS:
            set_fan_speed(pwm_path, new_fan_speed)

        # Wait for a defined interval before checking the temperature again
        time.sleep(10)  # Adjust the interval as needed
