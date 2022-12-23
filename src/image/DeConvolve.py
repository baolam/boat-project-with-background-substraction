from typing import List
from typing import Tuple

from src.utils.rectangle import union
from src.utils.rectangle import overlap
from src.utils.rectangle import coordinate

ABSTRACT_RECTANGLE = List[Tuple[int, int, int, int]]

class DeConvolve:
  def __init__(self):
    self.threshold = 0

  def coordinate(self, rec):
    return coordinate(rec, self.threshold)
  
  def overlap(self, rec1, rec2):
    return overlap(rec1, rec2, self.threshold)
  
  def union(self, rec1, rec2):
    return union(rec1, rec2, self.threshold)

  def check(self, rectangles : ABSTRACT_RECTANGLE):
    for i in range(len(rectangles) - 1):
      for j in range(i + 1, len(rectangles)):
        is_overlap, __ = self.union(rectangles[i], rectangles[j])
        if is_overlap:
          return True
    return False

  def run(self, rectangles : ABSTRACT_RECTANGLE):
    if len(rectangles) == 0:
      return []
    # Lưu đồ thuật toán
    '''
      Nếu hai hình chữ nhật mà trùng lắp -> gộp lại thành một
      Gọi result là mảng quản lý các hình chữ nhật
      Lặp qua lần lượt các hình chữ nhật và đối chiếu với hcn trong mảng result
    '''
    r = self.__run(rectangles)
    while self.check(r):
      r = self.__run(r)
    return r

  def __run(self, rectangles : ABSTRACT_RECTANGLE):
    memories = [False] * len(rectangles)
    result = []
    for i in range(0, len(rectangles)):
      r = rectangles[i]
      if memories[i]:
        continue
      for j in range(i + 1, len(rectangles)):
        is_overlap, data = self.union(r, rectangles[j])
        if is_overlap: 
          memories[j] = True
          r = data
      result.append(r)
    return result
