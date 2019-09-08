import pandas as pd
import os
import time
from datetime import datetime

path = "E:/hiru/works/ml/project1/intraQuarter"


def key_stats(gather="Total Debt/Equity (mrq)"):
    stats_path = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(stats_path)]
    # print(stock_list)
    df = pd.DataFrame(columns=['Date', 'Unix', 'Ticker', 'DE Ratio'])

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        # each file get file names
        ticker = each_dir.split("\\")[1]

        if len(each_file) > 0:
            for file in each_file:
                # date_stamp get the date and time from the file
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                # print(date_stamp, unix_time)
                full_file_path = each_dir+'/'+file
                #print(full_file_path)
                source = open(full_file_path, 'r').read()
                #print(source)
                try:
                    value = float(source.split(gather + ':</td><td class="yfnc_tabledata1">')[1].split('</td>')[0])
                    df = df.append({'Date':date_stamp,'Unix':unix_time, 'Ticker':ticker, 'DE Ratio':value }, ignore_index=True)
                except Exception as e:
                    pass
                #get the totle deb of each company for each file
                #print(ticker + ":", value)

    save = gather.replace(' ','').replace(')','').replace('(','').replace('/','')+str('.csv')
    print(save)
    df.to_csv(save)


key_stats()
