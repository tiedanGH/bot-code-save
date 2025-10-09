# video_no_dep_random.py
# 纯标准库、无依赖：生成随机内容的 AVI（RGB24 uncompressed video + 8-bit PCM mono audio）
# 输出 test.avi 并把 data:video/avi;base64,... 写入 test_avi_data_uri.txt

import struct, base64, math, os, random, time

def make_avi_random(filename="test.avi", duration=2.0, fps=8, width=120, height=80):
    # 随机种子（使用系统随机）
    seed_bytes = os.urandom(8)
    seed = int.from_bytes(seed_bytes, "big") ^ int(time.time_ns() & ((1<<63)-1))
    prng = random.Random(seed)

    frames = int(duration * fps)
    frame_size = width * height * 3  # RGB24
    audio_rate = 8000  # 8kHz
    audio_channels = 1
    audio_bits = 8
    audio_samples = int(duration * audio_rate)

    # 随机参数（在一次运行中固定）
    bg_color = (prng.randint(10, 60), prng.randint(10, 60), prng.randint(10, 60))
    num_rects = prng.randint(1, 3)
    rects = []
    for _ in range(num_rects):
        rw = prng.randint(10, min(40, width//2))
        rh = prng.randint(8, min(30, height//2))
        x0 = prng.randint(0, max(0, width - rw))
        y0 = prng.randint(0, max(0, height - rh))
        vx = prng.uniform(-60, 60)  # px/sec
        vy = prng.uniform(-40, 40)
        color = (prng.randint(120,255), prng.randint(40,220), prng.randint(40,220))
        rects.append((rw, rh, x0, y0, vx, vy, color))

    # 随机音频频率与调制
    base_freq = prng.uniform(220.0, 880.0)
    freq_mod = prng.uniform(-20.0, 20.0)

    # 用于每帧的简单伪随机噪声：LCG，基于全局 seed 和帧索引，效率高
    def frame_noise_generator(frame_index):
        # LCG params
        m = 2**32
        a = 1664525
        c = 1013904223
        s = (seed + frame_index*65537) & 0xFFFFFFFF
        def next_byte():
            nonlocal s
            s = (a * s + c) % m
            return (s >> 16) & 0xFF
        return next_byte

    # 生成一帧图像的 bytes (RGB24)
    def frame_bytes(i):
        buf = bytearray(frame_size)
        # 背景
        r,g,b = bg_color
        for p in range(0, frame_size, 3):
            buf[p:p+3] = bytes((r,g,b))
        # 放置每个矩形：位置随时间移动
        for (rw, rh, x0, y0, vx, vy, color) in rects:
            # 以秒为单位移动
            t = i / fps
            x = int((x0 + vx * t) % max(1, (width - rw + 1)))
            y = int((y0 + vy * t) % max(1, (height - rh + 1)))
            for yy in range(rh):
                row = y + yy
                if row < 0 or row >= height: continue
                base_off = row * width * 3
                for xx in range(rw):
                    col = x + xx
                    if col < 0 or col >= width: continue
                    off = base_off + col*3
                    buf[off:off+3] = bytes(color)
        # 添加每帧小噪声（亮度扰动），使用 LCG 产生，不耗太多 CPU
        nb = frame_noise_generator(i)
        # 每隔若干像素加一点随机值，避免每像素计算过多
        step = 7
        for yy in range(0, height, step):
            for xx in range(0, width, step):
                off = ((yy * width) + xx) * 3
                if off+2 < frame_size:
                    v = nb() % 24  # 0..23
                    # 给 R,G,B 都加一点（注意截断）
                    buf[off] = (buf[off] + v) & 0xFF
                    buf[off+1] = (buf[off+1] + (v//2)) & 0xFF
                    buf[off+2] = (buf[off+2] + (v//3)) & 0xFF
        return bytes(buf)

    # 音频：带小幅度频率抖动的正弦波
    def audio_bytes():
        data = bytearray()
        for n in range(audio_samples):
            t = n / audio_rate
            # 频率随时间微抖
            freq = base_freq + freq_mod * math.sin(2*math.pi*0.5*t)
            s = 0.45 * math.sin(2*math.pi*freq*t + 0.5*math.sin(2*math.pi*3*t))
            # 8-bit unsigned PCM (0..255)
            val = int((s + 0.5) * 255) & 0xFF
            data.append(val)
        return bytes(data)

    # 生成帧与音频
    avi_frames = [frame_bytes(i) for i in range(frames)]
    audiodata = audio_bytes()

    # === 以下为 AVI 头结构（参考前次修正版） ===
    dwMicroSecPerFrame = int(1_000_000 / fps)
    dwMaxBytesPerSec = max(1, frame_size * fps)
    dwPaddingGranularity = 0
    dwFlags = 0
    dwTotalFrames = frames
    dwInitialFrames = 0
    dwStreams = 2
    dwSuggestedBufferSize = frame_size
    dwWidth = width
    dwHeight = height

    avih_data = struct.pack("<14I",
                            dwMicroSecPerFrame,
                            dwMaxBytesPerSec,
                            dwPaddingGranularity,
                            dwFlags,
                            dwTotalFrames,
                            dwInitialFrames,
                            dwStreams,
                            dwSuggestedBufferSize,
                            dwWidth,
                            dwHeight,
                            0,0,0,0)
    avih_chunk = b"avih" + struct.pack("<I", len(avih_data)) + avih_data

    # video strh
    fccType_vid = b'vids'
    fccHandler_vid = b'DIB '
    dwFlags_vid = 0
    wPriority = 0
    wLanguage = 0
    dwInitialFrames = 0
    dwScale = 1
    dwRate = int(fps)
    dwStart = 0
    dwLength = frames
    dwSuggestedBufferSize_vid = frame_size
    dwQuality = 0xFFFFFFFF
    dwSampleSize_vid = 0
    rcLeft, rcTop, rcRight, rcBottom = 0, 0, width, height

    sv = b""
    sv += struct.pack("<4s", fccType_vid)
    sv += struct.pack("<4s", fccHandler_vid)
    sv += struct.pack("<I", dwFlags_vid)
    sv += struct.pack("<H", wPriority)
    sv += struct.pack("<H", wLanguage)
    sv += struct.pack("<I", dwInitialFrames)
    sv += struct.pack("<I", dwScale)
    sv += struct.pack("<I", dwRate)
    sv += struct.pack("<I", dwStart)
    sv += struct.pack("<I", dwLength)
    sv += struct.pack("<I", dwSuggestedBufferSize_vid)
    sv += struct.pack("<I", dwQuality)
    sv += struct.pack("<I", dwSampleSize_vid)
    sv += struct.pack("<i", rcLeft)
    sv += struct.pack("<i", rcTop)
    sv += struct.pack("<i", rcRight)
    sv += struct.pack("<i", rcBottom)
    strh_video = b"strh" + struct.pack("<I", len(sv)) + sv

    # video strf (BITMAPINFOHEADER)
    biSize = 40
    biWidth = width
    biHeight = height
    biPlanes = 1
    biBitCount = 24
    biCompression = 0
    biSizeImage = frame_size
    biXPelsPerMeter = 0
    biYPelsPerMeter = 0
    biClrUsed = 0
    biClrImportant = 0
    svf = struct.pack("<IIIHHIIIIII",
                      biSize, biWidth, biHeight, biPlanes, biBitCount,
                      biCompression, biSizeImage, biXPelsPerMeter, biYPelsPerMeter, biClrUsed, biClrImportant)
    strf_video = b"strf" + struct.pack("<I", len(svf)) + svf

    # audio strh
    fccType_aud = b'auds'
    fccHandler_aud = b'\x00\x00\x00\x00'
    dwFlags_aud = 0
    wPriority_aud = 0
    wLanguage_aud = 0
    dwInitialFrames_aud = 0
    audio_block_align = audio_channels * (audio_bits // 8)
    dwScale_aud = audio_block_align
    dwRate_aud = audio_rate * audio_block_align
    dwStart_aud = 0
    dwLength_aud = audio_samples
    dwSuggestedBufferSize_aud = len(audiodata)
    dwQuality_aud = 0xFFFFFFFF
    dwSampleSize_aud = audio_block_align

    sa = b""
    sa += struct.pack("<4s", fccType_aud)
    sa += struct.pack("<4s", fccHandler_aud)
    sa += struct.pack("<I", dwFlags_aud)
    sa += struct.pack("<H", wPriority_aud)
    sa += struct.pack("<H", wLanguage_aud)
    sa += struct.pack("<I", dwInitialFrames_aud)
    sa += struct.pack("<I", dwScale_aud)
    sa += struct.pack("<I", dwRate_aud)
    sa += struct.pack("<I", dwStart_aud)
    sa += struct.pack("<I", dwLength_aud)
    sa += struct.pack("<I", dwSuggestedBufferSize_aud)
    sa += struct.pack("<I", dwQuality_aud)
    sa += struct.pack("<I", dwSampleSize_aud)
    sa += struct.pack("<i", 0)
    sa += struct.pack("<i", 0)
    sa += struct.pack("<i", 0)
    sa += struct.pack("<i", 0)
    strh_audio = b"strh" + struct.pack("<I", len(sa)) + sa

    # audio strf (WAVEFORMATEX)
    wFormatTag = 1
    nChannels = audio_channels
    nSamplesPerSec = audio_rate
    nAvgBytesPerSec = audio_rate * audio_block_align
    nBlockAlign = audio_block_align
    wBitsPerSample = audio_bits
    wavfmt = struct.pack("<HHIIHH", wFormatTag, nChannels, nSamplesPerSec, nAvgBytesPerSec, nBlockAlign, wBitsPerSample)
    strf_audio = b"strf" + struct.pack("<I", len(wavfmt)) + wavfmt

    # LISTs
    strl_video_content = strh_video + strf_video
    strl_video = b"LIST" + struct.pack("<I4s", 4 + len(strl_video_content), b"strl") + strl_video_content
    strl_audio_content = strh_audio + strf_audio
    strl_audio = b"LIST" + struct.pack("<I4s", 4 + len(strl_audio_content), b"strl") + strl_audio_content
    hdrl_content = avih_chunk + strl_video + strl_audio
    hdrl = b"LIST" + struct.pack("<I4s", 4 + len(hdrl_content), b"hdrl") + hdrl_content

    # movi
    movi_data = bytearray()
    for f in avi_frames:
        movi_data += b"00db" + struct.pack("<I", len(f)) + f
        if len(f) % 2 == 1:
            movi_data += b'\x00'
    movi_data += b"01wb" + struct.pack("<I", len(audiodata)) + audiodata
    if len(audiodata) % 2 == 1:
        movi_data += b'\x00'
    movi = b"LIST" + struct.pack("<I4s", 4 + len(movi_data), b"movi") + bytes(movi_data)

    riff_data = hdrl + movi
    riff = b"RIFF" + struct.pack("<I4s", 4 + len(riff_data), b"AVI ") + riff_data

    with open(filename, "wb") as f:
        f.write(riff)

    # 返回文件名与本次随机种子（便于复现）
    return filename, seed, {
        "bg_color": bg_color,
        "num_rects": num_rects,
        "rects": rects,
        "base_freq": base_freq,
        "freq_mod": freq_mod,
        "frames": frames,
        "fps": fps,
        "width": width,
        "height": height
    }

if __name__ == "__main__":
    debug = True
    out, seed, info = make_avi_random("test.avi", duration=2.0, fps=8, width=120, height=80)
    with open(out, "rb") as f:
        data = f.read()
    uri = "data:video/avi;base64," + base64.b64encode(data).decode("ascii")
    with open("test_avi_data_uri.txt", "w", encoding="utf-8") as wf:
        wf.write(uri)
    
    if debug:
        print("已生成文件: {}".format(out))
        print("大小 (bytes): {}".format(len(data)))
        print("随机种子(seed):", seed)
        print("生成参数:", info)
        print("完整 data URI 已写入 test_avi_data_uri.txt")
        print("data URI 前200字符预览:\n", uri[:200])
    else:
        # 如需打印完整 URI，请取消下行注释（注意：会很长）
        print(uri)
