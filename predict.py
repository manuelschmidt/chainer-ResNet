#!/usr/bin/env python
# -*- coding: utf-8 -*-

from chainer import serializers
from chainer import Variable
from skimage import io
from skimage import transform

import argparse
import numpy as np

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', type=str, default='ResNet152')
    parser.add_argument('--img', type=str, default='cat.png')
    args = parser.parse_args()

    if args.model == 'ResNet152':
        from ResNet152 import ResNet
    elif args.model == 'ResNet101':
        from ResNet101 import ResNet
    elif args.model == 'ResNet50':
        from ResNet50 import ResNet

    img = io.imread(args.img)
    img = transform.resize(img, (224, 224))
    if img.shape[-1] > 3:
        img = img[:, :, :3]
    img = img[:, :, ::-1] * 255

    x_data = img.transpose(2, 0, 1).astype(np.float32)[np.newaxis, :, :, :]
    x_data = Variable(x_data)

    model = ResNet()
    serializers.load_hdf5(args.model + '.model', model)

    model.train = False
    pred = model(x_data, None).data

    f = open('data/synset_words.txt')
    line = f.read().split('\n')[:-1]
    f.close()

    for i in np.argsort(pred)[0][-1::-1][:5]:
        print(line[i])
