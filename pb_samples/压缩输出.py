import gzip, base64

def gzip_text(text):
    data = text.encode('utf-8')
    cdata = gzip.compress(data)
    bdata = base64.encodebytes(cdata)
    btext = bdata.decode('utf-8')
    return btext

def ungzip_text(btext):
    bdata = btext.encode('utf-8')
    cdata = base64.decodebytes(bdata)
    data = gzip.decompress(cdata)
    text = data.decode('utf-8')
    return text

s="这是一串字符串这是一串字符串这是一串字符串这是一串字符串这是一串字符串"
btext = gzip_text(s)
print(btext)
text = ungzip_text(btext)
print(text)
