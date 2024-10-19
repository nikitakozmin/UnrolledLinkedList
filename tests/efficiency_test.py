"""This file should be placed along with the executable file."""

import matplotlib.pyplot as plt
from random import randint
from main import *
import time


# Node for LinkedList
class Node:
    def __init__(self, value = None, next = None):
        self.value = value
        self.next = next

class LinkedList:
    def __init__(self):
        self.first = None
        self.last = None
        self.length = 0

    def __str__(self):
        if self.first != None:
            current = self.first
            out = 'LinkedList [\n' +str(current.value) +'\n'
            while current.next != None:
                current = current.next
                out += str(current.value) + '\n'
            return out + ']'
        return 'LinkedList []'

    def clear(self):
        self.__init__()

    def __getitem__(self, index):
        cur = self.first
        while cur != None:
            if index == 0:
                return cur.value
            index -= 1
            cur = cur.next
        raise IndexError("linked list index out of range")
        

# add to end of LinkedList
    def add(self, x):
        self.length+=1
        if self.first == None:
            # self.first and self.last will point to the same memory location
            self.last = self.first = Node(x, None)
        else:
            # here, already to different ones, because the assignment occurred
            self.last.next = self.last = Node(x, None)

    def InsertNth(self,i,x):
        if self.first == None:
            self.last = self.first = Node(x, None)
            self.length += 1
            return
        if i == 0:
          self.first = Node(x,self.first)
          self.length += 1
          return
        curr=self.first
        count = 0
        while curr != None:
            count+=1
            if count == i:
              curr.next = Node(x,curr.next)
              self.length += 1
              if curr.next.next == None:
                self.last = curr.next
              break
            curr = curr.next

    def Del(self,i):
        if (self.first == None):
          return
        curr = self.first
        count = 0
        if i == 0:
          self.first = self.first.next
          self.length -= 1
          return
        while curr != None:
            if count == i:
              if curr.next == None:
                self.last = curr
              old.next = curr.next 
              self.length -= 1
              break
            old = curr  
            curr = curr.next
            count += 1


if __name__ == "__main__":
    set_n_elements = []
    ull_times = []
    list_times = []
    ll_times = []
    for n_elements in range(0, 10000, 1000):
        print(f"Check {n_elements} elements...")
        set_n_elements.append(n_elements)
        a = [randint(-1000, 1000) for _ in range(n_elements)]
        count = 1
        ull_local_times = []
        list_local_times = []
        ll_local_times = []
        for _ in range(count):
            ull = UnrolledLinkedList(a)
            start = time.time()
            for i in range(n_elements):
                ull.insert(0, a[i]) #len(ull)
            del ull
            end = time.time() - start
            ull_local_times.append(end)
            
            lst = list(a)
            start = time.time()
            for i in range(n_elements):
                lst.insert(0, a[i]) #len(lst)
            del lst
            end = time.time() - start
            list_local_times.append(end)
            
            ll = LinkedList()
            for i in range(n_elements):
                ll.InsertNth(i-1, a[i])
            start = time.time()
            for i in range(n_elements):
                ll.InsertNth(0, a[i]) #ll.length
            del ll
            end = time.time() - start
            ll_local_times.append(end)
        end = sum(ull_local_times) / count
        ull_times.append(end)
        end = sum(list_local_times) / count
        list_times.append(end)
        end = sum(ll_local_times) / count
        ll_times.append(end)
    plt.scatter(set_n_elements, ull_times)
    plt.plot(set_n_elements, ull_times, label='ull')
    plt.scatter(set_n_elements, list_times)
    plt.plot(set_n_elements, list_times, label='list')
    plt.scatter(set_n_elements, ll_times)
    plt.plot(set_n_elements, ll_times, label='linked list')
    plt.xlabel("n_elements")
    plt.ylabel("time, sec")
    plt.legend()
    plt.show()
