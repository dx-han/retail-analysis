# -*- coding: UTF-8 -*-
import json
import sys

def main(jsonfile,sqlfile):

    f = open(jsonfile,'r')
    length = 0
    for line in f:
        length += 1


    newf = open(sqlfile,'a')
    
    ######
    # you must change the following syntax
    insert = 'INSERT INTO `blackmores_retention` (`month`,`total`,`first_product_name_format`,`day_90`,`day_180`,`day_360`)'
    ######
    
    _add = '\nVALUES\n'
    insert = insert + _add

    i = 0
    f = open(jsonfile, 'r')
    for line in f:
        dt = json.loads(line)

        ######
        # you must change the following syntax
        data = [dt['month'], dt['total'],
                dt['first_product_name_format'],
                str(dt['day_90']),str(dt['day_180']),str(dt['day_360'])]
        ######
        # print(data)
        if i == length-1: break
        if i % 10000 == 0:
            newf.write(insert)
            tmp = str(tuple(data))
            newf.write(tmp + ',\n')
            i += 1
        else:
            if (i+1)%10000!=0:
                tmp = str(tuple(data))
                newf.write(tmp + ',\n')
                i += 1
            else:
                tmp = str(tuple(data))
                newf.write(tmp + ';\n')
                i += 1

    tmp = str(tuple(data))
    newf.write(tmp + ';\n')
    newf.write('\nUNLOCK TABLES;\n')


if __name__ == '__main__':
    # main(sys.argv[1],sys.argv[2])
    main('retention_order_reducer.json','sql模版.sql')
