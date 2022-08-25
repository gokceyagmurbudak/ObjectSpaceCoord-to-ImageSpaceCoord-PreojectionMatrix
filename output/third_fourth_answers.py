import math
import numpy as np
import pandas as pd
import matplotlib.image as mpimg
import matplotlib.pyplot as plt

# I opened the image 106.jp2

img=mpimg.imread("C:/Users/HP/Desktop/midterm_foto_gor_ana/code/106.jpg")

exterior_orientation=np.array([[1,0,0,-497312.996],
                              [0,1,0,-5419477.065],
                              [0,0,1,-1158.888],
                              [0,0,0,1]])
# convert from gon to degree
omega_d = -0.481059 #-0.53451 gon
phi_d   = -0.171225 #-0.19025 gon
kappa_d = -0.121401 #-0.13489 gon

# convert from degree to radian

omega=np.deg2rad(omega_d)
phi=np.deg2rad(phi_d)
kappa=np.deg2rad(kappa_d)

# matrix representation of rotation matrix
# np.cos or np.sin use radian as unit

R=np.array([[np.cos(phi)*np.cos(kappa)+np.sin(phi)*np.sin(omega)*np.sin(kappa),np.cos(omega)*np.sin(kappa),-np.sin(phi)*np.cos(kappa)+np.cos(phi)*np.sin(omega)*np.sin(kappa),0],
            [-np.cos(phi)*np.sin(kappa)+np.sin(phi)*np.sin(omega)*np.cos(kappa),np.cos(omega)*np.cos(kappa),np.sin(phi)*np.sin(kappa)+np.cos(phi)*np.sin(omega)*np.cos(kappa),0],
            [np.sin(phi)*np.cos(omega),-np.sin(omega),np.cos(omega)*np.cos(phi),0],
            [0,0,0,1]])

# matrix representation of pixel coordinates
pixel_coordinate = np.array([[6912],
                             [3840],
                             [10000]])
# matrix representation of interior orientation
interior_orientation = np.array([[-120/0.012,0,3840,0],
                                 [0,120/0.012,6912,0],
                                 [0,0,1,0]])

# first part of projection matrix equation with homogenous matrix 
perspective_projection=np.matmul(interior_orientation,R)
perspective_projection2=np.matmul(perspective_projection,exterior_orientation)
#print(perspective_projection2)

# To show the world coordinates, we read the point data 
#   and the id information of those points in the excel file.  
excel_data_df = pd.read_excel('x_y_z_id.xlsx', sheet_name='x_y_z_id', usecols=['x_coord','y_coord','osm_way_id','z_coord'])


        
# To show x, y and z coordinates in the excel file
df = pd.DataFrame(excel_data_df, columns= ['x_coord','y_coord','z_coord'])
df2= pd.DataFrame(excel_data_df, columns= ['osm_way_id'])


id_=df2.values.reshape(1389,1)
a = df.values.reshape(1389,3) # x,y,z world coordinates

# We obtained the u and v pixel values 
  # by multiplying the world coordinates with our projection matrix.
      # The camera cooridinarte is 3 dimensions.To obtain u and v,
       # We divide the first and second matrix row by the third row.
camera_coordinate_list=[]
u=[]
v=[]
x_y_z=[]
for i in range(0,1389):
    A= [a[i][0],a[i][1],a[i][2],1]
    camera_coordinate=np.matmul(perspective_projection2,A)
    camera_coordinate2=camera_coordinate.tolist()
    camera_coordinate_list.append(camera_coordinate2)
    u_0=camera_coordinate2[0]/camera_coordinate2[2]
    v_0=camera_coordinate2[1]/camera_coordinate2[2]
    u.append(u_0)
    v.append(v_0)
    x_y_z.append(A)


camera_coordinate_array=np.array(camera_coordinate_list).reshape(1389,3)
k=np.array([u,v])

# I had null value for id value, solution is..
for i in range (1389):
    if math.isnan(id_[i]):
        id_[i]=0
        
# I ploted u and v values and conditions is that id values are the same because
 # Each point must draw its own polygons, otherwise the drawing process continues 
  # until the number of points is finished. 
for i in range(0,1388):
    if id_[i]==id_[i+1]:
        plt.plot([u[i],u[i+1]], [v[i],v[i+1]],'ro--',markersize=5)
    else:
        i = i+1
        plt.plot([u[i],u[i+1]], [v[i],v[i+1]],'ro--',markersize=5)



    
#to show finished image.  

imgplot = plt.imshow(img)

plt.show(imgplot)


