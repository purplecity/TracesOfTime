#在一个固定长度记录或者数据块的集合上迭代，而不是在一个文件中一行一行的迭代。


# 又遇到iter这个函数了。第二个参数是结尾符

from functools import partial

RECORD_SIZE=32
with open('somefile.data','rb') as f:
    records=iter(partial(f.read,RECORD_SIZE),b'')
    for r in records:
        print(r)

'''
def iter(source, sentinel=None):  # known special case of iter
    """
    iter(iterable) -> iterator
    iter(callable, sentinel) -> iterator

    Get an iterator from an object.  In the first form, the argument must
    supply its own iterator, or be a sequence.
    In the second form, the callable is called until it returns the sentinel.
    """

iter() 函数有一个鲜为人知的特性就是，如果你给它传递一个可调用对象和一个标记值，它会创建一个迭代器。 这个迭代器会一直调用传入的可调用对象直到它返回标记值为止，这时候迭代终止。

在例子中， functools.partial 用来创建一个每次被调用时从文件中读取固定数目字节的可调用对象。 标记值 b'' 就是当到达文件结尾时的返回值。

最后再提一点，上面的例子中的文件时以二进制模式打开的。 如果是读取固定大小的记录，这通常是最普遍的情况。 而对于文本文件，一行一行的读取(默认的迭代行为)更普遍点


class partial(Generic[_T]):
    func = ...  # type: Callable[..., _T]
    args = ...  # type: Tuple[Any, ...]
    keywords = ...  # type: Dict[str, Any]
    def __init__(self, func: Callable[..., _T], *args: Any, **kwargs: Any) -> None: ...
    def __call__(self, *args: Any, **kwargs: Any) -> _T: ...



'''