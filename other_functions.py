"""
Functions we'll need soon:

Compute face normals
Compute local basis for each face
Compute adjacency matrix

"""
import igl
import numpy as np

# input STL file
filename = "challenge/Part.STL"

# vertices and faces
mesh_vertices, mesh_faces = igl.read_triangle_mesh(filename)
mesh_edges = igl.edges(mesh_faces)

# remove duplicate vertices
vertices, faces, VMAP = igl.remove_duplicates(mesh_vertices, mesh_faces, 0.0001)

# get unique edges, no duplicates
edges = igl.edges(faces)

# normal for degenerate face
v = np.array([1,1,1])
degen_normal = v / np.sqrt(np.sum(v**2))

# face normals
normals = igl.per_face_normals(vertices,faces,degen_normal)

# check normals are unit size
for k in range(len(normals)):
    if np.linalg.norm(normals[k]) < 0.95:
        print(k, normals[k], np.linalg.norm(normals[k]))
        raise ValueError('Found normal that is less than unit size')


# local basis for each face
x_bases, y_bases, z_bases = igl.local_basis(vertices, faces)

# vertex adjacency matrix
a = igl.adjacency_matrix(faces)

