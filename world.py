# Creation of the synthetic dataset of the world
# blog post: https://towardsdatascience.com/tsne-degrades-to-pca-d4abf9ef51d3
# github repo: https://github.com/NikolayOskolkov/tSNELargePerplexityLimit

import cartopy
import os
import pdb
import matplotlib
import numpy as np
import pandas as pd
import cartopy.crs as ccrs
import matplotlib.pyplot as plt
import cartopy.feature as cfeature
import argparse
import cartopy.io.shapereader as shpreader
import shapely.wkt as wkt
import shapely

from shapely.geometry import MultiPolygon
from skimage.io import imread
from mpl_toolkits import mplot3d

def parse_args():
    parser = argparse.ArgumentParser(description='world')
    parser.add_argument('--n', type=int, default=10000,
                        help='amount of sampels to randomly draw, final size ~= n / 4 as 71percent of the earth is water')
    return parser.parse_args()

# helper function to plot single countries and later use this
# data for the final world data set
def plot_single_continents():
    shapename = 'admin_0_countries'
    countries_shp = shpreader.natural_earth(resolution='110m',
                                            category='cultural',
                                            name=shapename)

    plt.figure(figsize = (20, 15))
    ax = plt.axes(projection=ccrs.Miller())
    ax.outline_patch.set_visible(False)
    #ax.set_extent([-180, 180, -50, 70])
    for country in shpreader.Reader(countries_shp).records():
        # print(country.attributes['NAME_LONG'])
        if country.attributes['NAME_LONG'] in ['United States','Canada']:#, 'Mexico']:
            name = country.attributes['NAME_LONG']
            try:
                ax.add_geometries(country.geometry, ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            except:
                ax.add_geometries([country.geometry], ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            plt.savefig('NorthAmerica.png')
    plt.close()

    plt.figure(figsize = (20, 15))
    ax = plt.axes(projection=ccrs.Miller())
    ax.outline_patch.set_visible(False)
    #ax.set_extent([-180, 180, -50, 70])
    for country in shpreader.Reader(countries_shp).records():
        if country.attributes['NAME_LONG'] in ['Brazil','Argentina', 'Peru', 'Uruguay', 'Venezuela',
                                            'Columbia', 'Bolivia', 'Colombia', 'Ecuador', 'Paraguay']:
            name = country.attributes['NAME_LONG']
            try:
                ax.add_geometries(country.geometry, ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            except:
                ax.add_geometries([country.geometry], ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            plt.savefig('SouthAmerica.png')
    plt.close()

    plt.figure(figsize = (20, 15))
    ax = plt.axes(projection=ccrs.Miller())
    ax.outline_patch.set_visible(False)
    #ax.set_extent([-180, 180, -50, 70])
    for country in shpreader.Reader(countries_shp).records():
        if country.attributes['NAME_LONG'] in ['Australia']:
            name = country.attributes['NAME_LONG']
            try:
                ax.add_geometries(country.geometry, ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            except:
                ax.add_geometries([country.geometry], ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            plt.savefig('Australia.png')
    plt.close()


    plt.figure(figsize = (20, 15))
    ax = plt.axes(projection=ccrs.Miller())
    ax.outline_patch.set_visible(False)
    #ax.set_extent([-180, 180, -50, 70])
    for country in shpreader.Reader(countries_shp).records():
        if country.attributes['NAME_LONG'] in ['Russian Federation', 'China', 'India', 'Kazakhstan', 'Mongolia',
                                            'France', 'Germany', 'Spain', 'Ukraine', 'Turkey', 'Sweden',
                                            'Finland', 'Denmark', 'Greece', 'Poland', 'Belarus', 'Norway',
                                            'Italy', 'Iran', 'Pakistan', 'Afganistan', 'Iraq', 'Bulgaria',
                                            'Romania', 'Turkmenistan', 'Uzbekistan' 'Austria', 'Ireland',
                                            'United Kingdom', 'Saudi Arabia', 'Hungary']:
            name = country.attributes['NAME_LONG']
            try:
                ax.add_geometries(country.geometry, ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            except:
                ax.add_geometries([country.geometry], ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            plt.savefig('Eurasia.png')
    plt.close()


    plt.figure(figsize = (20, 15))
    ax = plt.axes(projection=ccrs.Miller())
    ax.outline_patch.set_visible(False)
    #ax.set_extent([-180, 180, -50, 70])
    for country in shpreader.Reader(countries_shp).records():
        if country.attributes['NAME_LONG'] in ['Libya', 'Algeria', 'Niger', 'Marocco', 'Egypt', 'Sudan', 'Chad',
                                            'Democratic Republic of the Congo', 'Somalia', 'Kenya', 'Ethiopia',
                                            'The Gambia', 'Nigeria', 'Cameroon', 'Ghana', 'Guinea', 'Guinea-Bissau',
                                            'Liberia', 'Sierra Leone', 'Burkina Faso', 'Central African Republic',
                                            'Republic of the Congo', 'Gabon', 'Equatorial Guinea', 'Zambia',
                                            'Malawi', 'Mozambique', 'Angola', 'Burundi', 'South Africa',
                                            'South Sudan', 'Somaliland', 'Uganda', 'Rwanda', 'Zimbabwe', 'Tanzania',
                                            'Botswana', 'Namibia', 'Senegal', 'Mali', 'Mauritania', 'Benin',
                                            'Nigeria', 'Cameroon']:
            name = country.attributes['NAME_LONG']
            print(f'{name}')
            try:
                ax.add_geometries(country.geometry, ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            except:
                ax.add_geometries([country.geometry], ccrs.Miller(), label=country.attributes['NAME_LONG'], color = 'black')
            plt.savefig('Africa.png')
    plt.close()

def create_world_dataset(args):

    if not os.path.exists('world_data'):
        os.mkdir('world_data')

    plot_single_continents()
    rng = np.random.RandomState(123)
    plt.figure(figsize = (20, 11.5))
    matplotlib.rcParams.update({'font.size': 22})

    N_NorthAmerica = args.n
    data_NorthAmerica = imread('NorthAmerica.png')[::-1, :, 0].T
    X_NorthAmerica = rng.rand(4 * N_NorthAmerica, 2)
    i, j = (X_NorthAmerica * data_NorthAmerica.shape).astype(int).T
    X_NorthAmerica = X_NorthAmerica[data_NorthAmerica[i, j] < 1]
    X_NorthAmerica = X_NorthAmerica[X_NorthAmerica[:, 1]<0.67]
    y_NorthAmerica = np.array(['brown']*X_NorthAmerica.shape[0])
    plt.scatter(X_NorthAmerica[:, 0], X_NorthAmerica[:, 1], c = 'brown', s = 50)

    N_SouthAmerica = args.n
    data_SouthAmerica = imread('SouthAmerica.png')[::-1, :, 0].T
    X_SouthAmerica = rng.rand(4 * N_SouthAmerica, 2)
    i, j = (X_SouthAmerica * data_SouthAmerica.shape).astype(int).T
    X_SouthAmerica = X_SouthAmerica[data_SouthAmerica[i, j] < 1]
    y_SouthAmerica = np.array(['red']*X_SouthAmerica.shape[0])
    plt.scatter(X_SouthAmerica[:, 0], X_SouthAmerica[:, 1], c = 'red', s = 50)

    N_Australia = args.n
    data_Australia = imread('Australia.png')[::-1, :, 0].T
    X_Australia = rng.rand(4 * N_Australia, 2)
    i, j = (X_Australia * data_Australia.shape).astype(int).T
    X_Australia = X_Australia[data_Australia[i, j] < 1]
    y_Australia = np.array(['darkorange']*X_Australia.shape[0])
    plt.scatter(X_Australia[:, 0], X_Australia[:, 1], c = 'darkorange', s = 50)

    N_Eurasia = args.n
    data_Eurasia = imread('Eurasia.png')[::-1, :, 0].T
    X_Eurasia = rng.rand(4 * N_Eurasia, 2)
    i, j = (X_Eurasia * data_Eurasia.shape).astype(int).T
    X_Eurasia = X_Eurasia[data_Eurasia[i, j] < 1]
    X_Eurasia = X_Eurasia[X_Eurasia[:, 0]>0.5]
    X_Eurasia = X_Eurasia[X_Eurasia[:, 1]<0.67]
    y_Eurasia = np.array(['blue']*X_Eurasia.shape[0])
    plt.scatter(X_Eurasia[:, 0], X_Eurasia[:, 1], c = 'blue', s = 50)

    N_Africa = args.n
    data_Africa = imread('Africa.png')[::-1, :, 0].T
    X_Africa = rng.rand(4 * N_Africa, 2)
    i, j = (X_Africa * data_Africa.shape).astype(int).T
    X_Africa = X_Africa[data_Africa[i, j] < 1]
    y_Africa = np.array(['darkgreen']*X_Africa.shape[0])
    plt.scatter(X_Africa[:, 0], X_Africa[:, 1], c = 'darkgreen', s = 50)

    plt.title('World Map Data Set', fontsize = 25)
    plt.savefig('world_data/world_2d.png')

    # concatenate to one global (hrhr) data set
    data_list = []
    continents = ['africa', 'australia', 'eurasia', 'northamerica', 'southamerica']
    for name, data in zip(continents,[X_Africa, X_Australia, X_Eurasia, X_NorthAmerica, X_SouthAmerica]):
        # pdb.set_trace()
        temp = pd.DataFrame({'x_1': data[:, 0],
                             'x_2': data[:, 1],
                             'y': [name for _ in range(data.shape[0])]})
        data_list.append(temp)
    world_data = pd.concat(data_list, axis=0)
    world_data.to_csv('world_data/rawdata_world_2d.csv', index=False)
    print(f'Gathered world data with {world_data.shape[0]} lon/lat samples')

    # Inverse-Map to 3D space
    p = world_data['x_1'].values * (3 * np.pi - 0.6)
    t = world_data['x_2'].values * np.pi

    x_sphere = np.sin(t) * np.cos(p)
    y_sphere = np.sin(t) * np.sin(p)
    z_sphere = np.cos(t)

    world_3d = pd.DataFrame({'x_1': x_sphere,
                             'x_2': y_sphere,
                             'x_3': z_sphere,
                             'y': world_data['y'].values})
    world_3d.to_csv('world_data/rawdata_world_3d.csv', index=False)
    print(f'Gathered world data with {world_data.shape[0]} 3-dimensional samples')

    def country2int(country):
        if country == 'africa':
            return 1
        elif country == 'australia':
            return 2
        elif country == 'eurasia':
            return 3
        elif country == 'northamerica':
            return 4
        elif country == 'southamerica':
            return 5


    # plot 3d
    plt.figure(figsize=(20,15))
    ax = plt.axes(projection = '3d')
    ax.view_init(10, 60)
    ax.scatter3D(world_3d['x_1'], world_3d['x_2'], - world_3d['x_3'],
                 c = [country2int(country) for country in world_3d['y']])
    plt.title('World Map Data Set', fontsize = 25)
    plt.savefig('world_data/world_3d.png')


    # clean intermediate plots
    os.system('rm NorthAmerica.png SouthAmerica.png Eurasia.png Australia.png Africa.png')

if __name__ == '__main__':
    args = parse_args()
    create_world_dataset(args)