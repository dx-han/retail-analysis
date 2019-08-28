# Retail Analysis
Several valuable directions of data analysis in retail industry.

## Table of Contents
[Retention (Matrix) Analysis](#retention-(matrix)-analysis)

## Retention (Matrix) Analysis

Input Requirements

- File type: csv
- Column name: customer_id, txn_date, other dimensions which map each customer

Attention

- The format of txn_date must be Year-Month-Day (%Y-%m-%d) without any information about hour, minute, and second
- I highly recommend adding 'ID' in front of each customer_id. For some automatically-convenient reasons, pandas will read number as int/float even though they are stored as string in the csv file. To ensure the format of customer_id is string, adding 'ID' will be safe and no error will be caused during the calculation.

Structure of Input

| customer_id | txn_date | ... |
| ---         | ---      | --- |
| ID233 | 2018-01-01 | ... |
| ... | ... | ... |

Usage
```
python run.py --filename data/test --periods 30,60,90 --nature-periods 1,2,3
```
where *data/test* means a csv file named test located in a relative-position folder called data, *periods* means the length of intervals by days, *nature-periods* means the length of intervals by nature months.
