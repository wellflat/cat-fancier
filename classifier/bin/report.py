#!/usr/local/bin/python
# -*- coding: utf-8 -*-

import os
import matplotlib.pyplot as plt
import numpy as np

# cm = [[44,  1,  0,  0,  3,  1,  0,  0,  1,  2,  1,  1],
#       [ 1, 52,  0,  0,  0,  3,  2,  0,  0,  0,  0,  0],
#       [ 0,  0, 43,  0,  0,  0,  0,  0,  5,  0,  4,  0],
#       [ 0,  0,  0, 54,  0,  0,  1,  0,  0,  0,  0,  0],
#       [ 1,  0,  0,  0, 32,  1,  0,  1,  0,  4,  0,  1],
#       [ 0,  1,  0,  1,  2, 36,  0,  0,  0,  0,  0,  0],
#       [ 1,  6,  0,  0,  0,  1, 42,  6,  1,  0,  0,  0],
#       [ 0,  0,  0,  1,  0,  0,  3, 34,  2,  0,  0,  0],
#       [ 0,  0, 11,  0,  0,  0,  0,  4, 32,  0,  0,  0],
#       [ 0,  0,  0,  1,  7,  0,  0,  0,  0, 52,  0,  1],
#       [ 0,  0,  3,  0,  0,  0,  0,  0,  1,  0, 45,  0],
#       [ 1,  1,  0,  0,  0,  0,  0,  0,  0,  1,  0, 44]]

# cm = [[40,  2,  0,  0,  0,  1,  2,  0,  0,  2,  0,  2],
#       [ 5, 39,  0,  0,  0,  0,  1,  0,  0,  1,  0,  0],
#       [ 0,  0, 34,  0,  1,  0,  0,  1,  4,  0,  8,  0],
#       [ 0,  0,  0, 48,  0,  0,  0,  0,  0,  1,  0,  1],
#       [ 2,  1,  0,  0, 39,  0,  0,  3,  0,  4,  0,  1],
#       [ 0,  8,  0,  0,  2, 41,  0,  0,  0,  3,  0,  0],
#       [ 3,  5,  0,  2,  0,  1, 38,  1,  2,  0,  0,  0],
#       [ 0,  0,  0,  0,  0,  1,  5, 35,  1,  0,  0,  0],
#       [ 0,  0,  8,  0,  0,  0,  1,  3, 41,  0,  2,  0],
#       [ 2,  0,  1,  1,  5,  0,  0,  0,  0, 46,  0,  0],
#       [ 0,  0,  7,  0,  0,  0,  1,  0,  1,  0, 38,  4],
#       [ 1,  0,  0,  0,  0,  0,  0,  0,  0,  1,  0, 46]]

if __name__ == '__main__':
    os.chdir(os.path.dirname(__file__))
    
    cmfilename = '../data/svm_rbf_cm.npy'
    cm = np.load(cmfilename)
    norm = []
    for i in cm:
        a = 0
        tmp = []
        a = sum(i, 0)
        for j in i:
            tmp.append(float(j)/float(a))
        norm.append(tmp)
    
    fig = plt.figure(figsize=(6,4))
    print(fig)
    plt.clf()
    ax = fig.add_subplot(111)
    ax.set_aspect(1)
    res = ax.imshow(np.array(norm), cmap=plt.cm.jet, interpolation='nearest')

    width = len(cm)
    height = len(cm[0])

    for x in xrange(width):
        for y in xrange(height):
            ax.annotate(str(cm[x][y]), xy=(y, x),
                        horizontalalignment='center',
                        verticalalignment='center')

    # show confusion matrix
    #plt.title('cat classification (linear)')
    plt.title('cat classification (rbf)')
    plt.colorbar(res)
    labels = ['Abyssinian', 'Bengal', 'Birman', 'Bombay', 'British_Shorthair', 'Egyptian_Mau', 'Maine_Coon', 'Persian', 'Ragdoll', 'Russian_Blue', 'Siamese', 'Sphynx']
    #plt.xticks(range(width), labels[:width], fontsize=10)
    plt.yticks(range(height), labels[:height], fontsize=10)
    plt.tick_params(labelbottom="off")
    plt.show()
    resultfile = '../tmp/cm.png'
    plt.savefig(resultfile)
    print('save ok: %s' % (resultfile,))
