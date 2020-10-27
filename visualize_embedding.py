import matplotlib.pyplot as plt
from sklearn.manifold import locally_linear_embedding
import pandas as pd
import pdb
import argparse

def parse_args():
    parser = argparse.ArgumentParser(description='Circle plots')
    parser.add_argument('--input_path', type=str, default='results/lle_circles.csv',
                        help='input path')
    return parser.parse_args()

def plot_embedding(args):
    output = pd.read_csv(args.input_path)
    y = output['y']
    output.drop(['y'], 1, inplace=True)
    d = output.shape[1]
    X = output.values
    # plot resulting embedding in 2d or 3d
    if d == 2:
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.scatter(X[:, 0], X[:, 1], c=y, cmap=plt.cm.Spectral)
        plt.title('Embedding of Circles Dataset via LLE')
        plt.savefig('results/lle_circles.png', dpi=300)

if __name__ == "__main__":
    args = parse_args()
    plot_embedding(args=args)