# https://www.geeksforgeeks.org/find-two-rectangles-overlap/

def coordinate(rec, threshold):
  x, y, w, h = rec
  return [x - threshold, x + w + threshold], \
    [y - threshold, y + h + threshold]

def overlap(rec1, rec2, threshold):
  x1, y1 = coordinate(rec1, threshold)
  x2, y2 = coordinate(rec2, threshold)

  # if x1[0] == x1[1] or y1[0] == y1[1] == 1 \
  #   or x2[0] == x2[1] or y2[0] == y2[1]:
  #   return False
  
  if x1[0] >= x2[1] or x2[0] >= x1[1]:
    return False

  # Sửa lại điều kiện cạnh này 
  if y1[0] >= y2[1] or y2[0] >= y1[1]:
    return False
  
  return True

def union(rec1, rec2, threshold : int = 0):
  if not overlap(rec1, rec2, threshold):
    return False, []
  # x, y min
  # x, y max
  # print(rec1, rec2)
  x1, y1 = coordinate(rec1, threshold)
  x2, y2 = coordinate(rec2, threshold)
  x_min = min(x1[0], x2[0])
  x_max = max(x1[1], x2[1])
  y_min = min(y1[0], y2[0])
  y_max = max(y1[1], y2[1])
  return True, (x_min, y_min, x_max - x_min, y_max - y_min)
