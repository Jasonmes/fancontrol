import pynvml

def get_gpu_temperature():
    try:
        pynvml.nvmlInit()  # Initialize NVML
        device_count = pynvml.nvmlDeviceGetCount()  # Get the number of GPUs
        
        for i in range(device_count):
            handle = pynvml.nvmlDeviceGetHandleByIndex(i)  # Get the GPU handle
            temp = pynvml.nvmlDeviceGetTemperature(handle, pynvml.NVML_TEMPERATURE_GPU)
            name = pynvml.nvmlDeviceGetName(handle)
            print(f"GPU {i} ({name.decode('utf-8')}): {temp}°C")
        
        pynvml.nvmlShutdown()  # Don't forget to shutdown the NVML session
    except pynvml.NVMLError as error:
        print(f"Failed to get GPU temperature: {error}")

if __name__ == "__main__":
    get_gpu_temperature()
