from shapely.geometry import Polygon, Point, LineString, MultiPolygon
import pylab, math, json
import shapefile

def point_hash(pt):
  return hash((pt.x, pt.y))

def clamp(val, min_val, max_val, min_out, max_out):
  if val <= min_val:
     return min_out
  if val >= max_val:
    return max_out
  scale = (val - min_val) / (max_val - min_val)
  return min_out + scale * (max_out - min_out)

LOW_2PP = 0.5
LOW_PRI = 210
LOW_SEC = 210
LOW_RADIUS = 8
LOW_VOTES = 400
HIGH_2PP = 0.7
HIGH_PRI = 255
HIGH_SEC = 0
HIGH_RADIUS = 20
HIGH_VOTES = 2500

ne_lat = -35.11203684
ne_lng = 149.22332660
sw_lat = -35.33640515
sw_lng = 148.94866840

height = abs(sw_lat - ne_lat)
width = abs(sw_lng - ne_lng)

sf = shapefile.Reader('shapefiles/COM_ELB_region')
# Find the ELECT_DIV field
elect_div_idx = -1
for i,field in enumerate(sf.fields[1:]):
  if field[0] == 'ELECT_DIV':
    elect_div_idx = i
    break
assert elect_div_idx > -1

fraser_idx = -1
for i,record in enumerate(sf.records()):
  if record[elect_div_idx] == 'Fraser':
    fraser_idx = i
    break
assert fraser_idx > -1

shape = sf.shape(fraser_idx)

boundary_polys = []
for i in range(len(shape.parts) - 1):
  boundary_polys.append(Polygon(shape.points[shape.parts[i]:shape.parts[i+1]]))

p = MultiPolygon(boundary_polys)
minx, miny, maxx, maxy = p.bounds

bound_box = Polygon([(minx, miny), (minx, maxy), (maxx, maxy), (maxx, miny)])

bound_box_pts = zip(bound_box.exterior.xy[0], bound_box.exterior.xy[1])
bound_box_lines = []
for i in range(len(bound_box_pts) - 1):
  bound_box_lines.append(LineString([bound_box_pts[i], bound_box_pts[i+1]]))


diag_length = math.sqrt(height**2 + width**2)

#print bound_box_lines

booths = {
'ainslienorth': Point(149.144166, -35.256786),
'ainsliesouth': Point(149.145102, -35.267501),
'amaroo': Point(149.132587, -35.169448),
'aranda': Point(149.084432, -35.255632),
'belconnen': Point(149.0718475, -35.2396298),
'belconnenppvc': Point(149.069036, -35.2389275),
'braddon': Point(149.137702, -35.274868),
'bruce': Point(149.0909124, -35.244079),
'campbell': Point(149.1106371, -35.275081),
'charnwood': Point(149.030743, -35.199244),
'city': Point(149.129927, -35.27663),
'cityfraserppvc': Point(149.129927, -35.27663),
'dickson': Point(149.138, -35.253),
'divisionalofficeprepoll': Point(149.126166, -35.279795),
'downer': Point(149.145017, -35.245186),
'evatt': Point(149.077576, -35.207254),
'evattsouth': Point(149.049966, -35.211034),
'florey': Point(149.051672, -35.226376),
'frasercentral': Point(149.0449986, -35.1913361),
'giralang': Point(149.094794, -35.212894),
'gungahlin': Point(149.130782, -35.187115),
'gungahlinppvc': Point(149.12269, -35.187509),
'hall': Point(149.070511, -35.171149),
'harrison': Point(149.151402, -35.197876),
'holt': Point(149.0246982, -35.2279199),
'kaleen': Point(149.114536, -35.224305),
'kaleensouth': Point(149.098301, -35.235693),
'lyneham': Point(149.125595, -35.252276),
'macgregor': Point(149.012145, -35.213163),
'macquarie': Point(149.05869, -35.251208),
'melba': Point(149.049966, -35.211034),
'ngunnawal': Point(149.112176, -35.166544),
'ngunnawalsouth': Point(149.106865, -35.174905),
'nicholls': Point(149.100486, -35.181719),
'oconnor': Point(149.125512, -35.258867),
'page': Point(149.042858, -35.239931),
'palmerston': Point(149.117902, -35.190631),
'reid': Point(149.139997, -35.282012),
'scullin': Point(149.040072, -35.235709),
'turner': Point(149.125971, -35.264656),
'watson': Point(149.15985, -35.241439),
'weetangera': Point(149.046045, -35.249283)
}

votes = {
'ainslienorth': {'alp': 76.42, 'lnp': 23.58, 'tot': 2200},
'ainsliesouth': {'alp': 76.66, 'lnp': 23.34, 'tot': 800},
'amaroo': {'alp': 55.78, 'lnp': 44.22, 'tot': 3000},
'aranda': {'alp': 73.05, 'lnp': 26.95, 'tot': 2700},
'belconnen': {'alp': 65.32, 'lnp': 34.68, 'tot': 2500},
'belconnenppvc': {'alp': 61.31, 'lnp': 38.69, 'tot': 7300},
'braddon': {'alp': 72.49, 'lnp': 27.51, 'tot': 1800},
'bruce': {'alp': 61.07, 'lnp': 38.93, 'tot': 800},
'campbell': {'alp': 48.89, 'lnp': 51.11, 'tot': 2100},
'charnwood': {'alp': 63.63, 'lnp': 36.37, 'tot': 3400},
'city': {'alp': 70.42, 'lnp': 29.58, 'tot': 1400},
'cityfraserppvc': {'alp': 67.45, 'lnp': 32.55, 'tot': 4300},
'dickson': {'alp': 69.7, 'lnp': 30.3, 'tot': 1500},
'divisionalofficeprepoll': {'alp': 67.99, 'lnp': 32.01, 'tot': 2400},
'downer': {'alp': 71.01, 'lnp': 28.99, 'tot': 1200},
'evatt': {'alp': 64.24, 'lnp': 35.76, 'tot': 3200},
'evattsouth': {'alp': 66.01, 'lnp': 33.99, 'tot': 1500},
'florey': {'alp': 63.38, 'lnp': 36.62, 'tot': 2000},
'frasercentral': {'alp': 62.46, 'lnp': 37.54, 'tot': 3000},
'giralang': {'alp': 63.8, 'lnp': 36.2, 'tot': 1800},
'gungahlin': {'alp': 55.04, 'lnp': 44.96, 'tot': 2700},
'gungahlinppvc': {'alp': 52.44, 'lnp': 47.56, 'tot': 3500},
'hall': {'alp': 51.7, 'lnp': 48.3, 'tot': 200},
'harrison': {'alp': 53.34, 'lnp': 46.66, 'tot': 2000},
'holt': {'alp': 65.54, 'lnp': 34.46, 'tot': 2600},
'kaleen': {'alp': 64.03, 'lnp': 35.97, 'tot': 2700},
'kaleensouth': {'alp': 62.58, 'lnp': 37.42, 'tot': 1700},
'lyneham': {'alp': 76.78, 'lnp': 23.22, 'tot': 3000},
'macgregor': {'alp': 67.03, 'lnp': 32.97, 'tot': 2000},
'macquarie': {'alp': 70.67, 'lnp': 29.33, 'tot': 1800},
'melba': {'alp': 65.29, 'lnp': 34.71, 'tot': 1900},
'ngunnawal': {'alp': 63.16, 'lnp': 36.84, 'tot': 2100},
'ngunnawalsouth': {'alp': 63.48, 'lnp': 36.52, 'tot': 900},
'nicholls': {'alp': 53.62, 'lnp': 46.38, 'tot': 3100},
'oconnor': {'alp': 69.84, 'lnp': 30.16, 'tot': 900},
'page': {'alp': 64.82, 'lnp': 35.18, 'tot': 2000},
'palmerston': {'alp': 64.43, 'lnp': 35.57, 'tot': 2400},
'reid': {'alp': 62.03, 'lnp': 37.97, 'tot': 700},
'scullin': {'alp': 69.3, 'lnp': 30.7, 'tot': 1600},
'turner': {'alp': 76.63, 'lnp': 23.37, 'tot': 2100},
'watson': {'alp': 73.19, 'lnp': 26.81, 'tot': 2900},
'weetangera': {'alp': 63.88, 'lnp': 36.12, 'tot': 2200}
}

#watson = Point(149.15985, -35.241439)
#aranda = Point(149.084432, -35.255632)
#palmerston = Point(149.117902, -35.190631)

x,y = bound_box.exterior.xy
pylab.fill(x, y, color='#ff0000', alpha=0.25)

for name,point in booths.items():
  pylab.plot(point.x, point.y, 'b,')

#pylab.show()

poly_map = {}
poly_map_points = {}

booth_indices = booths.keys()
booth_indices.sort()

for outer_i in range(len(booth_indices)):
  point1 = booths[booth_indices[outer_i]]
  for inner_i in range(outer_i-1, -1, -1):
    point2 = booths[booth_indices[inner_i]]
    #for name2,point2 in booths.items():
    #if name1 == name2:
      #continue
    if (point1.x - point2.x)**2 + (point1.y - point2.y)**2 < 10**(-6):
      continue
    print booth_indices[outer_i], booth_indices[inner_i]
#for point1,point2 in [(watson, aranda), (aranda, palmerston), (watson, palmerston)]:
    midpt = Point((point1.x + point2.x)/2.0, (point1.y + point2.y)/2.0)
    #pylab.plot(midpt.x, midpt.y, 'g,')
    
    #print "Diagonal length: ", diag_length
    
    grad = (point1.y - point2.y)/(point1.x - point2.x)
    perp_grad = -1.0/grad
    #print "Gradient: ", grad, perp_grad
    
    angle = math.atan(perp_grad)
    #alt_angle = math.pi/2.0 - angle
    #print "Angle: ", angle
    
    delta_x = (diag_length)*math.cos(angle)
    delta_y = (diag_length)*math.sin(angle)
    
    ext1 = Point(midpt.x + delta_x, midpt.y + delta_y)
    ext2 = Point(midpt.x - delta_x, midpt.y - delta_y)
    #print "Ext1: ", ext1.x, ext1.y
    #print "Ext2: ", ext2.x, ext2.y
    #pylab.plot([ext1.x, ext2.x], [ext1.y, ext2.y], 'g,')
    
    intra = LineString([(point1.x, point1.y), (point2.x, point2.y)])
    perp = LineString([(ext1.x, ext1.y), (ext2.x, ext2.y)])
    bdy = bound_box.intersection(perp)
    bdy_end1 = (bdy.xy[0][0], bdy.xy[1][0])
    bdy_end2 = (bdy.xy[0][1], bdy.xy[1][1])
    #print "Perp line: ", bdy
    
    x,y = intra.xy
    #pylab.plot(x, y, color='blue', aa=True)
    
    x,y = bdy.xy
    #pylab.plot(x, y, color='green', aa=True)
    
    grad_actual = (ext2.y - ext1.y)/(ext2.x - ext1.x)
    #print "Actual grad: ", grad_actual
    
    # Walk the boundary box and create a new polygon
    first_poly = []
    second_poly = []
    i = 0
    while i < len(bound_box_lines):
      if bound_box_lines[i].intersects(bdy):
        break
      i+=1
      
    assert i != len(bound_box_lines)
    
    first_pt = bound_box_lines[i].intersection(bdy)
    first_poly.append((first_pt.xy[0][0], first_pt.xy[1][0]))
    i = (i+1) % len(bound_box_lines)
    
    j = 0
    while True:
      first_poly.append((bound_box_lines[i].xy[0][0], bound_box_lines[i].xy[1][0]))
      if bound_box_lines[i].intersects(bdy):
        break
      i = (i+1) % len(bound_box_lines)
      j += 1
      if j > len(bound_box_lines):
        assert False
    
    second_pt = bound_box_lines[i].intersection(bdy)
    first_poly.append((second_pt.xy[0][0], second_pt.xy[1][0]))
    # First poly is now done
    
    second_poly.append((second_pt.xy[0][0], second_pt.xy[1][0]))
    i = (i+1) % len(bound_box_lines)
    j = 0
    while True:
      x,y = bound_box_lines[i].xy
      second_poly.append((bound_box_lines[i].xy[0][0], bound_box_lines[i].xy[1][0]))
      if bound_box_lines[i].intersects(bdy):
        break
      i = (i+1) % len(bound_box_lines)
      j += 1
      if j > len(bound_box_lines):
        assert False
    
    second_poly.append((first_pt.xy[0][0], first_pt.xy[1][0]))
    # Second poly also done
    
    poly_one = Polygon(first_poly)
    poly_two = Polygon(second_poly)
    
    pt1_hash = booth_indices[outer_i]#point_hash(point1)
    pt2_hash = booth_indices[inner_i]#point_hash(point2)
    
    if pt1_hash not in poly_map:
      poly_map[pt1_hash] = []
      #poly_map_points[pt1_hash] = point1
    if pt2_hash not in poly_map:
      poly_map[pt2_hash] = []
      #poly_map_points[pt2_hash] = point2
    
    if poly_one.contains(point1):
      poly_map[pt1_hash].append(poly_one)
    elif poly_two.contains(point1):
      poly_map[pt1_hash].append(poly_two)
    else:
      print "Point1 not in either poly"
      assert False
    
    if poly_one.contains(point2):
      poly_map[pt2_hash].append(poly_one)
    elif poly_two.contains(point2):
      poly_map[pt2_hash].append(poly_two)
    else:
      print "Point2 not in either poly"
      assert False

output = []
output_smoothed = []

for k,polys in poly_map.items():
  assert len(polys) > 0
  poly_int = polys[0]
  for i in range(1, len(polys)):
    poly_int = poly_int.intersection(polys[i])
  poly_int = p.intersection(poly_int)
  
  
  
  #col = k % 2**(3*8)
  #col_str = '#%06x' % col
  
  alpWin = False
  tpp = 0
  if votes[k]['alp'] > 50.0:
    alpWin = True
    tpp = votes[k]['alp']
  else:
    tpp = votes[k]['lnp']
  tpp_scale = round(tpp)/100;
  primCol = clamp(tpp_scale, LOW_2PP, HIGH_2PP, LOW_PRI, HIGH_PRI)
  secCol = clamp(tpp_scale, LOW_2PP, HIGH_2PP, LOW_SEC, HIGH_SEC)
  if alpWin:
    colour_parts = (primCol, secCol, secCol)
  else:
    colour_parts = (secCol, secCol, primCol)
  col = '#%02x%02x%02x' % colour_parts  
  
  poly_int_simp = poly_int.simplify(0.001)
  
  if isinstance(poly_int, Polygon):
    poly_points = [zip(poly_int.exterior.xy[0], poly_int.exterior.xy[1])]
    poly_points_simp = [zip(poly_int_simp.exterior.xy[0], poly_int_simp.exterior.xy[1])]
    x,y = poly_int.exterior.xy
    pylab.fill(x,y,color=col)
  else:
    poly_points = []
    poly_points_simp = []
    for segment in poly_int.geoms:
      poly_points.append(zip(segment.exterior.xy[0], segment.exterior.xy[1]))
      x,y = segment.exterior.xy
      pylab.fill(x,y,color=col)
    for segment in poly_int_simp.geoms:
      poly_points_simp.append(zip(segment.exterior.xy[0], segment.exterior.xy[1]))
  
  output.append({
    'poly': poly_points,
    'poly_simp': poly_points_simp,
    'name': k,
    '2pp': tpp,
    'winner': ('ALP' if alpWin else 'Coalition'),
    'votes': votes[k]['tot']
  })
  
  #poly_int_simp
  
  #print k, poly_int

fp = open('cache/fraser-poly.js', 'w')
json.dump(output, fp)
fp.close()

pylab.show()