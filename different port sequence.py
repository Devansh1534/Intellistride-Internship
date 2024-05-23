import time
from pymodbus.client.serial import ModbusSerialClient
from pymodbus.constants import Endian
from pymodbus.payload import BinaryPayloadDecoder
import mysql.connector
from datetime import datetime


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="root",
  database="mydb"
)


client = ModbusSerialClient(method='rtu', port='COM6', baudrate=9600, stopbits=1, bytesize=8, parity='E')
client.connect()

def hex_to_binary(hex_str):
    binary_str = bin(int(hex_str, 16))[2:].zfill(16)
    return binary_str

def process_registers(registers):
    concatenated_binary = ""
    for value in registers:
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

def read_and_process_registers(address, count):
    result = client.read_holding_registers(address=address, count=count, slave=1)
    registers = result.registers
    concatenated_binary = process_registers(registers)
    
    results = []
    for i in range(0, len(concatenated_binary), 16):
        binary_value = concatenated_binary[i:i+16]
        results.append(binary_to_float(binary_value))
    
    return results

results_100_120 = read_and_process_registers(101, 20)  

results_140_160 = read_and_process_registers(141, 20)  

all_results = results_100_120 + results_140_160

mycursor = mydb.cursor()
sql = "INSERT INTO energydata (voltage, event_timestamp) VALUES (%s, %s)"
current_timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

for voltage_val in all_results:
    mycursor.execute(sql, (voltage_val, current_timestamp))

mydb.commit()
mycursor.close()
mydb.close()

print(all_results)