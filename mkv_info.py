#!/usr/bin/env python3
"""Parse MKV EBML header to extract video dimensions."""
import sys

def read_ebml_int(data, pos):
    first = data[pos]
    size = 1
    for i in range(7, -1, -1):
        if first & (1 << i):
            size = 8 - i
            break
    value = first & ((1 << (8 - size)) - 1)
    for i in range(1, size):
        value = (value << 8) | data[pos + i]
    return value, pos + size, size

def read_ebml_element(data, pos):
    element_id, pos, _ = read_ebml_int(data, pos)
    data_size, pos, size_len = read_ebml_int(data, pos)
    return element_id, data_size, pos, pos + data_size

def find_video_dims(path):
    with open(path, 'rb') as f:
        data = f.read()
    pos = 0
    width = height = None
    while pos < len(data):
        elem_id, data_size, data_start, next_pos = read_ebml_element(data, pos)
        if elem_id == 0x1654AE6B:  # Tracks
            track_pos = data_start
            track_end = data_start + data_size
            while track_pos < track_end:
                t_id, t_size, t_data_start, t_next = read_ebml_element(data, track_pos)
                if t_id == 0xAE:  # TrackEntry
                    te_pos = t_data_start
                    te_end = t_data_start + t_size
                    while te_pos < te_end:
                        v_id, v_size, v_data_start, v_next = read_ebml_element(data, te_pos)
                        if v_id == 0xE0:  # Video
                            vid_pos = v_data_start
                            vid_end = v_data_start + v_size
                            while vid_pos < vid_end:
                                pw_id, pw_size, pw_data_start, pw_next = read_ebml_element(data, vid_pos)
                                if pw_id == 0x54B0:  # PixelWidth
                                    width = int.from_bytes(data[pw_data_start:pw_data_start+pw_size], 'big')
                                elif pw_id == 0x54BA:  # PixelHeight
                                    height = int.from_bytes(data[pw_data_start:pw_data_start+pw_size], 'big')
                                vid_pos = pw_next
                        te_pos = v_next
                track_pos = t_next
        pos = next_pos
    return width, height, len(data)

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else r"C:\Users\lms-work\Documents\Python\youtube-course\production\day-01\screen\v2\captures\2026-10-17 21-45-23.mkv"
    w, h, sz = find_video_dims(path)
    print(f"Dimensions: {w}x{h}")
    print(f"File size: {sz} bytes")
    print(f"Expected: 1920x1080 -> {'MATCH' if (w == 1920 and h == 1080) else 'MISMATCH'}")
