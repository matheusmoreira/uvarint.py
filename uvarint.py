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

from itertools import repeat
from typing import List, Union, NamedTuple

def encode(number: int) -> bytes:
    def to_byte(number: int) -> int:
        return number & 0b1111_1111

    buffer: bytearray = bytearray()

    while number >= 0b1000_0000:
        buffer.append(to_byte(number) | 0b1000_0000)
        number >>= 7

    buffer.append(to_byte(number))

    return bytes(buffer)

class Decoded(NamedTuple):
    """Decoded integer and number of bytes read."""
    integer: int
    bytes_read: int

def decode(buffer: bytes, max: Union[int, float] = 9) -> Decoded:
    if not buffer:
        raise ValueError('no input bytes to decode')

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

    return Decoded(number | (byte << position), i + 1)

class Expected(NamedTuple):
    """Decoded integers and number of bytes read."""
    integers: List[int]
    bytes_read: int

def expect(n: int, buffer: bytes, max: Union[int, float] = 9) -> Expected:
    integers: List[int] = []
    total: int = 0

    for _ in repeat(None, n):
        decoded: int
        bytes_read: int

        decoded, bytes_read = decode(buffer[total:], max=max)

        integers.append(decoded)
        total += bytes_read

    return Expected(integers, total)
