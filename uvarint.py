"""Unsigned variable-length integers.

Encode and decode unsigned varints to and from bytes.

Examples:
    encode(integer)
    decode(buffer)
    decode(big_buffer, limit=math.inf)
    expect(3, buffer_with_multiple_values)

Specification:

    1. Unsigned integers are serialized 7 bits at a time,
       starting with the least significant bits
    2. The most significant bit (msb) in each output byte
       indicates if there is a continuation byte (msb = 1)
    3. There are no signed integers
    4. Integers are minimally encoded
"""

from itertools import repeat
from typing import List, Union, NamedTuple


Number = Union[int, float]


def encode(integer: int) -> bytes:
    """Encodes an integer as an uvarint.

    :param integer: the integer to encode
    :return: bytes containing the integer encoded as an uvarint
    """
    def to_byte(integer: int) -> int:
        return integer & 0b1111_1111

    buffer: bytearray = bytearray()

    while integer >= 0b1000_0000:
        buffer.append(to_byte(integer) | 0b1000_0000)
        integer >>= 7

    buffer.append(to_byte(integer))

    return bytes(buffer)


class Decoded(NamedTuple):
    """Decoded integer and number of bytes read."""
    integer: int
    bytes_read: int


def decode(buffer: bytes, limit: Number = 9) -> Decoded:
    if not buffer:
        raise ValueError('no input bytes to decode')

    integer: int = 0
    position: int = 0

    i: int
    byte: int
    for i, byte in enumerate(buffer):
        if byte < 0b1000_0000:
            break

        integer |= (byte & 0b0111_1111) << position
        position += 7

        if position / 7 >= limit:
            raise OverflowError('integer > {} bytes'.format(limit))

    return Decoded(integer | (byte << position), i + 1)


class Expected(NamedTuple):
    """Decoded integers and number of bytes read."""
    integers: List[int]
    bytes_read: int


def expect(count: int, buffer: bytes, limit: Number = 9) -> Expected:
    integers: List[int] = []
    total: int = 0

    for _ in repeat(None, count):
        decoded: int
        bytes_read: int

        decoded, bytes_read = decode(buffer[total:], limit=limit)

        integers.append(decoded)
        total += bytes_read

    return Expected(integers, total)
