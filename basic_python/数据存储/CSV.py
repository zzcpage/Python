import csv
def csvWrite():
    headers = ['ID','UserName','Password','Age','Country']
    rows = [
        {1001,"qiye","qiye_pass",24,"China"},
        {1002,"Mary","Mary_pass",20,"USA"},
        {1003,"Jack","Jack_pass",20,"USA"}
    ]
    # rou里面也可以是字典数据类型
    with open('qiye.csv','w') as f:
        f_csv = csv.writer(f)
        f_csv.writerow(headers)
        f_csv.writerows(rows)
def csvReader():
    with open('qiye.csv') as f:
        f_csv = csv.reader(f)
        headers = next(f_csv)
        print(headers)
        for row in f_csv:
            print(row)