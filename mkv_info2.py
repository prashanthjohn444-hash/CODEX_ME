#!/usr/bin/env python3
"""Parse MKV EBML header to extract video dimensions and duration."""
import sys
import struct

def read_ebml_int(data, pos):
    """Read EBML variable-length integer. Returns (value, new_pos)."""
    first = data[pos]
    # Determine size of the length prefix (1-8 bytes)
    size = 1
    for i in range(7, -1, -1):
        if first & (1 << i):
            size = 8 - i
            break
    # Mask out the size bits to get the value
    value = first & ((1 << (8 - size)) - 1)
    for i in range(1, size):
        value = (value << 8) | data[pos + i]
    return value, pos + size

def read_element(data, pos):
    """Read an EBML element. Returns (element_id, data_size, data_start, next_pos)."""
    element_id, pos = read_ebml_int(data, pos)
    data_size, pos = read_ebml_int(data, pos)
    return element_id, data_size, pos, pos + data_size

def parse_mkv(path):
    with open(path, 'rb') as f:
        data = f.read()
    
    if len(data) < 4:
        return None, None, 0, "file too small"
    
    # Check EBML magic
    if data[0:4] != b'\x1a\x45\xdf\xa3':
        return None, None, len(data), "not EBML"
    
    width = height = None
    duration_ns = None
    
    pos = 0
    while pos < len(data):
        elem_id, data_size, data_start, next_pos = read_element(data, pos)
        
        if elem_id == 0x18538067:  # Segment
            # Parse within segment
            seg_pos = data_start
            seg_end = data_start + data_size
            while seg_pos < seg_end:
                s_id, s_size, s_data_start, s_next = read_element(data, seg_pos)
                
                if s_id == 0x2A6D7D6B:  # Duration (in SegmentInfo)
                    # Read duration as float (8 bytes) or uint
                    if s_size >= 8:
                        duration_ns = struct.unpack('>d', data[s_data_start:s_data_start+8])[0]
                    elif s_size == 4:
                        duration_ns = struct.unpack('>I', data[s_data_start:s_data_start+4])[0]
                    else:
                        duration_ns = int.from_bytes(data[s_data_start:s_data_start+s_size], 'big')
                
                if s_id == 0x1654AE6B:  # Tracks
                    tr_pos = s_data_start
                    tr_end = s_data_start + s_size
                    while tr_pos < tr_end:
                        t_id, t_size, t_data_start, t_next = read_element(data, tr_pos)
                        if t_id == 0xAE:  # TrackEntry
                            te_pos = t_data_start
                            te_end = t_data_start + t_size
                            while te_pos < te_end:
                                v_id, v_size, v_data_start, v_next = read_element(data, te_pos)
                                if v_id == 0xE0:  # Video
                                    vid_pos = v_data_start
                                    vid_end = v_data_start + v_size
                                    while vid_pos < vid_end:
                                        pw_id, pw_size, pw_data_start, pw_next = read_element(data, vid_pos)
                                        if pw_id == 0x54B0:  # PixelWidth
                                            width = int.from_bytes(data[pw_data_start:pw_data_start+pw_size], 'big')
                                        elif pw_id == 0x54BA:  # PixelHeight
                                            height = int.from_bytes(data[pw_data_start:pw_data_start+pw_size], 'big')
                                        vid_pos = pw_next
                                te_pos = v_next
                        tr_pos = t_next
                
                seg_pos = s_next
        
        pos = next_pos
    
    duration_s = duration_ns / 1e9 if duration_ns else None
    return (width, height), duration_s, len(data), "ok"

if __name__ == "__main__":
    import glob
    base = r"C:\Users\lms-work\Documents\Python\youtube-course\production\day-01\screen\v2\captures"
    files = sorted(glob.glob(base + "/section-*-obs.mkv"))
    for f in files:
        (w, h), dur, sz, status = parse_mkv(f)
        dur_str = f"{dur:.2f}s" if dur else "N/A"
        dim_str = f"{w}x{h}" if w and h else "N/A"
        print(f"{f.split('\\')[-1]}: {dim_str}, {dur_str}, {sz} bytes, {status}")
