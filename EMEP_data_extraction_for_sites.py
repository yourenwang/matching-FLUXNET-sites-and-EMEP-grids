import numpy as np
import netCDF4

year = 20XX # any year between 2000 and 2014
EMEP_file = 'C:\\your_own_directory\\EMEP01_L20EC_rv4_33_year.'+str(year)+'met_'+str(year)+'emis_rep2019.nc'

site_info = open('C:\\your_own_directory\\site_lat_lon.txt','r')

site_name = []
for i in range(23):site_name.append(0)
site_lat = np.zeros(23)
site_lon = np.zeros(23)
nearest_grid_in_lat_for_site = np.zeros(23)
nearest_grid_in_lon_for_site = np.zeros(23)

site_n = 0
for line in site_info:
	contents = line.split()
	site_name[site_n] = contents[0]
	site_lat[site_n] = contents[1]
	site_lon[site_n] = contents[2]
	site_n += 1
site_info.close()


grid_data = netCDF4.Dataset(EMEP_file)
grid_lat  = grid_data.variables['lat'][:]
grid_lon  = grid_data.variables['lon'][:]

n_lat_points = len(grid_lat)
n_lon_points = len(grid_lon)

total_SOX = grid_data.variables['DDEP_SOX_m2Grid'][:,:,:] + grid_data.variables['WDEP_SOX'][:,:,:] 
total_OXN = grid_data.variables['DDEP_OXN_m2Grid'][:,:,:] + grid_data.variables['WDEP_OXN'][:,:,:] 
total_RDN = grid_data.variables['DDEP_RDN_m2Grid'][:,:,:] + grid_data.variables['WDEP_RDN'][:,:,:]

	
for i in range(0, site_n):		
	for j in range(0, n_lat_points-1):
		if (site_lat[i] - grid_lat[j])*(site_lat[i] - grid_lat[j+1]) > 0:
			pass
		else: 
			if abs(site_lat[i] - grid_lat[j]) < abs(site_lat[i] - grid_lat[j+1]):
				nearest_grid_in_lat_for_site[i] = j
			else:
				nearest_grid_in_lat_for_site[i] = j+1
			break	

for i in range(0, site_n):		
	for j in range(0, n_lon_points-1):
		if (site_lon[i] - grid_lon[j])*(site_lon[i] - grid_lon[j+1]) > 0:
			pass
		else: 
			if abs(site_lon[i] - grid_lon[j]) < abs(site_lon[i] - grid_lon[j+1]):
				nearest_grid_in_lon_for_site[i] = j
			else:
				nearest_grid_in_lon_for_site[i] = j+1
			break	


f_output = open('C:\\your_own_directory\\EMEP_deposition_in_'+str(year)+'.csv','w') 
print >> f_output, 'Site_name', 'Site_lat', 'Site_lon', 'Nearest_grid_Lat', 'Nearest_grid_Lon', 'Nearest_grid_SOX', 'Nearest_grid_OXN', 'Nearest_grid_RDN'
for t in range(0, site_n):	
	print >> f_output, site_name[t], site_lat[t], site_lon[t], grid_lat[nearest_grid_in_lat_for_site[t]], grid_lon[nearest_grid_in_lon_for_site[t]], \
	      total_SOX[0, nearest_grid_in_lat_for_site[t], nearest_grid_in_lon_for_site[t]], \
		  total_OXN[0, nearest_grid_in_lat_for_site[t], nearest_grid_in_lon_for_site[t]], \
		  total_RDN[0, nearest_grid_in_lat_for_site[t], nearest_grid_in_lon_for_site[t]]

f_output.close()	
