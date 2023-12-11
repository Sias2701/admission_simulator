from secrets import token_hex
source = open('Major_code.csv').readlines()
files = open('new.csv','r').read()
for l in source:
    val = l.split(', ')[1].strip()
    src = ", " + val + ","
    dst = ", '" + val + "', '"
    files = files.replace(src, dst)
open('new1.csv','w').write(files)