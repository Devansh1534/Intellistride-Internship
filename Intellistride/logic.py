def hex_to_binary(hex_str):
    binary_str = bin(int(hex_str, 16))[2:].zfill(16)
    return binary_str

def main(result_registers):
    binary_values = [hex_to_binary(format(reg, 'X').zfill(4)) for reg in result_registers]
    concatenated_binary = ''.join(binary_values)
    return concatenated_binary

def registers(address, count, slave):
    return [0xABCD, 0x1234]

result_registers = registers(address=142, count=2, slave=1)
concatenated_binary = main(result_registers)
print(concatenated_binary)