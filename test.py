import math
import unittest
from typing import List, Union, NamedTuple
from functools import reduce

import uvarint

class Representation(NamedTuple):
    """A map of an integer to its known correct uvarint representation."""
    integer: int
    uvarint: bytes

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
    all: List[Representation] = valid + [over_limit]

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

    def test_decode_limits(self) -> None:
        self.assertEqual(len(TestUvarint.upper_bound[1]), 9)

        decoded, encoded = TestUvarint.over_limit
        result, count = uvarint.decode(encoded, max=math.inf)

        self.assertEqual(len(encoded), 10)
        self.assertEqual(count, 10)
        self.assertEqual(result, decoded)

        with self.assertRaises(OverflowError):
            uvarint.decode(encoded)

    def test_expect(self) -> None:
        integers: List[int] = list(map(lambda x: x.integer, TestUvarint.valid))
        buffers: List[bytes] = list(map(lambda x: x.uvarint, TestUvarint.valid))
        buffer: bytes = reduce(lambda x, y: x + y, buffers)

        decoded, total = uvarint.expect(len(integers), buffer)

        self.assertEqual(decoded, integers)
        self.assertEqual(total, len(buffer))

    def test_expect_limits(self) -> None:
        integers: List[int] = list(map(lambda x: x.integer, TestUvarint.all))
        buffers: List[bytes] = list(map(lambda x: x.uvarint, TestUvarint.all))
        buffer: bytes = reduce(lambda x, y: x + y, buffers)

        decoded, total = uvarint.expect(len(integers), buffer, max=math.inf)

        self.assertEqual(decoded, integers)
        self.assertEqual(total, len(buffer))

        with self.assertRaises(OverflowError):
            uvarint.expect(len(integers), buffer)

if __name__ == '__main__':
    unittest.main()
