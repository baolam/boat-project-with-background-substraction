import math

class MatrixPoint:
  def __init__(self, rows, cols):
    self.x = 0
    self.y = 0
    self.rows = rows
    self.cols = cols
  
  def run(self, d, angle):
    # Hàm này dùng để cập nhật lại toạ độ
    self.x = self.x + math.cos(angle) * d
    self.y = self.y + math.sin(angle) * d
  
  def coordinate(self):
    return {
      "x" : self.x,
      "y" : self.y
    }