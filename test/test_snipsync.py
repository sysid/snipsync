from snipsync.io import read_ultisnips


def test_read_ultisnips(ultisnips_file):
    data = read_ultisnips(ultisnips_file)
    print(data)