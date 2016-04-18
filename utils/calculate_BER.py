"""
This file opens two files, received_data.dat and original_data.dat, and
compare the bits on them. It prints the number of different bits, and
the BER obtained.
"""
import matplotlib.pyplot as plt
import numpy as np

def get_different_bits(byte1, byte2):
    xor = byte1 ^ byte2

    result = 0
    while xor != 0:
        result = result + (xor % 2)
        xor = xor // 2

    return result

with open("received_data.dat", "rb") as f:
    with open("original_data.dat", "rb") as g:
        received_byte = int.from_bytes(f.read(1), byteorder='big')
        original_byte = int.from_bytes(g.read(1), byteorder='big')
        result = 0
        i = 0
        results = []

        while received_byte != 0: 
            if (original_byte == 0):
                g.seek(0)
                original_byte = int.from_bytes(g.read(1), byteorder='big')

            result = result + get_different_bits(received_byte, original_byte)
            if result == 7:
                print(received_byte, original_byte)

            results.append(result)
            received_byte = int.from_bytes(f.read(1), byteorder='big')
            original_byte = int.from_bytes(g.read(1), byteorder='big')
            i += 1

        # Sometimes last byte messes all up an throws an error when it
        # shouldn't be one. With this 2 lines, we don't use the last byte
        # at all.
        del results[-1]
        result = results[-1]

print("# different bits:", result)
print("BER:", result / i)

plt.plot(range(0, len(results)), results)
plt.xlabel('# bytes')
plt.ylabel('# Erroneous bits')
plt.title('Error evolution')
plt.grid(True)
plt.show()
