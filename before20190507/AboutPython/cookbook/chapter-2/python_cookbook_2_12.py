# str.transhlate的使用
s = 'pýtĥöñ\fis\tawesome\r\n'
remap={
    ord('\t'):' ',
    ord('\f'):' ',
    ord('\r'):None
}

print(s.translate(remap))

intab = "aeiou"
outtab = "12345"
trantab = str.maketrans(intab, outtab)  # 制作翻译表

str = "this is string example....wow!!!"
print(str.translate(trantab))

'''
pýtĥöñ is awesome

th3s 3s str3ng 2x1mpl2....w4w!!!
'''