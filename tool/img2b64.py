import base64
 
with open(r"path_2_icon.ico", 'rb') as f:
    base64_data = base64.b64encode(f.read())
    data = base64_data.decode()
    print(data)
    #with open('icon.txt', 'wt') as f:
    #    f.write(data)
