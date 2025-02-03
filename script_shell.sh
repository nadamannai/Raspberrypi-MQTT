
modprobe i2c-dev
modprobe aht10
i2cdetect -y 1

if ! i2cdetect -y 1 | grep -q "38"; then
  echo "Failed to register AHT10 sensor at address 0x38. Exiting."
  exit 1
fi

echo aht10 0x38 > /sys/bus/i2c/devices/i2c-1/new_device

hwmon_dir="/sys/class/hwmon/hwmon2"
temperature_file="$hwmon_dir/temp1_input"
humidity_file="$hwmon_dir/humidity1_input"


# Check if hwmon2 directory exists
if [ -d "$hwmon_dir" ]; then
    echo "hwmon2 directory exists: $hwmon_dir"
else
    echo "Error: hwmon2 directory not found: $hwmon_dir"
fi

# Check if the temperature file exists
if [ -f "$temperature_file" ]; then
    echo "Temperature file exists: $temperature_file"
else
    echo "Error: Temperature file not found: $temperature_file"
fi

# Check if the humidity file exists
if [ -f "$humidity_file" ]; then
    echo "Humidity file exists: $humidity_file"
else
    echo "Error: Humidity file not found: $humidity_file"
fi

python3 python_pub.py

