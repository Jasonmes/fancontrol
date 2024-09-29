import subprocess

def get_sensors_output():
    try:
        result = subprocess.run(['sensors'], stdout=subprocess.PIPE, text=True)
        return result.stdout
    except Exception as e:
        print(f"Error reading sensors: {e}")
        return None

def parse_cpu_temp(sensors_output):
    lines = sensors_output.split('\n')
    for line in lines:
        if "Core 0" in line:  # Adjust based on your sensors output
            temp_str = line.split(':')[1].split('°')[0].strip()
            return float(temp_str)
    return None

if __name__ == "__main__":
    sensors_output = get_sensors_output()
    if sensors_output:
        cpu_temp = parse_cpu_temp(sensors_output)
        if cpu_temp:
            print(f"CPU Temperature: {cpu_temp}°C")
        else:
            print("Could not find CPU temperature in sensors output")
