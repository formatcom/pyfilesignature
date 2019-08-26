class BinarySignature:
    _format = None
    __signature = {
        b'\x42\x4D': 'BMP',
        b'\xFF\xD8': {
            'read': 1,
            b'\xFF': {
                'read': 1,
                b'\xE0': 'JPG',
                b'\xE1': 'JPG',
                b'\xE2': 'JPG',
                b'\xE3': 'JPG',
                b'\xE8': 'JPG',
            },
        },
        b'\x47\x49': {
            'read': 2,
            b'\x46\x38': 'GIF',
        },
        b'\x89\x50': {
            'read': 6,
            b'\x4E\x47\x0D\x0A\x1A\x0A': 'PNG',
        },
        b'\x25\x50': {
            'read': 2,
            b'\x44\x46': 'PDF',
        },
    }

    def __init__(self, data):
        self._data = data

    @property
    def format(self):
        if self._format:
            return self._format

        _format = None
        _start = 0
        _end = 2
        _break = False
        _signature = self.__signature
        while not _break:
            _format = _signature.get(
                self._data[_start:_end]
            )

            if not _format:
                return None
            elif isinstance(_format, str):
                _break = True
            else:
                _start = _end
                _end = _start+_format.get('read')
                _signature = _format
                del _signature['read']

        self._format = _format
        return _format

_list = ('linux.png', 'python.jpg', 'otherfile', 'empty', 'dummy.jpg', )

for name in _list:
    _file = None
    with open(name, 'rb') as f:
        _file = BinarySignature(f.read())
    print(name, _file.format)

