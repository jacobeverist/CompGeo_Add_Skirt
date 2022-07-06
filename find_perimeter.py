"""
Find perimeter edges of the mesh.

"""

import igl
import numpy as np

# input STL file
filename = "challenge/Part.STL"

# vertices and faces
mesh_vertices, mesh_faces = igl.read_triangle_mesh(filename)
mesh_edges = igl.edges(mesh_faces)
print("MESH GRAPH")
print("mesh vertices:", len(mesh_vertices))
print("mesh faces:", len(mesh_faces))
print("mesh edges:", len(mesh_edges))
print()

# remove duplicate vertices
vertices, faces, VMAP = igl.remove_duplicates(mesh_vertices, mesh_faces, 0.0001)

print("DUPLICATES REMOVED")
print("unique vertices:", len(vertices))
print("unique faces:", len(faces))
#for k in range(len(vertices)):
#    print(k, VMAP[k], mesh_vertices[k], vertices[VMAP[k]])

# get unique edges, no duplicates
edges = igl.edges(faces)
print("unique edges:", len(edges))
print()

# unique edge map
# E #F*3 by 2 list of all directed edges, such that E.row(f+#F*c) is the
# edge opposite F(f,c)
# uE #uE by 2 list of unique undirected edges
# EMAP #F*3 list of indices into uE, mapping each directed edge to unique
# undirected edge so that uE(EMAP(f+#F*c)) is the unique edge
# corresponding to E.row(f+#F*c)
# uE2E #uE list of lists of indices into E of coexisting edges, so that
# E.row(uE2E[i][j]) corresponds to uE.row(i) for all j in
# 0..uE2E[i].size()-1.
E, uE, EMAP, uE2E = igl.unique_edge_map(faces)

# find edges that were referenced once
perim_edges = []
for k in range(len(uE2E)):
    if len(uE2E[k]) == 1:
        perim_edges += [k,]

# convert to numpy array
perim_edges = np.array(perim_edges)


print("SHARED EDGES")
print("directed edges:", len(E))
print("unique undirected edges:", len(uE))
print("perim edges:", len(perim_edges))
print()

# print found perimeter edgers
#print(perim_edges)
#print(uE[perim_edges])

# TODO: check hypothesis that all edges used once are perimeter edges and they form a cycle











