# Create your views here.

from django.template import Context, loader
from django.http import HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect, HttpResponseBadRequest, Http404
from django.contrib.admin import site as adminsite
from search import * 
import re
import ast
import random


i = 0
#lines = open("search/smallMetadata").readlines()
#lines = open("search/MetadataDump_flattened").readlines()
lines = open("search/MetadataDump_FlattenedBarrington").readlines()
print "Number of lines read : ",len(lines)
points = {}

for j in range(len(lines)):
	point = ast.literal_eval(lines[j].strip())
	points[point["uuid"]] = {}
	points[point["uuid"]]["string"] = lines[j].strip()
	points[point["uuid"]]["dict"] = point
	points[point["uuid"]]["dict-split"] = {}
	for key in points[point["uuid"]]["dict"]:
		value = points[point["uuid"]]["dict"][key]
		split_values = re.split('\ |\/|\.|\_|\-|\,',value)
		points[point["uuid"]]["dict-split"][key] = split_values
	points[point["uuid"]]["index"] = j
	if j==0:
		print points

def search(request):
	t = loader.get_template('search3.html')
	c = Context({})
	return HttpResponse(t.render(c))

def getresultsStatus(request):
	global i
	global lines

	#f = open("temp-" + str(i),"w")
	#f.write(str(request))
	i += 1
	#f.write("SESSION DATA : " + str(request.session))

	request.session["test_key"] = "TEST VALUE"

	#f.write("\n\n\nNEW SESSION DATA\n" + str(request.session) + "\n\n")
	parts = str(request).split(',')
	result = [ ]
	for part in parts:
		if "POST" not in part:
			continue
		#f.write(" Number of lines in read file : " + str(len(lines)))
		query = part.strip().split('\'')[1].strip()
		result = parse_query(lines,query,20)	

		if len(result) == 0:
			result = [ {"Path" : "No results" } ]
			print "Returning No results"
		#f.write("\n\n"  + str(query) + "\n\n" + str(result))
		break
	#f.close()	

	request.session["initial_search_results"] = result
	if "all_search_results" in request.session:
		del request.session["all_search_results"]
	request.session["result_counter"] = len(result)
	request.session["deleted"] = 0
	request.session["deleted_results"] = []

	request.session.modified = True
	result = str(result)
	result = re.sub('\'','\"',result)
	print "Returning result from main view module : ",result
	return HttpResponse([result])

def getExtraResults(request):
	global i
	global lines

	#f = open("temp-" + str(i),"w")
	#f.write(str(request))
	#i += 1
	print "Getting all results "

	parts = str(request).split(',')
	result = [ ]
	for part in parts:
		if "POST" not in part:
			continue
		#f.write(" Number of lines in read file : " + str(len(lines)))
		query = part.strip().split('\'')[1].strip()
		result = parse_query(lines,query,10000)	

			
		if len(result) == 0:
			print "EXTRA RESULTS : No extra results : "
			result = [ {"Path" : "No results" } ]
		#f.write("\n\n"  + str(query) + "\n\n" + str(result))
		break
	#f.close()	
	
	final_results = []
	final_results.extend(request.session["initial_search_results"])
		
	for point in result:
		if point in request.session["initial_search_results"]:
			continue
		final_results.append(point)
		
	request.session["all_search_results"] = final_results
	print "Obtained all search results, Number of results : ",len(request.session["all_search_results"])
	result = str(result)
	result = re.sub('\'','\"',result)
	request.session.modified = True
	return HttpResponse([result])

def getNextSearchResults(request):
		print "starting gnsr"
		try:
			counter = request.session["result_counter"]
			if counter >= len(request.session["all_search_results"]):
				result = str(request.session["all_search_results"])
				result = re.sub('\'','\"',result)
				print "t1: ", result
				return HttpResponse([result])


			result = []
			if (request.session["deleted"]) > 2:
				ref_point_orig = request.session["all_search_results"][0]
				ref_point = points[ref_point_orig["uuid"]]["dict-split"]
				common_keys = ref_point
				for point_orig in request.session["all_search_results"][1:counter]:
					point = points[point_orig["uuid"]]["dict-split"]
					to_delete_keys = []
					to_delete_values = []
					for key in common_keys:
						if key not in point:
							to_delete_keys.append(key)
							continue
						for value in ref_point[key]:
							if value not in point[key]:
								to_delete_values.append((key,value))
								continue
					for key in to_delete_keys:
						del common_keys[key]
					for (key,value) in to_delete_values:
						if key not in common_keys:
							continue
						common_keys[key].remove(value)

				to_delete = []
				for point_orig in request.session["all_search_results"][request.session["result_counter"]:]:
					point = points[point_orig["uuid"]]["dict-split"]
					flag = 0
					for key in common_keys:
						if key not in point:
							flag = 1
							break
						for value in common_keys[key]:
							if value not in point[key]:
								flag = 1
								break
						if flag ==1 :
							break
					if flag == 1:
						to_delete.append(point_orig)

				for point in to_delete:
					request.session["all_search_results"].remove(point)
				

			if counter + 20 > len(request.session["all_search_results"]):
				end_point = len(request.session["all_search_results"])
			else:
				end_point = counter + 20
			for c in range(end_point):
				result.append(request.session["all_search_results"][c])

			request.session["result_counter"] = end_point

			request.session.modified = True

			result = str(result)
			result = re.sub('\'','\"',result)
		except Exception as e:
			print "Exception:", e
			return HttpResponse(e)
		request.session.modified = True
		return HttpResponse([result])

def replace(request):
	global points
	global i
	#f = open("temp-" + str(i),"w")
	#f.write(str(request))
	#i += 1
	parts = str(request).split(',')
	ans = [ ]

	result = []
	point_to_remove = None

	print "Printing request session"
	print request.session


	for part in parts:
		if "POST" not in part:
			continue
		query = part.strip().split('\'')[1].strip()
		print query
		#point_to_remove = None
		for point in request.session["all_search_results"]:
			if query == point["uuid"]:
				print "Removing point ",point
				point_to_remove = point
				break
		break
	request.session["all_search_results"].remove(point_to_remove)
	request.session["result_counter"] -= 1
	request.session["deleted"] += 1
	request.session["deleted_results"].append(point_to_remove)
	print "Counter = ",request.session["result_counter"]
	request.session.modified = True
	return HttpResponse("")

def genQuery(request):
	counter = request.session["result_counter"]
	common_keys = []
	ref_point = request.session["all_search_results"][0]
	for key in ref_point:
		flag = 0
		for point in request.session["all_search_results"][1:counter]:
			if key not in point:
				flag = 1
				break
			if ref_point[key] != point[key]:
				flag = 1
				break
		
		if flag == 0:
			common_keys.append(key)

	query = "select data before now limit 1000 where "
	for k in range(len(common_keys)):
		if "UnitofMeasure" in common_keys[k]:
			continue
		query = query + common_keys[k] + "='" + ref_point[common_keys[k]] + "'"
		if k < len(common_keys)-1:
			query = query + " and "

	request.session.modified = True
	return HttpResponse(query)

def replaceOld(request):
	global points
	global i
	#f = open("temp-" + str(i),"w")
	#f.write(str(request))
	i += 1
	parts = str(request).split(',')
	ans = [ ]

	result = []
	for part in parts:
		if "POST" not in part:
			continue
		query = part.strip().split('\'')[1].strip()
		if "test_key" not in request.session:
			result = [ { "Path" : " No results" , "uuid" : "random" } ]
		else:
			result = [ { "Path" : request.session["test_key"] , "uuid" : "random" } ]
		break
	result = str(result)
	result = re.sub('\'','\"',result)
	return HttpResponse([result])


		
def getMetadata(request):
	global points
	global i
	#f = open("temp-" + str(i),"w")
	#f.write(str(request))
	#i += 1
	parts = str(request).split(',')
	ans = [ ]
	for part in parts:
		if "POST" not in part:
			continue
		query = part.strip().split('\'')[1].strip()
		#f.write("\n UUID = " + query)
		print "UUID",query
		#ans = [ points['43a17dfe-3118-5cbe-b591-0178c9f95f5a']['string'] ]
		ans = [ str(points[query]["dict"]) ]
		#print "ANS ",ans
		#f.write("\n\n RETURNED " + str(ans))
		#f.close()
		break 
		
	return HttpResponse([ str(ans) ])

def updateMetadata(request):
	global points
	global lines
	global i
	#f = open("temp-" + str(i),"w")
	#f.write(str(request))
	#i += 1
	parts = str(request).split(',')
	ans = [ ]
	for part in parts:
		if "POST" not in part:
			continue
		query = part.strip().split('\'')[1].strip()

		print "UPDATING DATA",query
		tags = query.strip().split(' ')
		uuid = tags[0].strip()
		for tag in tags[1:]:
			key = tag.split(':')[0].strip()
			value = tag.split(':')[1].strip()
			points[uuid]["dict"]["Added/" + key] = value
		
		points[uuid]["string"] = str(points[uuid]["dict"])
		lines[points[uuid]["index"]] = points[uuid]["string"]
 
		break

	return HttpResponse([])

def getresults(request):
	global i

	f = open("tmp-" + str(i),"w")
	f.write(str(request))
	i += 1


	parts = str(request).split(',')
	result = [ 1, 2 , 3]
	for part in parts:
		if "POST" not in part:
			continue
		query = part.strip().split('[')[1].strip().split('\'')[1].strip()
		result = keywordSearch(query)	

		f.write("\n\n"  + str(query) + "\n\n" + str(result))
		break
	f.close()	

	result = str(result)
	result = re.sub('\'','\"',result)
	return HttpResponse([result])
