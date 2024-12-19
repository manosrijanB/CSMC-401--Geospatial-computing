
# Terrain and Canopy Modeling Using Triangle-PR-Quadtree

## Project Overview

This project involves the development of terrain and canopy models using LiDAR (Light Detection and Ranging) point clouds and Triangulated Irregular Networks (TINs). The primary focus is on implementing and applying the Triangle PR-quadtree data structure to model terrain features and forest canopy structures for two different domains: bathymetric (seabed) analysis and forest canopy analysis.

The project is divided into two main parts:

1. **First Part**: The goal is to compute a TIN from a set of terrain points and implement a Triangle PR-quadtree to efficiently store and query the terrain data. The key tasks in this part involve:
    - Computing a TIN using a function from the Scipy library.
    - Implementing the Triangle PR-quadtree data structure and its related algorithms for data insertion and traversal.
   
2. **Second Part**: The Triangle PR-quadtree is applied to two different datasets: bathymetric data for seabed analysis and LiDAR data for forest canopy analysis. Tasks in this part include:
    - **Seabed Modeling**: Analyze the seabed using bathymetric data, compute terrain features like roughness and curvature, and identify critical points like maxima and minima.
    - **Forest Canopy Modeling**: Analyze LiDAR point clouds to create a canopy model and detect tree tops using local maxima filtering.

## Objectives

- **Terrain Modeling**: Use LiDAR point clouds to create a model representing the terrain surface, including the computation of morphological features such as roughness and curvature.
- **Canopy Modeling**: Use LiDAR point clouds to create a canopy model and detect tree tops (maxima) within a forest canopy, which is crucial for forest monitoring and carbon stock estimation.
- **Triangle PR-Quadtree Data Structure**: Implement this new data structure for efficient spatial indexing and queries on terrain and canopy data, enhancing performance for large datasets.

## Project Requirements

### Tools and Libraries
- **Python**: Used for implementing the project and running the algorithms.
- **Scipy**: Library for computational geometry to compute the TIN from the point cloud data.
- **Matplotlib**: For visualizing the results in 3D.
- **NumPy**: Used for numerical computations such as computing roughness and curvature.

### Input Data
- **Bathymetric Data**: A `.pts` file containing the bathymetric data points representing the seabed.
- **Canopy Data**: A `.pts` file containing the LiDAR data points for the canopy.

### Output
- **Text Files**: Contains the computed values for roughness, curvature, and maxima.
- **Images**: Visual representations of the TIN models with roughness, curvature, and maxima marked, including 3D visualizations.
  
## Workflow

1. **Part One**: 
    - Compute a TIN from the provided points using Scipy.
    - Implement the Triangle PR-quadtree data structure and insert the TIN into it.
    - Traverse the quadtree and print its contents.

2. **Part Two**:
    - **Seabed Analysis**:
        - Compute roughness and curvature for each vertex of the TIN.
        - Identify and visualize critical points such as maxima and minima.
    - **Forest Canopy Analysis**:
        - Construct a TIN from the LiDAR data points.
        - Use local maxima filtering to detect tree tops (maxima).
        - Visualize the results in 3D and mark the tree tops.

### Outputs
- Bathymetric data with color-coded roughness and curvature.
- Visualization of maxima for both seabed and canopy models.
- Text files for roughness, curvature, and maxima, along with their corresponding visualizations.

## Key Concepts

### Triangle PR-Quadtree
- The Triangle PR-quadtree is a spatial indexing structure that allows for efficient storage and querying of points and triangles from the TIN.
- The quadtree recursively subdivides the space into quadrants, and each leaf node stores a set of vertices and triangles.

### Roughness and Curvature
- **Roughness** is computed as the standard deviation of local elevations around each vertex.
- **Curvature** is calculated using the angles of triangles at each vertex to estimate how much the surface deviates from being flat.

### Local Maxima Detection
- Local maxima correspond to the highest points in a region, such as tree tops in a forest canopy or high points in a seabed. These are important for tasks like tree detection or analyzing seabed landforms.

## Known Challenges and Considerations

- **Data Distribution**: The performance of the Triangle PR-quadtree is sensitive to the distribution of the points in space, which could affect query performance and accuracy.
- **Complexity of Implementation**: The implementation of the Triangle PR-quadtree and the algorithms for roughness, curvature, and maxima detection can be complex and require significant computational resources, especially for large datasets.
- **Visualization**: Generating clear and accurate 3D visualizations is essential for interpreting the results of the modeling tasks, which can be resource-intensive.

## How to Run the Program

To run the program successfully, ensure that the directory is set to **"provided_code_project"**. Open the terminal and execute the following commands for the respective tasks:

### For Task 1: Seabed Analysis (Bathymetric Data)

python3 main_test_demo.py ./data_part_II/test_bathymetric.pts 100

### For Task 2: Forest Canopy Analysis (LiDAR Data)

python3 main_test_demo.py ./data_part_II/test_chm.pts 100

### Explanation:
Command Structure: Replace ./data_part_II/test_bathymetric.pts or ./data_part_II/test_chm.pts with the correct path to the input .pts file.
Capacity: The number 100 indicates the capacity for the images. You can adjust this number as per your requirements.
Executing these commands will generate the output images for the respective data sets. Ensure that the correct file paths and capacity are provided for accurate results.

## Conclusion
This project combines computational geometry, data structure design, and practical applications in environmental science and forestry. The use of the Triangle PR-quadtree enhances the performance of handling large datasets, making it an efficient tool for terrain and canopy modeling. The project provides valuable insights into seabed and forest structure analysis, with applications in marine navigation and forest management. """
