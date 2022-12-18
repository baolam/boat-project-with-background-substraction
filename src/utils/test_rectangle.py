from .rectangle import union

while True:
  rec1 = list(map(int, input("Hình 1: ").split()))
  rec2 = list(map(int, input("Hình 2: ").split()))
  
  print(union(rec1, rec2))