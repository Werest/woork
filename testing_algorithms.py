# Наименование метода
# K-Means
# Affinity propagation
# Mean-shift
# Birch
# MiniBatchKMeans
from sklearn.cluster import KMeans
from sklearn.cluster import AffinityPropagation
from sklearn.cluster import MeanShift
from sklearn.cluster import Birch
from sklearn.cluster import MiniBatchKMeans
import pandas as pd
from yellowbrick.cluster import KElbowVisualizer
import numpy as np
import matplotlib.pyplot as plt


def kmm(z):
    model = KMeans()
    vis = KElbowVisualizer(model, k=(1, 15))
    vis.fit(np.array(z))

    k = KMeans(n_clusters=vis.elbow_value_).fit(z)
    x_t = list(k.cluster_centers_[:, 0])
    y_t = list(k.cluster_centers_[:, 1])
    return x_t, y_t


def mbkmm(z):
    model = MiniBatchKMeans()
    vis = KElbowVisualizer(model, k=(1, 15))
    vis.fit(np.array(z))

    k = MiniBatchKMeans(n_clusters=vis.elbow_value_).fit(z)
    x_t = list(k.cluster_centers_[:, 0])
    y_t = list(k.cluster_centers_[:, 1])
    return x_t, y_t


def aff(z):
    af = AffinityPropagation().fit(z)
    x_t = list(af.cluster_centers_[:, 0])
    y_t = list(af.cluster_centers_[:, 1])
    cluster_centers_indices = af.cluster_centers_indices_
    print(cluster_centers_indices)
    return x_t, y_t


def ms(z):
    af = MeanShift().fit(z)
    x_t = list(af.cluster_centers_[:, 0])
    y_t = list(af.cluster_centers_[:, 1])
    return x_t, y_t


def brc(z):
    brc = Birch().fit(z)
    x_t = list(brc.subcluster_centers_[:, 0])
    y_t = list(brc.subcluster_centers_[:, 1])
    return x_t, y_t



def obraz(name):
    img = pd.read_csv('datatest/{}.csv'.format(name))
    x = np.loadtxt('datatest/{}_x.txt'.format(name))
    y = np.loadtxt('datatest/{}_y.txt'.format(name))
    z = [list(hhh) for hhh in zip(x, y)]
    x_t, y_t = kmm(z)
    af_xt, af_yt = aff(z)
    ms_xt, ms_yt = ms(z)
    brc_xt, brc_yt = brc(z)
    mbkmm_xt, mbkmm_yt = mbkmm(z)

    fig, (ax, ax2, ax3, ax4, ax5, ax6) = plt.subplots(nrows=1, ncols=6, figsize=(12, 5),
                                                      sharex=True, sharey=True)
    # ax.axis('on')
    # ax2.axis('on')

    ax.imshow(img)
    ax2.imshow(img)
    ax3.imshow(img)
    ax4.imshow(img)
    ax5.imshow(img)
    ax6.imshow(img)

    fig.suptitle('{}'.format(name), fontsize=16)
    ax.set_title('Original')
    ax2.set_title('Kmeans')
    ax3.set_title('Affinity propagation')
    ax4.set_title('Mean-shift')
    ax5.set_title('Birch')
    ax6.set_title('MiniBatchKMeans')

    ax2.scatter(y_t, x_t, s=5, c='red')
    ax3.scatter(af_yt, af_xt, s=5, c='red')
    ax4.scatter(ms_yt, ms_xt, s=5, c='red')
    ax5.scatter(brc_yt, brc_xt, s=5, c='red')
    ax6.scatter(mbkmm_yt, mbkmm_xt, s=5, c='red')

    plt.savefig('datatest/{}.png'.format(name))


names = ['A1 97_ac', 'A18 111_ac', 'A8_2 76_ac', 'A3 76_ac']
for n in names:
    obraz(n)
