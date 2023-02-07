def estimate(trash_areas):
  areas = dict()
  for trash_area in areas:
    __, __, w, h = trash_area
    if areas[w * h] == None:
      areas[w * h] = []
    areas[w * h].append(trash_area)
  return trash_areas

def real_distance(w, f=30, e=0.2, W=2):
  return f * W / (w + e)