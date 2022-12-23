def estimate(trash_areas):
  areas = dict()
  for trash_area in areas:
    __, __, w, h = trash_area
    if areas[w * h] == None:
      areas[w * h] = []
    areas[w * h].append(trash_area)
  return trash_areas