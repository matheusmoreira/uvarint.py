# Unsigned variable-length integers.
#
# Specification:
#
#   1. Unsigned integers are serialized 7 bits at a time, starting with the least significant bits
#   2. The most significant bit (msb) in each output byte indicates if there is a continuation byte (msb = 1)
#   3. There are no signed integers
#   4. Integers are minimally encoded
#
# References:
#
#     https://github.com/multiformats/unsigned-varint
#

import typing

def encode(number: int) -> bytes:
    def to_byte(number: int) -> int:
        return number & 0b1111_1111

    buffer: bytearray = bytearray()

    while number >= 0b1000_0000:
        buffer.append(to_byte(number) | 0b1000_0000)
        number >>= 7

    buffer.append(to_byte(number))

    return bytes(buffer)

def decode(buffer: bytes, max: typing.Union[int, float] = 9) -> typing.Tuple[int, int]:
    number: int = 0
    position: int = 0

    i: int
    byte: int
    for i, byte in enumerate(buffer):
        if byte < 0b1000_0000:
            break

        number |= (byte & 0b0111_1111) << position
        position += 7

        if position / 7 >= max:
            raise OverflowError('decoded number larger than {} bytes'.format(max))

    return number | (byte << position), i + 1
