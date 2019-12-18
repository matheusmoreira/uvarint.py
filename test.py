import math
import unittest
from typing import List, Union, Tuple

import uvarint

class TestUvarint(unittest.TestCase):

    # Example values from the multiformats specification README
    # https://github.com/multiformats/unsigned-varint/blob/master/README.md
    examples: List[Tuple[int, bytes]] = [
        (1,     bytes([0b0000_0001])),
        (127,   bytes([0b0111_1111])),
        (128,   bytes([0b1000_0000, 0b0000_0001])),
        (255,   bytes([0b1111_1111, 0b0000_0001])),
        (300,   bytes([0b1010_1100, 0b0000_0010])),
        (16384, bytes([0b1000_0000, 0b1000_0000, 0b0000_0001]))
    ]

    upper_bound: Tuple[int, bytes] = (2 ** 63 - 1, bytes([0b1111_1111] * 8 + [0b0111_1111]))
    over_limit: Tuple[int, bytes] = (2 ** 63, bytes([0b1000_0000] * 9 + [0b0000_0001]))

    values: List[Tuple[int, bytes]] = examples + [upper_bound]
    all: List[Tuple[int, bytes]] = values + [over_limit]

    multiple: Tuple[Tuple[int, int], bytes] = (
        (64, 300), bytes([0b0100_0000, 0b1010_1100, 0b0000_0010])
    )

    def test_encoding(self) -> None:
        decoded: int
        encoded: bytes

        for (decoded, encoded) in TestUvarint.all:
            self.assertEqual(uvarint.encode(decoded), encoded)

    def test_decoding(self) -> None:
        decoded: int
        encoded: bytes

        for (decoded, encoded) in TestUvarint.values:
            result: int
            count: int

            result, count = uvarint.decode(encoded)
            self.assertEqual(result, decoded)
            self.assertEqual(count, len(encoded))

    def test_limits(self) -> None:
        self.assertEqual(len(TestUvarint.upper_bound[1]), 9)

        decoded, encoded = TestUvarint.over_limit
        result, count = uvarint.decode(encoded, max=math.inf)

        self.assertEqual(len(encoded), 10)
        self.assertEqual(count, 10)
        self.assertEqual(result, decoded)

        with self.assertRaises(OverflowError):
            uvarint.decode(encoded)

    def test_decode_multiple(self) -> None:
        first: int
        second: int
        buffer: bytes

        first_result: int
        second_result: int
        count: int

        (first, second), buffer = TestUvarint.multiple
        first_result, count = uvarint.decode(buffer)

        self.assertEqual(first, first_result)
        self.assertEqual(count, 1)

        second_result, count = uvarint.decode(buffer[count:])

        self.assertEqual(second, second_result)
        self.assertEqual(count, 2)


if __name__ == '__main__':
    unittest.main()
