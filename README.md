# CompGeo_Add_Skirt Challenge

---

# Code
`visualize_stl.py`: Visual a mesh with an interactive web plot

`find_perimeter.py`: Find perimeter edges of the mesh

`other_functions.py`: Functions we'll need soon (face normals, local basis, adjacency matrix)

# Purpose
This README explains the approach I would use to solve the [CompGeo_Add_Skirt challenge](https://github.com/Machina-Labs/CompGeo_Add_Skirt).  Implementation would entail a lot of work beyond 2-4 hours so we just outline our development approach instead.


# Approach
Solving and coding computational geometry problems are particularly difficult because they are very prone to pernicious and undetectable errors during development.  Because of this, care must be taken during development to break down the solution into pieces and build upon solid foundations.  Furthermore, checking the validity of your data at each intermediate step of your solution helps isolate and diagnose errors.

The solution should be built on a foundation of valid assumptions and mathematically correct algorithms.  Given this foundation, heuristic solutions can then be applied with relative freedom since we can have confidence that the foundational code and data is correct and reliable.

Therefore, it makes sense to spend a lot of time analyzing and planning how to approach the problem.  We break down the problem into the below components.

## Definitions
- Define any special terms being used (vertex, edge, face, perimeter, etc.)
- Define the problem
- Define input
- Define output
- Define any constraints
- Define optimality

## Assumptions
- Collect any assumptions that are stated or hidden with the problem statement
- Add further assumptions to reduce the scope of your problem to something manageable
- Add assumptions at each intermediate step of your solution

## Validation Functions
- Create functions to check the validity of each assumption.  
- Apply appropriate validation function to each step of the algorithm

## Correct Algorithms
- Create a library of primitive functions that are "correct" under the given assumptions
- Should be mathematically correct with a written proof
- Use software libraries or literature proofs as much as possible
- Avoid writing your own proofs since that's a rabbit hole you don't need to go down

## Heuristics
- Develop heuristic solutions with correct primitives and valid data.
- Optimize solution based on desired constraints
- Humans evaluate effectiveness of solution visually

---

# Solution

The components of our solution are described below.

## Definitions

### Problem
At the high level, the problem is taking in an input STL file, adding a skirt to the mesh representing the part, and outputing a new STL file.
 

### Terms
A **vertex** is a point in 3D cartesian space.  An **edge** is a line segment defined by two vertices.  A **face** is a triangle (for this problem) defined by 3 edges that form a cycle.

A **mesh** is a collection of vertices, edges, and faces.  The original mesh is denoted $M_1$.

A **perimeter** is a cycle of edges that are each adjacent to only one face.  It follows that every vertex on a perimeter is adjacent to two faces.  The perimeter of $M_1$ is denoted $C_1$.  Every vertex on a perimeter is connected to at least 3 edges (is this true?).

The **skirt** is an appendage of mesh, $M_2$, along the perimeter $C_1$, that terminates on the z=0 plane.  The resulting composite mesh, $M_3$ has a new perimeter $C_3$ completely on the z=0 plane.    

The **wall angle** is the angle between a face on the skirt perimeter $C_3$ and the z=0 plane.

The **skirt angle** is the angle between the mesh $M_1$ and the skirt $M_2$ along a face on the perimeter $C_1$.

A **ray** is part of a line with a starting point but no ending point.  It is defined by an origin and a direction.

### Constraints
- The new perimeter $C_3$ will be located on the z=0 plane.
- The wall angle will be $\leq 70$ degrees.

### Optimality
Although not specified, we claim the following metrics should be minimized to create an optimal solution.

- The mesh should be centered in the neighborhood of the z-axis. 
- The wall angle should be minimized.
- The skirt angle should be minimized.  ($0$ degrees is acceptable)
- The surface area of the skirt should be minimized.


## Assumptions

### Stated in Problem
We assume the input STL file is valid and well-formed.

We assume all vertices are in the negative z space.

We assume the input mesh is well-formed with the following properties:
- each face is a triangle
- each vertex has at least 2 connected edges
- each edge has at least one adjacent face
- no duplicate vertices, edges, or faces
- no edge intersects another edge
- no face intersects another face

### Scope Reduction
We assume the input mesh has at least one perimeter.   To simplify the problem, we also assume that the mesh has only one perimeter.  That is, we assume that there are no holes in the input mesh.  In the future we would consider parts with holes.

We assume we have infinite material for the skirt.   For this case, we do not consider limitations of the material size or operational space.  Therefore, there is no limitation of vertices in the x and y direction.


### Intermediate 
- We assume that the new skirt perimeter $C_3$ is contained on the z=0 plane. 


## Validation Functions
We will need the following functions to validate the data prior to algorithmic operations:

### Initial
- Function to validate well-formed STL
- Function to validate input mesh is well-formed
- Function to validate vertices are all $\leq 0$ along z-axis
- Function to validate there is one and only one perimeter

### Intermediate
- Function to validate that the skirt perimeter is on the z=0 plane

## Correct Algorithms

### Custom Algorithms
We will need the following correct primitive function:
- Retrieve the perimeter of a mesh
- Translate mesh
- Rotate mesh about an origin 
- Find plane defined by origin and two vectors
- Find intersection point between a ray and plane
- Rotate a ray along a plane

### Libraries
We can use CGAL or libigl for data structures and classical computaional geometry algorithms.

## Heuristics

We propose the following heuristic operations to solve the skirt problem:

### Center the Part
- Translate the mesh in the x-y direction so that it is centered along the z-axis.

### Orient the Part
- Create a set of rays $R_1$ such that their origins are the center points of the edges on the perimeter $C_1$, are perpendicular to the edges, and are coplanar to the each edge's adjacent face.  .
- Rotate the mesh such that the maximum number of rays in $R_1$ intersect the z=0 plane and that the length between each ray's origin and its intersection point is minimized.

### Create an Infinite Skirt
- For each vertex $v_i$ on the perimeter $M_1$ with adjacent edges $e_i$ and $e_{i+1}$, create a set of rays $R_2$ with origins $v_i$ and the direction being the sum of directions of $e_i$ and $e_{i+1}$ into $v_1$.

### Connect Skirt to z=0 Plane
- Rotate each ray $r_i$ in $R_2$ along the plane defined by the vector of $r_i$ and the normal $n_i$ of the plane defined by $e_i$ and $e_{i+1}$.
- Rotate until $r_i$ intersects z=0 plane, and that the angle between $r_1$ and z=0 plane is less than $70$ degrees.  

### Create Extension Mesh
- Create vertices $w_i$ from the intersection point of the rays in $R_1$ with z=0 plane.
- Create edges defined by the origin vertex $v_i$ of a ray $r_i$ and its corresponding intersection vertex $w_i$
- Create perimeter edges defined by $w_i$ and $w_{i+1}$ along z=0 plane in same order as the $C_1$ perimeter vertices
- Create edge between $v_i$ and $w_{i+1}$ to form two triangle faces from rectangle.
- New skirt perimeter $C_3$ is defined by vertices $w_i$ and edges defined by $w_i$ and $w_{i+1}$.
- Validate skirt perimeter is on z=0 plane.

## Discussion
This solution ensures wall angle constraint is met but doesn't consider any factors such as smoothness, ease of manufacturability, material usage, operational space, or skirt angle.

We have determined correctness of the solution since the problem is currently not mathematically well-defined.  Suitability of the solutions generated will need to be determined by human evaluation.

Errors in the approach may exist and will need to be discovered after coding.  Debugging will be easier given the foundations of correctness and validated data.











