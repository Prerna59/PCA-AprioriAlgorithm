#Submitted By--> Prerna Singh(50249100)
#                Shivani Thakur(50249137)
import numpy as np
import matplotlib.pyplot as plt
from sklearn.manifold import TSNE

def load_dataset(fileLocation):
    #Need to read the last column which is diesease name and rest columns are the features
    #Opening the file for reading 
    # Putting all the values in zeroth column 
    col_num = -1
    diseases = []
    delimiter = "\t"
    cols = 0
    with open(fileLocation, "r") as file:
        data = file.readlines()
        cols = len(data[0].strip().split(delimiter))
        for line in data:
            diseases.append(line.strip().split(delimiter)[col_num])        
    #Getting all the unique disease and assigning unique number to them
    count = 0
    unique_disease = dict()
    for disease in diseases:
        if disease in unique_disease:
            continue
        unique_disease[disease] = count
        count+=1
    #extracting all the disease unique number to plot in different color
    unique_disease_Number = []
    for disease in diseases:
        if(unique_disease[disease] in unique_disease_Number):
            continue
        unique_disease_Number.append(unique_disease[disease])
    # Reading feature matrix further 
    #feature_matrix = np.loadtxt(fileLocation, delimiter="\t", usecols=[0,1,2,3])
    feature_matrix = np.loadtxt(fileLocation, delimiter="\t", usecols = range(cols - 1))
    
    return diseases, unique_disease, unique_disease_Number, feature_matrix
        
#PCA
def PCA(feature_matrix):
    #Adjusted Matrix
    adjMatrix = feature_matrix - feature_matrix.mean(axis = 0) 
    #Covariance of adjusted matrix
    covMatrix = np.cov(adjMatrix.T)
    #Eigen value and Eigen vector
    eigenVal, eigenVec = np.linalg.eig(covMatrix)
    #Finding top n eigen value for principle component, In this case we are finding 2
    # -2 represents the top k values 
    index = eigenVal.argsort()[-2:][::-1]   
    eigenVal_top2 = eigenVal[index]
    eigenVec_top2 = eigenVec[:,index]
    #Need to build priniciple components from n dimensions to two dimensions
    row = feature_matrix.shape[0]
    col = eigenVec_top2.shape[1] # will be two for two dimensions
    pca_mat = np.empty([row,col])
    for i, j in enumerate(eigenVec_top2.T):
        pca_mat[:,i] = np.dot(adjMatrix, j)   
    return pca_mat

#SVD
def svd(feature_matrix):
    U, S, V = np.linalg.svd(feature_matrix)
    svd_mat = U[:, :2]
    return svd_mat

#tSNE
def tSNE(feature_matrix):
    tSNE_mat = TSNE(n_components=2, n_iter = 1000).fit_transform(feature_matrix)
    return tSNE_mat

def plot_graph(fileName, diseases, unique_disease, unique_disease_Number,mat_type):
    #colors = ["r","g","b"]
    #To assign colors needed
    colors = []
    for i in unique_disease_Number:    
        colors.append(plt.cm.jet(float(i) / max(unique_disease_Number)))
    i = 0
    for disease in unique_disease:
        x = []
        for j, p in enumerate(mat_type[:,0]):
            if diseases[j] == disease:
                x.append(p)
        y = []
        for k, p in enumerate(mat_type[:,1]):
            if diseases[k] == disease:
                y.append(p)
        plt.scatter(x, y, c=colors[i], label=str(disease))
        i = i+1 
    plt.title(fileName)
    plt.legend()
    plt.show()
    
def PCA_Graph(fileLocation, fileName):
    diseases, unique_disease, unique_disease_Number,feature_matrix = load_dataset(fileLocation)
    matrix_type = PCA(feature_matrix)
    plot_graph(fileName, diseases, unique_disease, unique_disease_Number,matrix_type)

def SVD_Graph(fileLocation, fileName):
    diseases, unique_disease, unique_disease_Number,feature_matrix = load_dataset(fileLocation)
    matrix_type = svd(feature_matrix)
    plot_graph(fileName, diseases, unique_disease, unique_disease_Number,matrix_type)
    
def tSNE_Graph(fileLocation,fileName):
    diseases, unique_disease, unique_disease_Number,feature_matrix = load_dataset(fileLocation)
    matrix_type = tSNE(feature_matrix)
    plot_graph(fileName, diseases, unique_disease, unique_disease_Number,matrix_type)
    
#PCA Graphs
PCA_Graph("pca_a.txt", "PCA_pca_a")
PCA_Graph("pca_b.txt", "PCA_pca_b")
PCA_Graph("pca_c.txt", "PCA_pca_c")
#SVD Graphs
SVD_Graph("pca_a.txt", "SVD_pca_a")
SVD_Graph("pca_b.txt", "SVD_pca_b")
SVD_Graph("pca_c.txt", "SVD_pca_c")
#tSNE Graphs
tSNE_Graph("pca_a.txt", "tSNE_pca_a")
tSNE_Graph("pca_b.txt", "tSNE_pca_b")
tSNE_Graph("pca_c.txt", "tSNE_pca_c")

# Graphs on demo data
#PCA_Graph("pca_demo.txt")
#SVD_Graph("pca_demo.txt")
#tSNE_Graph("pca_demo.txt")
