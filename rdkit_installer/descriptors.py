import inspect

import pandas as pd
from rdkit import Chem
from rdkit.Chem import Descriptors
from rdkit.ML.Descriptors import MoleculeDescriptors


def calc_descriptors(smiles):
    return calc_400descriptors(smiles)


def calc_208descriptors(smiles):
    desc_names = [x[0] for x in Descriptors._descList if x[0]]
    calc = MoleculeDescriptors.MolecularDescriptorCalculator(desc_names)

    matrix = []
    for smile in smiles:
        row = []
        mol = Chem.MolFromSmiles(smile)
        for d in calc.CalcDescriptors(mol):
            row.append(d)
        matrix.append(row)
        if len(matrix)%1000 == 0:
            print("{} smiles processed in calc_208descriptors...".format(len(matrix)))

    return pd.DataFrame(matrix, columns=desc_names)


def calc_400descriptors(smiles):
    matrix = []
    for smile in smiles:
        row = []
        mol = Chem.MolFromSmiles(smile)
        desc_names = []
        for desc_name in inspect.getmembers(Descriptors, inspect.isfunction):
            desc_name = desc_name[0]
            if desc_name.startswith("_"):
                continue
            if desc_name == "setupAUTOCorrDescriptors":
                continue
            row.append(getattr(Descriptors, desc_name)(mol))
            desc_names.append(desc_name)
        matrix.append(row)
        if len(matrix)%1000 == 0:
            print("{} smiles processed in calc_400descriptors...".format(len(matrix)))

    return pd.DataFrame(matrix, columns=desc_names)
