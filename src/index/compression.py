import struct

def vb_encode_number(n):
    bytes_list = []
    while True:
        bytes_list.insert(0, n % 128)
        if n < 128:
            break
        n //= 128
    bytes_list[-1] += 128
    return bytes(bytes_list)


def vb_encode_list(numbers):
    return b''.join(vb_encode_number(n) for n in numbers)


def vb_decode_stream(bytestream):
    numbers = []
    n = 0
    for b in bytestream:
        if b < 128:
            n = 128*n + b
        else:
            n = 128*n + (b - 128)
            numbers.append(n)
            n = 0
    return numbers


def gap_encode_list(postings):
    if not postings:
        return []
    gaps = [postings[0]]
    for i in range(1, len(postings)):
        gaps.append(postings[i] - postings[i-1])
    return gaps


def gap_decode_list(gaps):
    if not gaps:
        return []
    postings = [gaps[0]]
    for g in gaps[1:]:
        postings.append(postings[-1] + g)
    return postings