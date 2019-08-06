# ...
> Llvm clang ： clang是llvm的一个子项目是llvm编译器的前端 前后端解耦的 gcc/g++： gcc 前后端没解耦 gdb对应于lldb  ./configure 生成makefile。make按照makefile编译文件  make install 也是按照makefile中的innstall去安装文件   构建何必这么麻烦 — cmake 和bazel解决问题。ide对cmake支持还挺好

# About C

## 内存分区
### 数据类型
> 数据类型:"类型"是对数据的抽象 类型相同的数据有相同的表示形式、存储格式以及相关的操作  程序中使用的所有数据都必定属于某一种数据类型 数据类型可理解为创建变量的模具：是固定内存大小的别名。数据类型的作用：编译器预算对象（变量）分配的内存空间大小。数据类型只是模具，编译器并没有分配空间，只有根据类型（模具）创建变量（实物），编译器才会分配空间。

```C

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void) {
    int a; //告诉编译器，分配 4个字节
    int b[10]; //告诉编译器，分配 4 * 10 个字节

    //类型的本质：固定内存块大小别名，可以通过 sizeof()测试字节大小
    printf("sizeof(a)=%lu,sizeof(b)=%lu\n", sizeof(a), sizeof(b)); //sizeof 是lu类型所以 lu


    //打印地址
    //数组名字，数组首元素地址，数组首地址
    printf("b:%lu,&b:%lu\n",b,&b);
    printf("b+1:%lu， &b+1:%lu\n", b + 1, &b + 1);
    //b, &b的数组类型不一样
    //b， 数组首元素地址， 一个元素4字节，+1跳一个元素长度， +4
    //&b, 整个数组的首地址，一个数组4*10  = 40字节，+1调整个数组长度， +40

    //都是打印指针变量本身 由于32位指针变量4字节 64位8字节 所以采用lu8字节
    //可以看到相差的值确实是相差4和40

    //sizeof是操作符，不是函数；sizeof测量的实体大小为编译期间就已确定。

    //起别名
    typedef unsigned int u32;
    u32 t; //等价于 unsigned int t
    struct MyStruct
    {
        int a;
        int b;
    };

    //C语言定义结构体变量，一定要加上struct关键字
    struct MyStruct m1;
    //MyStruct m2; //err

    //struct MyStruct2起别名为TMP
    typedef struct MyStruct2
    {
        int a;
        int b;
    }TMP;


    TMP m3;
    struct MyStruct2 m4;
    return 0;
}

```


```C

//void数据类型

//函数参数为空 定义函数时  可以用void修饰 
int func(void) {

}
//当函数没有返回值时，用void修饰
void fun(void) {

}

//不能定义void类型的普通变量
void a; //err 无法确定类型 不同类型分配空间不一样

//可以定义void* 指针变量,这种指针变量称为万能指针, void* 可以指向任何类型的数据
void *p = NULL;

char ch = 'c';
p = (void*) &ch;

printf("*p=%c\n),*((char*)p));
int a = 10;
p = (void*) a;
printf("*p=%d\n",*((int*)p));

//void* 常用于数据类型的封装
void* memcpy(void* dest, const void* src, size_t len);
void* memset(void* buffer,int c, size_t num);


```

> 数据类型本质是固定内存大小的别名，是个模具，C语言规定：通过数据类型定义变量。数据类型大小计算（sizeof）可以给已存在的数据类型起别名typedef 数据类型的封装（void 万能类型）

### 变量本质
> 既能读又能写的内存对象 称为变量;若一旦初始化后不能修改的对象则称为常量
> 变量的定义形式  类型 标识符, 标识符...
```c
int x;
int a,b,c;
double a,b,c;
```
>  变量的本质:一段连续内存空间的别名
1. 程序通过变量来申请和命名内存空间 int a = 0;
2. 通过变量名访问内存空间
3. 不是向变量读写数据,而是向变量所代表的内存空间读写数据

```c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int main(void)
{
	//变量本质：一段连续内存空间别名
	//变量相当于门牌号，内存相当于房间
	int a;
	int *p;

	//直接赋值
	a = 10;
	printf("a = %d\n", a);

	//间接赋值
	p = &a;
	printf("p = %d\n", p);

	*p = 22;
	printf("*p = %d, a = %d\n", *p, a);

	return 0;
}
```

### 分区模型
> C代码编译成可执行程序经过4步：
1. 预处理：宏定义展开、头文件展开、条件编译，这里并不会检查语法
2. 编译：检查语法，将预处理后文件编译生成汇编文件
3. 汇编：将汇编文件生成目标文件(二进制文件)
4. 链接：将目标文件链接为可执行程序


