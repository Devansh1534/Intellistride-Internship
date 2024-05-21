import time
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import mysql.connector
from datetime import datetime

# MySQL connection
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mydb"
)

# Modbus client
client = ModbusSerialClient(method='rtu', port='COM6', baudrate=9600, stopbits=1, bytesize=8, parity='E')
client.connect()

def hex_to_binary(hex_str):
    binary_str = bin(int(hex_str, 16))[2:].zfill(16)
    return binary_str

def concatenate_binaries(result_registers):
    concatenated_binary = ""
    for value in result_registers:
        hex_value = format(value, 'X').zfill(4)
        binary = hex_to_binary(hex_value)
        concatenated_binary += binary
    return concatenated_binary

def binary_to_float(binary_str):
    sign_bit = int(binary_str[0])
    exponent_bits = binary_str[1:9]
    fraction_bits = binary_str[9:]
    exponent = int(exponent_bits, 2) - 127
    fraction = 1
    for i in range(len(fraction_bits)):
        fraction += int(fraction_bits[i]) * 2**(-1 - i)
    value = (-1) ** sign_bit * fraction * 2 ** exponent
    return value

def read_and_store_data():
    result = client.read_holding_registers(address=100, count=30, slave=1)
    if not result.isError():
        result_registers = result.registers
        concatenated_binary = concatenate_binaries(result_registers)

        results = []
        for i in range(0, len(concatenated_binary), 32):
            binary_value = concatenated_binary[i:i+32]
            if len(binary_value) == 32:
                value = binary_to_float(binary_value)
                results.append(value)

        if results:
            mycursor = mydb.cursor()
            sql = "INSERT INTO energydata (voltage, current, power, energy, event_timestamp) VALUES (%s, %s, %s, %s, %s)"
            current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # Assuming the results list contains [voltage, current, power, energy] in that order
            mycursor.execute(sql, (*results[:4], current_timestamp))
            mydb.commit()
            mycursor.close()

# Fetch data every 10 seconds
while True:
    read_and_store_data()
    time.sleep(10)

client.close()
mydb.close()