def mod4bit(data: bytearray, start_value=0xAAAA):
    byte_sum = start_value
    # Iterate bytes in data
    for byte in data:
        byte_sum += byte
    return (((byte_sum) % 16))


def crc8(data: bytearray, initial_value=0xFF, polynom=0x07, xor_output=0x00):
    crc = initial_value
    # Iterate bytes in data
    for byte in data:
        # Iterate bits in byte
        for _ in range(0, 8):
            if (crc >> 7) ^ (byte & 0x01):
                crc = ((crc << 1) ^ polynom) & 0xFF
            else:
                crc = (crc << 1) & 0xFF
            # Shift to next bit
            byte = byte >> 1
    return crc ^ xor_output


def crc16(data: bytearray, initial_value=0xFFFF, polynom=0x1021, xor_output=0x00):
    if data is None or len(data) == 0:
        raise Exception("No data to process crc16")
    crc = initial_value
    # Iterate bytes in data
    for byte in data:
        crc ^= byte << 8
        # Iterate bits in byte
        for _ in range(0, 8):
            if (crc & 0x8000) > 0:
                crc = (crc << 1) ^ polynom
            else:
                crc = crc << 1
    return (crc ^ xor_output) & 0xFFFF
