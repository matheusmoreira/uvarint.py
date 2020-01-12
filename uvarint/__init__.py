"""Unsigned variable-length integers.

Encode and decode unsigned varints to and from bytes.

Examples:
    encode(integer)
    decode(buffer)
    decode(big_buffer, limit=math.inf)
    expect(3, buffer_with_multiple_values)
    cut(3, buffer_with_multiple_values)

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


# Limit decoding to at most 9 bytes by default.
LIMIT = 9


def decode(buffer: bytes, limit: Number = LIMIT) -> Decoded:
    """Decodes one uvarint in the given buffer.

    In addition to the decoded integer, the number of bytes read is returned.
    This allows the caller to seek past the integer in the buffer.

    The buffer may not be None or empty.
    There is no reasonable value to return in that case.
    ValueError will be raised.

    To prevent denial of service attacks, memory consumption is limited.
    By default, a limit of 9 bytes will be imposed on any inputs.
    The function will decode values in the interval [0, 2^63 - 1]
    and will raise OverflowError for bigger integers.
    This limit can be changed through the limit keyword argument.
    It can be removed entirely by passing math.inf.

    :param buffer: bytes containing at least one uvarint encoded integer
    :param limit: maximum number of bytes to decode
    :return: decoded integer and number of bytes read by the function
    """
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


def expect(count: int, buffer: bytes, limit: Number = LIMIT) -> Expected:
    """Decodes the expected number of uvarints in the given buffer.

    In addition to the list of decoded integers,
    the total number of bytes read is returned.
    This allows the caller to seek past the decoded data in the buffer.

    Should the buffer not contain the expected amount of uvarints,
    ValueError will be raised.

    The buffer may be None or empty if the expected count is zero.
    The result will be an empty list and a total of zero bytes read.

    To prevent denial of service attacks, memory consumption is limited.
    By default, a limit of 9 bytes will be imposed on individual uvarints.
    The function will decode values in the interval [0, 2^63 - 1]
    and will raise OverflowError for bigger integers.
    This limit can be changed through the limit keyword argument.
    It can be removed entirely by passing math.inf.

    :param count: expected number of uvarints in the buffer
    :param buffer: bytes containing at least one uvarint encoded integer
    :param limit: maximum number of bytes to decode
    :return: list of decoded integers and total number of bytes read
    """
    integers: List[int] = []
    total: int = 0

    for _ in repeat(None, count):
        decoded: int
        bytes_read: int

        decoded, bytes_read = decode(buffer[total:], limit=limit)

        integers.append(decoded)
        total += bytes_read

    return Expected(integers, total)


class Slice(NamedTuple):
    """Decoded integers and remaining bytes."""
    integers: List[int]
    rest: bytes


def cut(count: int, buffer: bytes, limit: Number = LIMIT) -> Slice:
    """Slices the expected number of uvarints out of the given buffer.

    In addition to the list of decoded integers,
    a buffer containing the remaining bytes is returned.
    This allows the caller to easily process the rest of the buffer.

    Should the buffer not contain the expected amount of uvarints,
    ValueError will be raised.

    The buffer may be None or empty if the expected count is zero.
    The result will be an empty list and the unmodified input buffer.

    To prevent denial of service attacks, memory consumption is limited.
    By default, a limit of 9 bytes will be imposed on individual uvarints.
    The function will decode values in the interval [0, 2^63 - 1]
    and will raise OverflowError for bigger integers.
    This limit can be changed through the limit keyword argument.
    It can be removed entirely by passing math.inf.

    :param count: expected number of uvarints in the buffer
    :param buffer: bytes containing at least that many uvarint-encoded integers
    :param limit: maximum number of bytes to decode
    :return: list of decoded integers and remaining bytes
    """
    integers: List[int]
    bytes_read: int

    integers, bytes_read = expect(count, buffer, limit=limit)
    buffer = buffer[bytes_read:]

    return Slice(integers, buffer)
