"""
 visASTRI_temporal.py  -  description
 ---------------------------------------------------------------------------------
 Plotting the temporal curve for the ASTRI DL0 data
 ---------------------------------------------------------------------------------
 copyright            : (C) 2015 Valentina Fioretti
 email                : fioretti@iasfbo.inaf.it
 ----------------------------------------------
 Usage:
 visASTRI_temporal.py filename selPDM param subfield_id maxevt xvalue_temp xvalue_graph t=title y=ylabel
 ---------------------------------------------------------------------------------
 Parameters:
 - filename: path + file name of the FITS file
 - selPDM: the ID of the PDM to be plotted (> 0).
 - param: name of the parameter to be plotted, using the same convention of the FITS fields. E.g. HI
 - subfield_id: element (starting from 1) of the sub-array to be plotted (e.g. 1 to select the pixel 1 for HI of PDM).
 - maxevt: max row (event) to read and plot. If 0 all the events are read.
 - xvalue_temp: selected x-axis value (element of the array) for which the y-value content must be plotted.
 - xvalue_graph: selected x-axis value (element of the array) for which the y-value content must be plotted.
 - (optional) t=title: title of the plot
 - (optional) y=ylabel: label of the y axis
---------------------------------------------------------------------------------
 Required data format: FITS file
 ---------------------------------------------------------------------------------
 Caveats:
 Each optional parameter requires the previous one.
 E.g. you can assign only the title, but if you want to assign the xlabel you need to assign the title.
 
 ---------------------------------------------------------------------------------
 Example:
 python visASTRI_temporal.py astri_000_13_002_00001_F_000009_000_0202.lv0 1 T 1 100 50 50 "t=PDM1 Temperature" "y=T"
 ---------------------------------------------------------------------------------
 Modification history:
 - 2015/09/10: Creation date.
 
"""

import numpy as np
import matplotlib.pylab as plt
import pylab
import sys
import os

import pyfits

# set-up parameters
ASTRI_nPDM = 37
ASTRI_NPixels_PDM = 64
ASTRI_nTemp_PDM = 16
ASTRI_nDT_PDM = 2

title = ''
xlabel = ''
ylabel = ''

# Import the input parameters
arg_list = sys.argv

if (len(arg_list) == 1):
 	print '-------------------------------------------------'
	print 'visASTRI_temporal.py'
	print '----'
	print 'Plotting the temporal curve and graph for the ASTRI DL0 data'
	print 'Author: V. Fioretti (INAF/IASF Bologna)'
	print '----'
	print 'Usage:'
	print 'visASTRI_temporal.py filename selPDM param subfield_id maxevt xvalue_temp xvalue_graph t=title y=ylabel'
 	print '-------------------------------------------------'
 	print 'Parameters:'
 	print '- filename: path + file name of the FITS file'
 	print '- selPDM: the ID of the PDM to be plotted (> 0)'
 	print '- param: name of the parameter to be plotted, using the same convention of the FITS fields. E.g. HI'
 	print '- subfield_id: element (starting from 1) of the sub-array to be plotted (e.g. 1 to select the pixel 1 for HI of PDM).'
 	print '- maxevt: max row (event) to read and plot. If 0 all the events are read.'
 	print '- xvalue_temp: selected x-axis value (element of the array) for which the y-value content must be plotted.'
 	print '- xvalue_graph: selected x-axis value (element of the array) for which the y-value content must be plotted.'
 	print '- (optional) t=title: title of the plot'
 	print '- (optional) y=ylabel: label of the y axis'
 	print '-------------------------------------------------'
 	print 'Example:'
 	print 'python visASTRI_temporal.py astri_000_13_002_00001_F_000009_000_0202.lv0 1 T 1 100 50 50 "t=PDM1 Temperature" y="T"'
 	print '-------------------------------------------------'

else:

	filename = arg_list[1]
	selPDM = int(arg_list[2])
	param = arg_list[3]
	subfield_id = int(arg_list[4])
	maxevt = int(arg_list[5])
	xvalue_temp = int(arg_list[6])
	xvalue_graph = int(arg_list[7])
	if (len(arg_list) > 8): 
		temp_string = arg_list[8]
		if (temp_string[0]=='t'):
			title = temp_string[2:]
		if (temp_string[0]=='y'):
			ylabel = temp_string[2:]
	if (len(arg_list) > 9): 
		temp_string = arg_list[9]
		if (temp_string[0]=='t'):
			title = temp_string[2:]
		if (temp_string[0]=='y'):
			ylabel = temp_string[2:]



	# read the file
	hdulist_astri = pyfits.open(filename)
	events = hdulist_astri[1].data
	cols_events = hdulist_astri[1].columns
	names_events = cols_events.names

	data_column = []
	time_column = []
	row_column = []
	sTIME = 'TIME_S'
	
	# if a PDM has been selected:
	if (selPDM > 0):
		if (selPDM < 10):
			sPDM = 'PDM0'+str(selPDM)+param
		else:
			sPDM = 'PDM'+str(selPDM)+param
		data_column_all = events.field(sPDM)
		time_column_all = events.field(sTIME)
		
		if (maxevt > 0):
			data_column_all = data_column_all[:maxevt]
			time_column_all = time_column_all[:maxevt]
			
		# if on pixel/one temperature sensor is selected
		if (subfield_id > 0):
			for evid in xrange(len(data_column_all)):
				row_data_column = data_column_all[evid]
				time_column.append(time_column_all[evid])
				row_column.append(evid + 1)
				data_column.append(row_data_column[subfield_id-1])

										
		# else if all the sub-array is taken
		else:
			print 'Error! Subfield_id must be > 0.'

	# else if all PDM are taken
	else:
		print 'Error! selPDM must be > 0.'

	yvalue_temp = data_column[xvalue_temp-1]	
	yvalue_graph = data_column[xvalue_graph-1]	

	fig = plt.figure(1,figsize=[10,6])
	ax_temp = fig.add_subplot(121)
	ax_graph = fig.add_subplot(122)


	ax_temp.plot(time_column, data_column, lw = 2)
	ax_graph.plot(row_column, data_column, lw = 2)

	ax_temp.set_xlabel('TIME_S')
	ax_temp.set_ylabel(ylabel)
	ax_temp.set_title(title)
	ax_temp.grid()
	ax_graph.set_xlabel('ROW COUNTER')
	ax_graph.set_ylabel(ylabel)
	ax_graph.set_title(title)
	ax_graph.grid()
	
	ax_temp.text(0.1, 0.9, ylabel+' value ['+str(time_column[xvalue_temp-1])+'] = '+str(yvalue_temp), transform=ax_temp.transAxes, fontsize=12, zorder=100)
	ax_graph.text(0.1, 0.9, ylabel+' value ['+str(row_column[xvalue_graph-1])+'] = '+str(yvalue_graph), transform=ax_graph.transAxes, fontsize=12, zorder=100)

	
	plt.show()


