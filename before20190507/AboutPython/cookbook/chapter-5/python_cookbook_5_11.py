# 文件路径名的操作

# os.path模块中的函数来操作路径名

import  os
path='/Users/purplecity/a.txt'

# get the laste component of the path
print(os.path.basename(path))

# get directory name
print(os.path.dirname(path))

#join path components together
print(os.path.join('tmp','data',os.path.basename(path)))

#Expand the user's home directory
path='~/bitcoin/hehe.txt'
print(os.path.expanduser(path))

#split the file extension
print(os.path.splitext(path))

'''
a.txt
/Users/purplecity
tmp/data/a.txt
/Users/purplecity/bitcoin/hehe.txt
('~/bitcoin/hehe', '.txt')



文件目录操作复习
def gen_find(filepat,top):
    for path,dirlist,filelist in os.walk(top):
        for name in fnmatch.filter(filelist,filepat):
            yield  os.path.join(path,name)


#找到top目录下所有符合filepat匹配模式的文件的文件路径
#os.walk() 方法用于通过在目录树中游走输出在目录中的文件名，向上或者向下。
# os.walk(top[, topdown=True[, onerror=None[, followlinks=False]]])

top -- 是你所要遍历的目录的地址, 返回的是一个三元组(root,dirs,files)。
root 所指的是当前正在遍历的这个文件夹的本身的地址
dirs 是一个 list ，内容是该文件夹中所有的目录的名字(不包括子目录)
files 同样是 list , 内容是该文件夹中所有的文件(不包括子目录)

'''