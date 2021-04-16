import os
import pickle
from joblib import load
import numpy as np
import json
from flask import jsonify, send_file
from sklearn.decomposition import PCA

UPLOAD_FOLDER = './UPLOADS/'
GNBF = load('files/GNB.pickle')
DCNF = load('files/DCNTree.pickle')
PCAM = load('files/PCA.pickle')

minAge = 10.0
minBMI = 11.5
minGlu = 55.12
maxAge = 82.0
maxBMI = 92.0
maxGlu = 271.74
# maxes and mins found in training program and manually copied over

def normalize(arg1):
    if(arg1[0] == 'Male'):
        arg1[0] = 0
    else:
        arg1[0] = 1
    arg1[1] = (int(arg1[1])-minAge)/(maxAge-minAge)
    arg1[2] = int(arg1[2])
    arg1[3] = int(arg1[3])
    if(arg1[4] == 'Yes'):
        arg1[4] = 1
    else:
        arg1[4] = 0
    if(arg1[5] == 'Rural'):
        arg1[5] = 0
    else:
        arg1[5] = 1
    arg1[6] = (int(arg1[6])-minGlu)/(maxGlu-minGlu)
    arg1[7] = (int(arg1[7])-minBMI)/(maxBMI-minBMI)
    if(arg1[8] in 'smokes'):
        arg1[8] = 1
    elif(arg1[8] in 'formerly smoked'):
        arg1[8] = .5
    else:
        arg1[8] = 0
    return arg1

def MakePredict(arg):
    arg = arg.split(',')
    if(len(arg)!=9):
        return "Invalid inputs: Required inputs are (Male or Female),age,hypertension(1 or 0),heart disease(1 or 0),ever married(Yes or No),residence(Urban or Rural),glucose,BMI,smoking status(formerly, smokes, or never) in that order case-sensitive"
    x = normalize(arg)
    x = np.array(x)
    x = x.reshape(1,-1)
    p = PCAM.transform(x)
    p = p.reshape(1,-1)
    pred = GNBF.predict(p)
    if(pred[0] == 1):
        return "Stroke likely"
    else:
        return "Stroke Unlikely"

def filePred(arg):
    f = request.files['file']
    f.save(UPLOAD_FOLDER + arg)
    fl = open(UPLOAD_FOLDER + arg, 'r')
    lines = fl.readlines()
    results = []
    fl.close()
    for line in lines:
        if len(line) != 9:
            results.apppend('invalid data')
            continue
        results.append(MakePred(line))
    return jasonify(results)

def getTree():
    path = "./files/fig1.pdf"
    return send_file(path,as_attachment=True)


























