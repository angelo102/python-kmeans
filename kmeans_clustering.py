import ConfigParser
import pylab as pl
from mpl_toolkits.mplot3d import Axes3D 
from numpy import vstack,array
from numpy.random import rand
from scipy.cluster.vq import kmeans,vq
import webbrowser

#get settings
config = ConfigParser.ConfigParser()
config.read("settings.ini")
input_file = config.get("SectionOne","input_file")
n_dimensions = int(config.get("SectionOne","num_dimensions"))
n_clusters = int(config.get("SectionOne","num_clusters"))
data_index1 = int(config.get("SectionOne","data_col_index1"))
data_index2 = int(config.get("SectionOne","data_col_index2"))
data_index3 = int(config.get("SectionOne","data_col_index3"))
x_col_index_d3 = int(config.get("SectionOne","x_col_index_d3"))
y_col_index_d3 = int(config.get("SectionOne","y_col_index_d3"))
url = config.get("SectionOne","d3_url")

#variable to hold attribute names for input on axis labels
col_names = []

#Obtain data from given file(dataset) in settings.ini
def get_data(num_dimensions):
	file_r = open(input_file,'r')
	col_names[:]=file_r.next().split(',')
	listn = []
	for line in file_r:
		s = line.split(',')
		if num_dimensions == 3:
			val = array([float(s[data_index1]),float(s[data_index2]),float(s[data_index3])])
		else:
			val = array([float(s[data_index1]),float(s[data_index2])])
		listn.append(val)
	file_r.close()
	data = vstack(listn)
	return data

#Export data to tsv file for visualization on D3
def export_d3_format():
	file_w = open('data.tsv','w')
	#write column headers
	headers ="\t".join(["x_value","y_value","centroid","\n"])
	file_w.write(headers)
	#write data
	for i,item in enumerate(data):
		s = "\t".join([str(item[x_col_index_d3]),str(item[y_col_index_d3]),str(idx[i]),"\n"])
		file_w.write(s)
	for i,centroid in enumerate(centroids):
		s = "\t".join([str(centroids[i][x_col_index_d3]),str(centroids[i][y_col_index_d3]),"centroid","\n"])
		file_w.write(s)
	file_w.close()

#Show data using plot from pylab and mplot3d
def plot_data(num_dimensions, num_clusters):
	if num_dimensions == 2:
		#maximum 8 cluster colors
		colors2d = ['ob','og','or','oc','om','oy','ok','ow']
		pl.xlabel("X: "+col_names[data_index1])
		pl.ylabel("Y: "+col_names[data_index2])
		# some plotting using numpy's logical indexing
		for i in range(num_clusters):
			#plot cluster
			pl.plot(data[idx==i,0],data[idx==i,1],colors2d[i%len(colors2d)])
			pl.plot(centroids[i,0],centroids[i,1],'sk',markersize=12)
		pl.show()
	else:
		colors3d = ['b','g','r','c','m','y','k','w']
		fig = pl.figure()
		ax = Axes3D(fig)
		ax.set_xlabel("X: "+col_names[data_index1])
		ax.set_ylabel("Y: "+col_names[data_index2])
		ax.set_zlabel("Z: "+col_names[data_index3])
		for i in range(num_clusters):
			ax.scatter(data[idx==i,0],data[idx==i,1],data[idx==i,2],c=colors3d[i%len(colors3d)])
			ax.scatter(centroids[i,0],centroids[i,1],centroids[i,2],c='k',s=50)
		pl.show()

#run
data = get_data(n_dimensions)
# compute kmeans with method from scipy
centroids,_ = kmeans(data,n_clusters)
# assign each sample to a cluster
idx,_ = vq(data,centroids)

#export data friendly to d3
export_d3_format()
webbrowser.open(url,new=2)
#plot data depending on dimensions and number of clusters
plot_data(n_dimensions,n_clusters)
#show centroid coordinates
print centroids



