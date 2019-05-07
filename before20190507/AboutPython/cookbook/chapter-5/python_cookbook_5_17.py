# 将字节写入文本文件

'''

#想从二进制模式的文件中读取或写入文本数据，必须确保要进行解码和编码操作
with open('/Users/purplecity/a.txt','rb') as f:
    data=f.read(16)
    text=data.decode('utf-8')

with open('/Users/purplecity/a.txt','wb') as f:
    text='helloworld'
    f.write(text.encode('utf-8'))

'''


#将字节数据直接写入文件的缓冲区即可
import sys
print(sys.stdout.write(b'hello\n'))

print(sys.stdout.buffer.write(b'hello\n'))

# 然后能够通过读取文本文件的 buffer 属性来读取二进制数据。
# 文本文件是通过在一个拥有缓冲的二进制模式文件上增加一个Unicode编码/解码层来创建。 buffer 属性指向对应的底层文件。如果你直接访问它的话就会绕过文本编码/解码层。




