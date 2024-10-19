def filter_none(iterable):
    return filter(lambda data: data is not None, iterable)


class UnrolledLinkedList:
    class Node(list):
        def __init__(self, iterable) -> None:
            self.data = list(iterable)
            self.next = None
        
        def __len__(self) -> int:
            return len(list(filter_none(self.data)))

        def __str__(self) -> str:
            return " ".join(map(str, filter_none(self.data)))
    
    def calculate_optimal_node_size(num_elements, element_bytes=4, min_cache_line_size=64) -> int:
        sum_bytes = num_elements * element_bytes
        cache_lines_needed = -(-sum_bytes // min_cache_line_size)
        optimal_node_size = cache_lines_needed+1
        return optimal_node_size
    
    def __init__(self, container=[], n_array=0, node_size_counter=calculate_optimal_node_size) -> None:
        self.node_size_counter = node_size_counter
        self.__len = len(container)
        if n_array <= 0:
            n_array = node_size_counter(len(self))
        self.n_array = n_array
        if len(self) == 0:
            self.num_nodes = 1
        else:
            self.num_nodes = -(-len(self) // n_array)
        i = 0
        self.head = self.Node([container[i*n_array + j] if i*n_array+j < len(self) else None for j in range(n_array)])
        cur = self.head
        for i in range(1, self.num_nodes):
            cur.next = self.Node([container[i*n_array + j] if i*n_array+j < len(self) else None for j in range(n_array)])
            cur = cur.next
    
    def __len__(self) -> int:
        return self.__len

    def __str__(self) -> str:
        rslt_str = ""
        cur = self.head
        i = 0
        while cur != None:
            rslt_str = f"{rslt_str}Node {i}: {str(cur)}\n"
            cur = cur.next
            i += 1
        return rslt_str

    def __bool__(self):
        return False if len(self.head)==0 and self.head.next==None else True
    
    def __getitem__(self, index):
        if index < 0 or index >= len(self):
            raise IndexError("ull index out of range")
        cur = self.head
        for _ in range(self.num_nodes):
            dif = index - len(cur)
            if dif >= 0:
                index = dif
                cur = cur.next
            else:
                return cur.data[index]

    def __delitem__(self, index):
        if index < 0 or index >= len(self):
            raise IndexError("ull index out of range")
        cur = self.head
        for _ in range(self.num_nodes):
            dif = index - len(cur)
            if dif >= 0:
                index = dif
                cur = cur.next
            else:
                del cur.data[index]
                cur.data.append(None)
                self.__len -= 1
                new_n_array = self.node_size_counter(len(self))
                if new_n_array != self.n_array:
                    self.balancing(new_n_array)
                break
    
    def index(self, value):
        index = 0
        cur = self.head
        for _ in range(self.num_nodes):
            if value in cur.data:
                local_index = cur.data.index(value)
                cur = self.head
                return index+local_index
            index += len(cur)
            cur = cur.next
        raise ValueError(f"{value} is not in ull")

    def container_to_cur_and_new_nodes(self, container, cur: Node):
        container = list(container)
        if len(container) <= self.n_array:
            cur.data = container + [None]*(self.n_array-len(container))
            self.__len += len(cur)
            return None
        len_container_for_two_nodes = min(self.n_array*2, len(container))
        new = self.Node([None]*self.n_array)
        new.next = cur.next
        cur.next = new
        self.num_nodes += 1
        cur.data = container[:len_container_for_two_nodes//2]
        self.__len += len(cur)
        cur.data += [None]*(self.n_array-len_container_for_two_nodes//2)
        self.container_to_cur_and_new_nodes(container[len_container_for_two_nodes//2:], new)
    
    def insert(self, index, value):
        if index < 0 or index > len(self):
            raise IndexError("ull index out of range")
        cur = self.head
        for _ in range(self.num_nodes):
            dif = index - len(cur)
            if dif > 0:
                index = dif
                cur = cur.next
            else:
                if len(cur) < self.n_array:
                    del cur.data[-1]
                    cur.data.insert(index, value)
                    self.__len += 1
                else:
                    whole_array = cur.data.copy()
                    whole_array.insert(index, value)
                    self.__len -= len(cur)
                    self.container_to_cur_and_new_nodes(filter_none(whole_array), cur)
                new_n_array = self.node_size_counter(len(self))
                if new_n_array != self.n_array:
                    self.balancing(new_n_array)
                return None
        return None

    def balancing(self, new_n_array):
        if len(self.head) == 0:
            del_cur = self.head
            self.head = del_cur.next
            del del_cur
        if new_n_array == self.n_array:
            return None
        self.n_array = new_n_array
        cur = self.head
        while cur != None:
            if cur.next != None and len(cur.next) == 0:
                del_cur = cur.next
                cur.next = del_cur.next
                del del_cur
                self.num_nodes -= 1
            whole_array = cur.data.copy()
            self.__len -= len(cur)
            self.container_to_cur_and_new_nodes(filter_none(whole_array), cur)
            cur = cur.next
        return None
    

def check(arr_1, arr_2, n_array=0):
    ull = UnrolledLinkedList(arr_1, n_array)
    print(ull)
    for e in arr_2:
        del ull[ull.index(e)]
        print(ull)
    return [ull[i] for i in range(len(ull))]


if __name__ == "__main__":
    ull = UnrolledLinkedList(list(map(int, input().split())))
    print(ull)
