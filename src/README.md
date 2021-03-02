# Model Exploration and Results

The general workflow that I'm following is shown below:

![Machine Learning Pipeline](../images/Other/Machine%20Learning%20Pipeline.png)

## Experiments

### Generate Functional Connectivity

After preprocessing all of the fMRI data, I had to convert the data into a compressed representation for the machine learning models to handle. Example representations include functional connectivity (FC) and intersubject correlation (ISC). To generate the FCs of subjects, I used Nilearn.

#### Scripts

- [Testing](../src/Functional%20Connectivity/Testing%20FC.ipynb)
- [Generate Power FC](../src/Functional%20Connectivity/Generate%20Power%20FC.ipynb)
- [Generate Yeo FC](../src/Functional%20Connectivity/Generate%20Yeo%20FC.ipynb)

There are two generation scripts because depending on how you cut up the brain, you can get different FCs. However, the general FC generation steps are as follows:

1. Provide the program with a set of coordinates (such as Power or Yeo).
2. For each coordinate, generate a sphere around that coordinate and average the time series signal in that sphere.
3. For each sphere, calculate the correlation between every other sphere.
4. Store the correlations in a matrix.

#### Results

Generating a functional connectivity from the Power's atlas yields this matrix:

![Functional Connectivity Matrix](../images/Functional%20Connectivity/FC%20Matrix.png)

For this matrix, each row and column is a node in the Power's atlas, which has 264 nodes. So, this means each cell in the matrix is the correlation strength between each node and the rest of the nodes in the atlas (self/recurrent connections are ignored and are set to zero). One issue with this atlas is that each node isn't easily labeled so determining which connections are stronger/weaker is difficult compared to a labeled atlas like Yeo. A more interpretable representation of the FC matrix is the correlation graph superimposed onto a brain as shown below:

![Functional Connectivity Correlation Graph](../images/Functional%20Connectivity/FC%20Correlation%20Graph.png)

This visualization makes it easier to map node location to brain area but without thresholding the connection strength, it becomes too much to handle.

### Unsupervised

After the FCs are generated, I didn't have access to the labels (cognitive measures) so I tried some unsupervised models. This included testing PCA, ICA, K-means, and t-SNE and then back-projecting the transformed data back into an FC. This was somewhat successful and the results are shown below.

#### Scripts

- [Data Exploration](../src/Unsupervised/Data%20Exploration.ipynb)
- [Derive Spatial Maps](../src/Unsupervised/Derive%20Spatial%20Maps.ipynb)

#### Results

When I run the PCA on the FC data, I decide how many components/dimensions to reduce the data to. In this case, I choose three for ease of visualization. The first PCA component can explain ~20% of the variance in the data and by back-projecting it as an FC matrix, I get this:

![PCA FC Matrix](../images/Unsupervised/PCA%20FC%20Matrix.png)
![PCA Correlation Graph](../images/Unsupervised/PCA%20Correlation%20Graph.png)

This matrix is the first PCA component meaning these are the connections that explain ~20% of the variance in the data. In other words, 20% of the differences in the data that we see can be explained by these connections (since each PCA component places a weight on each connection so the greater the weight, the greater the contribution of that connection to explaining the variance). If I run a different dimensionality reduction technique, such as ICA, I get these results:

![ICA FC Matrix](../images/Unsupervised/ICA%20FC%20Matrix.png)
![ICA Correlation Graph](../images/Unsupervised/ICA%20Correlation%20Graph.png)

The same as for PCA, this matrix is the first ICA component back-projected into FC matrix space. However, instead of each connection/cell weight representing that connection's contribution to explained variance as in PCA, each connection in ICA represents it's contribution to an independent component/network in the data. This is more tricky to interpret but I've moved on from it.

### Data Sanity Check

While matching subjects to labels, I performed some quick sanity checks to ensure the data was ok.

#### Scripts

- [Label Exploration](../src/Supervised/Label%20Exploration.ipynb)

#### Results

My sanity checks mostly consist of checking the data distribution for imbalances in ages/IQ and doing a quick check on age vs IQ.

![Age Distribution](../images/Data%20Distribution/Age%20Distribution.png)
![IQ Distribution](../images/Data%20Distribution/IQ%20Distribution.png)
![Age vs IQ](../images/Data%20Distribution/Age%20vs%20IQ.png)

### Supervised

Once I had the labels, I performed a matching between subjects and labels to get the subjects with labels (not all subjects had labels, and vice versa). After this, I tried various supervised models to tease out any link between FC and cognitive score (IQ). I didn't find any promising results as shown below. The Python scripts:

#### Scripts

- [Linear Models](../src/Supervised/Linear%20Models.ipynb)

#### Results

![PCR](../images/Supervised/Linear%20Models/PCR.png)
![PLS](../images/Supervised/Linear%20Models/PLS.png)
![Variance Threshold](../images/Supervised/Linear%20Models/Variance%20Threshold.png)
![Mutual Information](../images/Supervised/Linear%20Models/Mutual%20Information.png)
