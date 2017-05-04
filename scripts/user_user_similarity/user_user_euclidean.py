import csv
import numpy as np
import math
import random, sys


class user_sim:
	def __init__(self):	
		self.data=np.genfromtxt('refined_all.csv',delimiter=',')
		shp=self.data.shape
		self.length=shp[0]
		self.width=shp[1]
		self.user_rowid={}				#dictionary containing the row number of each user
		self.user_comments={}			#dictionary containing the number of comments of every user above a certain threshold
		self.imp_users=[]				#only stores the ids of users above 'threshold' number of comments

	def euclidean(self,a,b):
		arr_1=self.data[a][1:]
		arr_2=self.data[b][1:]
		diffx=arr_1-arr_2
		sqrd=diffx*diffx
		sum_sqrd=np.sum(sqrd)
		distx=math.sqrt(sum_sqrd)
		return(distx)

	def num_comments(self,threshold):
		count_above=0
		print("reached here!")
		with open("refined_all.csv","r") as f:
			reader = csv.reader(f)			#reading using CSV reader coz numpy doesn't read text 
			#row=next(reader)				#first row in the dataset
			for j in range(self.length):
				row=next(reader)
				userid=row[0]
				self.user_rowid[userid]=j
				noc=sum(self.data[j][1:])
				if noc>=threshold:
					self.user_comments[userid]=noc
					self.imp_users.append(userid)
					count_above+=1
		print(count_above,"instances above threshold!")
		print(self.imp_users)		

	def drawProgressBar(self,percent, barLen = 50):			#just a progress bar so that you dont lose patience
		    sys.stdout.write("\r")
		    progress = ""
		    for i in range(barLen):
		        if i<int(barLen * percent):
		            progress += "="
		        else:
		            progress += " "
		    sys.stdout.write("[ %s ] %.2f%%" % (progress, percent * 100))
		    sys.stdout.flush()

	def find_all_distances(self):				#finds the distance between each important user
		ofile=open('user_distances.txt','w')
		total=len(self.imp_users)
		total_comparisons=(total*(total+1))/2
		cnt=0
		for j in range(len(self.imp_users)):
			for k in range(j+1,len(self.imp_users)):
				perc=cnt/total_comparisons
				p=self.user_rowid[self.imp_users[j]]
				q=self.user_rowid[self.imp_users[k]]
				scr=self.euclidean(p,q)
				strx=self.imp_users[j]+'	'+self.imp_users[k]+'	'+str(scr)+'\n'
				ofile.write(strx)
				#print(perc,"%")
				cnt+=1
				self.drawProgressBar(perc)

	def control(self):
		self.num_comments(50)
		self.find_all_distances()


ux=user_sim()
ux.control()