//
// Created by purplecity on 2019-07-22.
//

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