# uvarint

Unsigned variable-length integers.

# Usage

    import uvarint

    x = uvarint.encode(16384) # b'\x80\x80\x01'
    y = uvarint.decode(x)     # 16384

# License

This module is licensed under the MIT license.
