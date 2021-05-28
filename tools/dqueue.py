import queue
import threading


class Queue(queue.Queue):

    def __init__(self, maxsize=0, count=1):
        """
        :param maxsize: 队列大小
        :param count:
            count >= 2, 调用count次m_get后删除元素
            count < 2, 直接取出
        """
        super().__init__(maxsize)
        self._count = 1 if count < 1 else count
        self._value = list(range(count))
        self.not_end = threading.Condition(self.mutex)
        self.flag = 1
        self.unfinished_tasks = count

    def m_get(self, sign=0, timeout=1):
        with self.not_empty:
            while not self._qsize():
                if not self.not_empty.wait(timeout):
                    return False

            if self._count < 2:
                item = self._get()
                self.not_full.notify()
                return True, item

            if sign in self._value:
                if self.flag == self._count:
                    item = self._get()
                    self.not_full.notify()
                    self.not_end.notify_all()
                    self.flag = 1
                    return True, item
                else:
                    # item = list(self.queue)[0]
                    item = self.queue[0]  # deque支持索引取值
                    self.flag += 1
                    self.not_end.wait()
                    return False, item
        return False

    def m_put(self, item, timeout=1):
        with self.not_full:
            if self.maxsize > 0:
                while self._qsize() >= self.maxsize:
                    if not self.not_full.wait(timeout):
                        return False
            self._put(item)
            self.not_empty.notify_all()
            return True
