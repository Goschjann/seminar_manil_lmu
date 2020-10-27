import matplotlib.pyplot as plt
from sklearn.manifold import locally_linear_embedding
import pandas as pd
import pdb

# read data
data = pd.read_csv('circle_data/rawdata_circle.csv')
y = data['y']
data.drop(['y'], axis=1, inplace=True)
X = data.values

# fit lle with output
d = 2
X_r, err = locally_linear_embedding(X,
                                    n_neighbors=12,
                                    n_components=d)
print("Reconstruction error: %g" % err)

# store the output in the required format
output = pd.DataFrame(X_r)
output.columns = [f'x_{idx}' for idx in range(X_r.shape[1])]
output['y'] = y
output.to_csv('results/lle_circles.csv', index=False)
