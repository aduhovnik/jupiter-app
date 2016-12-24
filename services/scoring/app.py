#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import os
from pickle import loads
from zipfile import ZipFile
from flask import Flask
from pandas import DataFrame


app = Flask(__name__)

data_path = 'data'
file_name = 'classifier.pkl'


zip_path = os.path.join(data_path, file_name + '.zip')
with ZipFile(zip_path, 'r') as a:
    data = a.read(file_name)
    scoring_obj = loads(data)


@app.route('/api/credits/scoring')
def scoring():
    return type(scoring_obj).__name__


def get_score(data_dict):
    """
    RevolvingUtilizationOfUnsecuredLines
    age
    NumberOfTime30-59DaysPastDueNotWorse
    DebtRatio
    MonthlyIncome
    NumberOfOpenCreditLinesAndLoans
    NumberOfTimes90DaysLate
    NumberRealEstateLoansOrLines
    NumberOfTime60-89DaysPastDueNotWorse
    NumberOfDependents
    :param data_dict:
        'credit_monthly_payments': []
        'credits_residue': float except real estate and car loans
        'MonthlyIncome': float
        'NumberOfTimes90DaysLate': int
        'NumberOfDependents': int
        'NumberOfTime30-59DaysPastDueNotWorse': int
        'NumberOfTime60-89DaysPastDueNotWorse' : int
        'age': int
        'NumberRealEstateLoansOrLines': int
        'credit_limits': []  except real estate and car loans
    :return:
    """
    data_dict['debtRatio'] = (sum(data_dict['credit_monthly_payments'])) / data_dict['MonthlyIncome']
    data_dict['RevolvingUtilizationOfUnsecuredLines'] = data_dict['credits_residue'] / sum(data_dict['credit_limits'])
    del data_dict['credit_monthly_payments']
    del data_dict['credits_residue']
    del data_dict['credit_limits']
    pd_data = DataFrame().from_dict(data_dict)
    score = scoring_obj.predict_proba(pd_data)
    return score[0][0]


def main():
    app.run('0.0.0.0', port=8001)


if __name__ == '__main__':
    main()
