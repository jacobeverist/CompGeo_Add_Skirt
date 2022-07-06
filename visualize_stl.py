"""
Visual a mesh with an interactive web plot

"""

import igl
import meshplot

# turn off jupyter interactive environment
meshplot.offline()

# input STL file
filename = "challenge/Part.STL"

# vertices and faces
vertices, faces = igl.read_triangle_mesh(filename)

# plot mesh to an interactive HTML page
meshplot.plot(vertices, faces, filename="meshview.html")

print("open file 'meshview.html' in your browser")



