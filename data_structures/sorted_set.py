from typing import Iterator, TypeVar, Generic
import random
import bisect

T = TypeVar("T")


class SortedSet(Generic[T]):
    __data : list[T]
    __sorting_function : callable[[T], any]

    def __init__(self, sort_key: callable[[T], any]):

        self.__data = []
        self.__sorting_function = sort_key




    def contains(self, elem: T) -> bool:
        return elem in self.__data
    
    def get_random(self):
        return random.choice(self.__data)
    
    def size(self):
        return len(self.__data)
    
    def add_sorted(self, elem: T):
        index : int = bisect.bisect_left(self.__data, elem, key = self.__sorting_function)
        if index != len(self.__data) and self.__data[index] == elem:
            return
        bisect.insort(self.__data, elem, key = self.__sorting_function)

    def remove(self, elem: T):
        self.__data.remove(elem)

    def remove_idx(self, idx: int):
        self.__data.pop(idx)

    
    def clear(self):
        self.__data.clear

    def get_idx(self, elem : T) -> int:
        return self.__data.index(elem)
    
    def get(self, idx: int) -> T:
        return self.__data[idx]
    
    def get_last(self) -> T:
        return self.__data[-1]

    def __iter__(self) -> Iterator[T]:
        return iter(self.__data)
    
    def __getitem__(self, index) -> T:
        return self.__data[index]

    def __setitem__(self, index, value):
        self.__data[index] = value


    @property 
    def data(self) -> list[T]:
        return self.__data
    
    @data.setter
    def data(self, data: list[T]):
        self.__data = data

    @property
    def sorting_function(self) -> callable[[T], any]:
        return self.__sorting_function
    
    @sorting_function.setter
    def sorting_function(self,sorting_function : callable[[T], any]):
        self.__sorting_function = sorting_function



