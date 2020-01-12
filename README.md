# uvarint

Unsigned variable-length integers. A type of [variable-length quantity].

# Usage

    import uvarint

    buffer = uvarint.encode(16384)                  # b'\x80\x80\x01'
    integer, bytes_read = uvarint.decode(buffer)    # 16384

    big = uvarint.encode(2 ** 63)
    uvarint.decode(big)              # Raises OverflowError; decoder limited to 9 bytes by default
    uvarint.decode(big, limit=16)    # Success; use math.inf for unlimited decoding

    multiple  = uvarint.encode(100)
    multiple += uvarint.encode(200)
    multiple += uvarint.encode(300)
    uvarint.expect(3, multiple).integers    # [100, 200, 300]
    uvarint.cut(0, multiple)                # Slice(integers=[], rest=b'd\xc8\x01\xac\x02')
    uvarint.cut(1, multiple)                # Slice(integers=[100], rest=b'\xc8\x01\xac\x02')
    uvarint.cut(2, multiple)                # Slice(integers=[100, 200], rest=b'\xac\x02')
    uvarint.cut(3, multiple)                # Slice(integers=[100, 200, 300], rest=b'')

# References

 - [Specification]

# License

This module is licensed under the MIT license.

[variable-length quantity]: https://en.wikipedia.org/wiki/Variable-length_quantity
[Specification]: https://github.com/multiformats/unsigned-varint
