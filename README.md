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
- The prefix of each customer_id must be 'id'. For example, if the input of customer id for the 1st row is '1200', an error will be raised. Instead, 'id1200' is accepted.

| customer_id | txn_date | ... |
| ---         | ---      | --- |
| ID233 | 2018-01-01 | ... |
| ... | ... | ... |



