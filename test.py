import math
import unittest
from typing import List, NamedTuple
from functools import reduce
from operator import add as concatenate

import uvarint

class Representation(NamedTuple):
    """A map of an integer to its known correct uvarint representation."""
    integer: int
    uvarint: bytes

def to_integer(r: Representation) -> int:
    return r.integer

def to_uvarint(r: Representation) -> bytes:
    return r.uvarint

class TestUvarint(unittest.TestCase):

    # Example values from the multiformats specification README
    # https://github.com/multiformats/unsigned-varint/blob/master/README.md
    examples: List[Representation] = [
        Representation(1,     bytes([0b0000_0001])),
        Representation(127,   bytes([0b0111_1111])),
        Representation(128,   bytes([0b1000_0000, 0b0000_0001])),
        Representation(255,   bytes([0b1111_1111, 0b0000_0001])),
        Representation(300,   bytes([0b1010_1100, 0b0000_0010])),
        Representation(16384, bytes([0b1000_0000, 0b1000_0000, 0b0000_0001]))
    ]

    more: List[Representation] = [
        Representation(64, bytes([0b0100_0000])),
        Representation(300, bytes([0b1010_1100, 0b0000_0010]))
    ]

    upper_bound: Representation = Representation(2 ** 63 - 1, bytes([0b1111_1111] * 8 + [0b0111_1111]))
    over_limit: Representation = Representation(2 ** 63, bytes([0b1000_0000] * 9 + [0b0000_0001]))

    valid: List[Representation] = examples + more + [upper_bound]
    all: List[Representation] = valid + [over_limit, over_limit]
    one: Representation = all[0]

    valid_integers: List[int] = list(map(to_integer, valid))
    valid_buffers: List[bytes] = list(map(to_uvarint, valid))

    all_integers: List[int] = list(map(to_integer, all))
    all_buffers: List[bytes] = list(map(to_uvarint, all))

    valid_buffer: bytes = reduce(concatenate, valid_buffers)
    all_buffer: bytes = reduce(concatenate, all_buffers)

    def test_encode(self) -> None:
        decoded: int
        encoded: bytes

        for (decoded, encoded) in TestUvarint.all:
            self.assertEqual(uvarint.encode(decoded), encoded)

    def test_decode(self) -> None:
        decoded: int
        encoded: bytes

        for (decoded, encoded) in TestUvarint.valid:
            result: int
            count: int

            result, count = uvarint.decode(encoded)
            self.assertEqual(result, decoded)
            self.assertEqual(count, len(encoded))

    def test_decode_empty_buffer(self) -> None:
        with self.assertRaises(ValueError):
            uvarint.decode(b'')

    def test_decode_limits(self) -> None:
        self.assertEqual(len(TestUvarint.upper_bound[1]), 9)

        decoded, encoded = TestUvarint.over_limit
        result, count = uvarint.decode(encoded, limit=math.inf)

        self.assertEqual(len(encoded), 10)
        self.assertEqual(count, 10)
        self.assertEqual(result, decoded)

        with self.assertRaises(OverflowError):
            uvarint.decode(encoded)

    def test_expect(self) -> None:
        integers: List[int] = TestUvarint.valid_integers
        buffer: bytes = TestUvarint.valid_buffer

        decoded, total = uvarint.expect(len(integers), buffer)

        self.assertEqual(decoded, integers)
        self.assertEqual(total, len(buffer))

    def test_expect_limits(self) -> None:
        integers: List[int] = TestUvarint.all_integers
        buffer: bytes = TestUvarint.all_buffer

        decoded, total = uvarint.expect(len(integers), buffer, limit=math.inf)

        self.assertEqual(decoded, integers)
        self.assertEqual(total, len(buffer))

        with self.assertRaises(OverflowError):
            uvarint.expect(len(integers), buffer)

    def test_expect_empty_buffer(self) -> None:
        with self.assertRaises(ValueError):
            uvarint.expect(1, b'')

    def test_expect_zero(self) -> None:
        integers: List[int]
        bytes_read: int

        integers, bytes_read = uvarint.expect(0, TestUvarint.one.uvarint)

        self.assertEqual(integers, [])
        self.assertEqual(bytes_read, 0)

    def test_expect_zero_with_empty_buffer(self) -> None:
        integers: List[int]
        bytes_read: int

        integers, bytes_read = uvarint.expect(0, b'')

        self.assertEqual(integers, [])
        self.assertEqual(bytes_read, 0)

    def test_expect_more_than_buffer_contains(self) -> None:
        with self.assertRaises(ValueError):
            uvarint.expect(2, TestUvarint.one.uvarint)

    def test_cut(self) -> None:
        integers: List[int] = TestUvarint.valid_integers
        buffers: List[bytes] = TestUvarint.valid_buffers
        buffer: bytes = TestUvarint.valid_buffer

        decoded, total = uvarint.cut(len(integers) - 1, buffer)

        self.assertEqual(decoded, integers[:-1])
        self.assertEqual(total, buffers[-1])

    def test_cut_limits(self) -> None:
        integers: List[int] = TestUvarint.all_integers
        buffers: List[bytes] = TestUvarint.all_buffers
        buffer: bytes = TestUvarint.all_buffer

        decoded, total = uvarint.cut(len(integers) - 1, buffer, limit=math.inf)

        self.assertEqual(decoded, integers[:-1])
        self.assertEqual(total, buffers[-1])

        with self.assertRaises(OverflowError):
            uvarint.cut(len(integers) - 1, buffer)

    def test_cut_empty_buffer(self) -> None:
        with self.assertRaises(ValueError):
            uvarint.cut(1, b'')

    def test_cut_zero(self) -> None:
        one: bytes = TestUvarint.one.uvarint
        integers: List[int]
        rest: bytes

        integers, rest = uvarint.cut(0, one)

        self.assertEqual(integers, [])
        self.assertEqual(rest, one)

    def test_cut_zero_with_empty_buffer(self) -> None:
        integers: List[int]
        rest: bytes

        integers, rest = uvarint.cut(0, b'')

        self.assertEqual(integers, [])
        self.assertEqual(rest, b'')

    def test_cut_more_than_buffer_contains(self) -> None:
        with self.assertRaises(ValueError):
            uvarint.cut(2, TestUvarint.one.uvarint)


if __name__ == '__main__':
    unittest.main()
