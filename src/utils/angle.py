import math
from typing import Tuple


def angle(centroid, width, __height=None) -> Tuple[int, bool]:
  """
    Xác định góc quay so với trục chính
    -----------------------------------
    Một bức ảnh đầu vào là một ma trận với kích thước height (chiều rộng) * width (chiều dài)
    -----------------------------------
    Trả về gồm giá trị góc quay và hướng quay
  """
  # x là giá trị theo trục width
  # y là giá trị theo trục y
  x, y = centroid
  if y == 0:
    return 0, False
  delta_x = x - width / 2
  left = True
  if delta_x > 0:
      left = False
  delta_x = abs(delta_x)
  tan_alpha = delta_x / y
  tan_alpha = math.atan(tan_alpha)
  tan_alpha = math.degrees(tan_alpha)
  return tan_alpha, left
