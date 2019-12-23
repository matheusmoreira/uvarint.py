# uvarint

Unsigned variable-length integers.

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

# References

 - [Specification]

# License

This module is licensed under the MIT license.

[Specification]: https://github.com/multiformats/unsigned-varint
