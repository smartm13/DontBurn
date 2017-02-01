
import googlemaps, math, ephem

import datetime
#import pprint
#sprint(now)

gmaps = googlemaps.Client(key='AIzaSyDafKfrnMkZ2czKRX_p_AgEzjDzaW92LcA')


#pprint(steps)

def angleFromCoordinate(loc1, loc2):
	loc1_lng = math.radians(loc1['lng'])
	loc1_lat = math.radians(loc1['lat'])
	loc2_lng = math.radians(loc2['lng'])
	loc2_lat = math.radians(loc2['lat'])
	d_lng = loc2_lng - loc1_lng
	y=math.sin(d_lng) * math.cos(loc2_lat)
	x = math.cos(loc1_lat) * math.sin(loc2_lat) - math.sin(loc1_lat) * math.cos(loc2_lat) * math.cos(d_lng)
	brng = math.atan2(y, x);
	brng = ephem.degrees(brng)
	#brng = math.degrees(brng)
	#brng = (brng + 360) % 360
	#brng = 360 - brng
	#print((brng.norm))
	#print('fdkhfdkj',brng.norm)
	#print(str(brng.norm))
	return brng.norm
def quadrant(angle):
	if angle>=ephem.degrees(0) and angle<ephem.degrees(math.pi/2):
		return 1
	if angle>=ephem.degrees(math.pi/2) and angle<ephem.degrees(math.pi):
		return 2
	if angle>=ephem.degrees(math.pi) and angle<ephem.degrees(3*(math.pi/2)):
		return 3
	if angle>=ephem.degrees(3*(math.pi/2)) and angle<ephem.degrees(2*math.pi):
		return 4

def whereissun(my,azm):
	mq = quadrant(my)
	aq = quadrant(azm)
	if mq==aq or abs(mq-aq)==2:
		if azm>my:
			return 'right'
		return 'left'
	else:
		if (mq==1 and aq==2) or (mq==2 and aq==3) or (mq==3 and aq==4) or (mq==4 and aq==1):
			return 'right'
		else:
			return 'left'


def azimuthAngle(location,secsAfterNow):
    now = datetime.datetime.utcnow()
    lng1 = (str(int(location['lng'])))
    lng2 = (str(int((location['lng']-int(location['lng']))*60)))
    lng3 = (str(((location['lng']-int(location['lng']))*60 - int((location['lng']-int(location['lng']))*60))*60))
    lng=lng1+':'+lng2+':'+lng3
    lat1 = (str(int(location['lat'])))
    lat2 = (str(int((location['lat']-int(location['lat']))*60)))
    lat3 = (str(((location['lat']-int(location['lat']))*60 - int((location['lat']-int(location['lat']))*60))*60))
    lat=lat1+':'+lat2+':'+lat3
    o = ephem.Observer()
    o.lon = lng
    o.lat = lat
    timeobj=now + datetime.timedelta(seconds=secsAfterNow)
    o.date = timeobj.strftime("%Y/%m/%d %H:%M:%S")
    sun = ephem.Sun(o)
    sun.compute(o)
    return(sun.az.norm)

def find_sun_pos(source,destination):
	directions_result = gmaps.directions(source,destination, mode="driving")#,departure_time=datetime.datetime.now())
	if directions_result==None:return 'not found'
	steps,data,trvTs=[],[],0
	dist_left = dist_right = 0
	for step in directions_result[0]['legs'][0]['steps']:
			l = {'start' : step['start_location'] , 'end' : step['end_location'], 'distance' : step['distance']['value'], 'distance_text' : step['distance']['text'], 'deltaTs':step['duration']['value'] }
			steps.append(l)
	for step in steps:
			myangle = (angleFromCoordinate(step['start'] ,step['end']))
			azm_start = (azimuthAngle(step['start'],trvTs))
			azm_end = (azimuthAngle(step['end'],trvTs+step['deltaTs']))  #prettyUseLessInCalculations-joLoda
			trvTs+=step['deltaTs']
			sun_pos =  whereissun(myangle, azm_start)
			distance_text = step['distance_text']
			distance = step['distance']

			if sun_pos == 'left':
				dist_left+=distance
			else:
				dist_right+=distance

			if dist_left>dist_right:
				a='<h3>sun will mostly be on: <i>left</i></h3>'
			else:
				a='<h3>sun will mostly be on: <i>right</i></h3>'
			d = "{ 'sun_pos': <b>"+sun_pos+"</b>, 'distance_text': "+distance_text+", 'myangle': "+str(myangle)+", 'azm_start': "+str(azm_start)+", 'azm_end': "+str(azm_end)+", 'distance':" +str(distance)+" }"
			data.append(str(d))
	data.insert(0,'total left distance: '+str(dist_left)+'m')
	data.insert(0,'total right distance: '+str(dist_right)+'m')
	data.insert(0,a)
	return data


#print(find_sun_pos('Himalaya Zircon, Motera, Ahmedabad, Gujarat 382424','Dada Harir Vav, Haripura, Asarwa, Ahmedabad, Gujarat 380016'))
