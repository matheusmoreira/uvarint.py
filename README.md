# uvarint

Unsigned variable-length integers.

# Usage

    import uvarint

    buffer = uvarint.encode(16384)                  # b'\x80\x80\x01'
    integer, bytes_read = uvarint.decode(buffer)    # 16384

    big = uvarint.encode(2 ** 63)
    uvarint.decode(big)                 # Raises OverflowError; decoder limited to 9 bytes by default
    uvarint.decode(big, max=16)         # Success; use math.inf for unlimited decoding

# License

This module is licensed under the MIT license.
