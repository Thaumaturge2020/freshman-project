import base64
a = base64.b64encode('AlwaysBeta'.encode('utf-8'))
b = str(base64.b64decode(a), 'utf-8')
print(a,'\n',b)
