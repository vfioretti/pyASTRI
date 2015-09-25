"""
 visASTRI_histo.py  -  description
 ---------------------------------------------------------------------------------
 Plotting the histograms for the ASTRI DL0 data
 ---------------------------------------------------------------------------------
 copyright            : (C) 2015 Valentina Fioretti
 email                : fioretti@iasfbo.inaf.it
 ----------------------------------------------
 Usage:
 visASTRI_histo.py filename selPDM param subfield_id nbins minval maxval maxevt binx t=title x=xlabel y=ylabel  
 ---------------------------------------------------------------------------------
 Parameters:
 - filename: path + file name of the FITS file
 - selPDM: the ID of the PDM to be plotted. If selPDM = 0 all the PDMs are plotted.
 - param: name of the parameter to be plotted, using the same convention of the FITS fields. E.g. HI
 - subfield_id: element (starting from 1) of the sub-array to be plotted (e.g. 1 to select the pixel 1 for HI of PDM).
 				 If subfield_id = 0 all the sub-array is plotted
 - nbins: number of bins for the histogram
 - minval: minimum value to create the histogram
 - maxval: maximum value to create the histogram
 - maxevt: max row (event) to read and plot. If 0 all the events are read.
 - binx: selected x-axis value index (starting from 0) for which the bin content must be plotted.
 - (optional) t=title: title of the plot
 - (optional) x=xlabel: label of the x axis
 - (optional) y=ylabel: label of the y axis
 ---------------------------------------------------------------------------------
 Required data format: FITS file
 ---------------------------------------------------------------------------------
 Caveats:
 Each optional parameter requires the previous one.
 E.g. you can assign only the title, but if you want to assign the xlabel you need to assign the title.
 
 ---------------------------------------------------------------------------------
 Example:
 python visASTRI_histo.py astri_000_11_111_11111_R_000000_000_0201.lv0 1 HI 0 100 800 1400 0 "t=PDM 01 HG histo" "x=ADC counts" "y=N" 
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
	print 'visASTRI_histo.py'
	print '----'
	print 'Plotting the histograms for the ASTRI DL0 data'
	print 'Author: V. Fioretti (INAF/IASF Bologna)'
	print '----'
	print 'Usage:'
	print 'visASTRI_histo.py filename selPDM param subfield_id nbins minval maxval maxevt binx t=title x=xlabel y=ylabel'
 	print '-------------------------------------------------'
 	print 'Parameters:'
 	print '- filename: path + file name of the FITS file'
 	print '- selPDM: the ID of the PDM to be plotted. If selPDM = 0 all the PDMs are plotted.'
 	print '- param: name of the parameter to be plotted, using the same convention of the FITS fields. E.g. HI'
 	print '- subfield_id: element (starting from 1) of the sub-array to be plotted (e.g. 1 to select the pixel 1 for HI of PDM).'
 	print '			      If subfield_id = 0 all the sub-array is plotted.'
 	print '- nbins: number of bins for the histogram'
 	print ' - minval: minimum value to create the histogram'
 	print ' - maxval: maximum value to create the histogram'
 	print ' - maxevt: max row (event) to read and plot. If 0 all the events are read.'
 	print ' - binx: selected x-axis value index (starting from 0) for which the bin content must be plotted.'
 	print ' - (optional) t=title: title of the plot'
 	print ' - (optional) x=xlabel: label of the x axis'
 	print ' - (optional) y=ylabel: label of the y axis'
 	print '-------------------------------------------------'
 	print 'Example:'
 	print 'python visASTRI_histo.py astri_000_11_111_11111_R_000000_000_0201.lv0 1 HI 0 100 800 1400 0 900 "t=PDM 01 HG histo" "x=ADC counts" "y=N"'
 	print '-------------------------------------------------'

else:

	filename = arg_list[1]
	selPDM = int(arg_list[2])
	param = arg_list[3]
	subfield_id = int(arg_list[4])
	nbins = int(arg_list[5])
	minval = int(arg_list[6])
	maxval = int(arg_list[7])
	maxevt = int(arg_list[8])
	binx = int(arg_list[9])
	if (len(arg_list) > 10): 
		temp_string = arg_list[10]
		if (temp_string[0]=='t'):
			title = temp_string[2:]
		if (temp_string[0]=='x'):
			xlabel = temp_string[2:]
		if (temp_string[0]=='y'):
			ylabel = temp_string[2:]	
	if (len(arg_list) > 11): 
		temp_string = arg_list[11]
		if (temp_string[0]=='t'):
			title = temp_string[2:]
		if (temp_string[0]=='x'):
			xlabel = temp_string[2:]
		if (temp_string[0]=='y'):
			ylabel = temp_string[2:]
	if (len(arg_list) > 12): 	
		temp_string = arg_list[12]
		if (temp_string[0]=='t'):
			title = temp_string[2:]
		if (temp_string[0]=='x'):
			xlabel = temp_string[2:]
		if (temp_string[0]=='y'):
			ylabel = temp_string[2:]

	# read the file
	hdulist_astri = pyfits.open(filename)
	events = hdulist_astri[1].data
	cols_events = hdulist_astri[1].columns
	names_events = cols_events.names


	tot_data_column = []
	data_column = []
	#square_data_column = []
	
	# if a PDM has been selected:
	if (selPDM > 0):
		if (selPDM < 10):
			sPDM = 'PDM0'+str(selPDM)+param
		else:
			sPDM = 'PDM'+str(selPDM)+param
		data_column_all = events.field(sPDM)
		if (maxevt > 0):
			data_column_all = data_column_all[:maxevt]
			
		# if on pixel/one temperature sensor is selected
		if (subfield_id > 0):
			for evid in xrange(len(data_column_all)):
				row_data_column = data_column_all[evid]
				tot_data_column.append(row_data_column[subfield_id-1])
				if (minval==0):
					if (row_data_column[subfield_id-1] < maxval):
						data_column.append(row_data_column[subfield_id-1])
						#square_data_column.append((row_data_column[subfield_id-1])**2.)
				else:
					if ((row_data_column[subfield_id-1] > minval) & (row_data_column[subfield_id-1] < maxval)):
						data_column.append(row_data_column[subfield_id-1])
						#square_data_column.append((row_data_column[subfield_id-1])**2.)
		# else if all the sub-array is taken
		else:
			for evid in xrange(len(data_column_all)):
				if (data_column_all[evid].size > 1):
					row_data_column = data_column_all[evid]
					for jcol in xrange(len(row_data_column)):
						tot_data_column.append(row_data_column[jcol])
						if (minval==0):
							if (row_data_column[jcol] < maxval):
								data_column.append(row_data_column[jcol])
								#square_data_column.append((row_data_column[jcol])**2.)
						else:
							if ((row_data_column[jcol] > minval) & (row_data_column[jcol] < maxval)):
								data_column.append(row_data_column[jcol])
								#square_data_column.append((row_data_column[jcol])**2.)		
				else:
					row_data_column = data_column_all[evid]
					tot_data_column.append(row_data_column)
					if (minval==0):
						if (row_data_column < maxval):
							data_column.append(row_data_column)
							#square_data_column.append((row_data_column[jcol])**2.)
					else:
						if ((row_data_column > minval) & (row_data_column < maxval)):
							data_column.append(row_data_column)
							#square_data_column.append((row_data_column[jcol])**2.)								
	# else if all PDM are taken
	else:

		for jid in xrange(ASTRI_nPDM):
			single_data_column = []
			tot_single_data_column = []
			#single_square_data_column = []
			if ((jid+1) < 10):
				sPDM = 'PDM0'+str(jid+1)+param
			else:
				sPDM = 'PDM'+str(jid+1)+param
			
			single_data_column_all = events.field(sPDM)
			if (maxevt > 0):
				single_data_column_all = single_data_column_all[:maxevt]

			if (subfield_id > 0):
				for evid in xrange(len(single_data_column_all)):
					row_data_column = single_data_column_all[evid]
					tot_single_data_column.append(row_data_column[subfield_id-1])
					if (minval==0):
						if (row_data_column[subfield_id-1] < maxval):
							single_data_column.append(row_data_column[subfield_id-1])
							#single_square_data_column.append((row_data_column[subfield_id-1])**2.)
					else:
						if ((row_data_column[subfield_id-1] > minval) & (row_data_column[subfield_id-1] < maxval)):
							single_data_column.append(row_data_column[subfield_id-1])
							#single_square_data_column.append((row_data_column[subfield_id-1])**2.)
												
				for jev in xrange(len(single_data_column)):
					data_column.append(single_data_column[jev])
				for jev in xrange(len(tot_single_data_column)):
					tot_data_column.append(tot_single_data_column[jev])
							
			else:
				for evid in xrange(len(single_data_column_all)):
					if (single_data_column_all[evid].size > 1):
						row_data_column = single_data_column_all[evid]
						for jcol in xrange(len(row_data_column)):
							tot_single_data_column.append(row_data_column[jcol])
							if (minval==0):
								if (row_data_column[jcol] < maxval):
									single_data_column.append(row_data_column[jcol])
									#single_square_data_column.append((row_data_column[jcol])**2.)
							else:
								if ((row_data_column[jcol] > minval) & (row_data_column[jcol] < maxval)):
									single_data_column.append(row_data_column[jcol])
									#single_square_data_column.append((row_data_column[jcol])**2.)
					else:
						row_data_column = single_data_column_all[evid]
						tot_single_data_column.append(row_data_column)
						if (minval==0):
							if (row_data_column < maxval):
								single_data_column.append(row_data_column)
								#single_square_data_column.append((row_data_column[jcol])**2.)
						else:
							if ((row_data_column > minval) & (row_data_column < maxval)):
								single_data_column.append(row_data_column)
								#single_square_data_column.append((row_data_column[jcol])**2.)												
				for jev in xrange(len(single_data_column)):
					data_column.append(single_data_column[jev])
				for jev in xrange(len(tot_single_data_column)):	
					tot_data_column.append(tot_single_data_column[jev])

		data_column = np.array(data_column)
		tot_data_column = np.array(tot_data_column)
		#square_data_column = np.array(square_data_column)
				




	N_counts, bin_array = np.histogram(data_column, bins = nbins, range=(minval, maxval))
	x_array = np.zeros(len(N_counts))
	err_x_array = np.zeros(len(N_counts))

	for jn in xrange(len(N_counts)):
			err_x_array[jn] = (bin_array[jn+1] - bin_array[jn])/2.
			x_array[jn] = bin_array[jn]
	
	valx = N_counts[binx-1]



	fig = plt.figure(1,figsize=[10,7])
	ax = fig.add_subplot(111)


	ax.bar(x_array, N_counts, width=2.*err_x_array, edgecolor='blue', facecolor='blue', lw = 1)


	# analysis results
	N_entries = len(tot_data_column)
	mean_out = np.mean(data_column)
	#rms_out = np.sqrt((1./N_entries)*np.sum(square_data_column))
	sd_out = np.std(data_column)
	
	plt.text(0.6, 0.8, 'Entries = '+str(N_entries), transform=ax.transAxes, fontsize=12, zorder=100)
	plt.text(0.6, 0.75, 'Mean = '+str(round(mean_out, 1)), transform=ax.transAxes, fontsize=12, zorder=100)
	plt.text(0.6, 0.7, 'RMS = '+str(round(sd_out, 1)), transform=ax.transAxes, fontsize=12, zorder=100)
	plt.text(0.6, 0.65, 'Bin content ['+str(binx)+'] = '+str(valx), transform=ax.transAxes, fontsize=12, zorder=100)

	ax.set_xlabel(xlabel)
	ax.set_ylabel(ylabel)
	ax.set_title(title)
	ax.grid()
	plt.show()


