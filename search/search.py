import os
import sys
import commands
import ast

def parse_query(in_lines,query,maxresults):
	print "Query : ",query
	parts = query.strip().split(' ')
	queryTerms = []
	filters = []
	for part in parts:
		part = part.strip()
		if part == '':
			continue
		if ":" not in part:
			queryTerms.append(part.upper())
		else:
			filters.append(part.upper())


	print "Query Terms : ",queryTerms
	print "Filters : ",filters
	results = getSearch(in_lines,queryTerms,maxresults)

	results =  filter(filters,results)

        print "Number of results after filterning : ",len(results)
	return results
	#return rank(results,queryTerms)

def getSearch(in_lines,words,maxresults):
	results = []

	count = 0	
	for orig_line in in_lines:
		line = orig_line.strip().upper()
		flag = 0
		for word in words:
			if word not in line or "SAMPLE" in line:
				flag = 1
				break
		if flag == 0:
			point = ast.literal_eval(orig_line.strip())
			results.append(point)
			count += 1

		if count == maxresults:
			break

        print "Results from search module : ",len(results)
	return results

def filter(filters,results):

	if len(filters) == 0:
		return results

	filterList = {}
	
	for f in filters:
		key = f.split(":")[0].strip()
		value = f.split(":")[-1].strip()
		
		if key not in filterList:
			filterList[key] = []
			filterList[key].append(value)
		else:
			filterList[key].append(value)
		
	final_results = []
	for result in results:
		flag = 1
		for key in filterList:
			string = ""
			for k in result.iterkeys():
				 if key in k.upper() :
					string = string + result[k].upper()
			for value in filterList[key]:
				if value not in string:
					flag = 0
					break

			if flag == 0:
				break

		if flag == 1:
			final_results.append(result)

	return final_results

def rank(filtered_results,queryTerms):
	results = []
	if len(queryTerms) == 0:
		return filtered_results
	for result in filtered_results:
		flag = 0
		for term in queryTerms :
			if term in result["uuid"].upper():
				flag = 1
				break

		if flag == 0:
			if "Description" in result:
				if term in result["Description"].upper() :
					results.insert(0,result)
				else:
					results.append(result)
			else:
				results.append(result)
	return results



if __name__ == "__main__":
	in_lines = open("MetadataDump_flattened").readlines()
	print "Number of read lines : ",len(in_lines)
	query = ""
	for i in range(len(sys.argv)-1):
		query = query + " " + sys.argv[i+1].strip()
	print parse_query(in_lines,query,100)




