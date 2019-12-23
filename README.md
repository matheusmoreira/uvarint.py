# uvarint

Unsigned variable-length integers.

# Usage

    import uvarint

    buffer = uvarint.encode(16384)                  # b'\x80\x80\x01'
    integer, bytes_read = uvarint.decode(buffer)    # 16384

# License

This module is licensed under the MIT license.
