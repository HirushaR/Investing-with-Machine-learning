import pandas as pd
import os
import time
from datetime import datetime
from time import mktime
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import style
style.use("dark_background")
import re

path = "E:/hiru/works/ml/project1/intraQuarter"


def Key_Stats(gather=["Total Debt/Equity" ,
                      'Trailing P/E' ,
                      'Price/Sales' ,
                      'Price/Book' ,
                      'Profit Margin' ,
                      'Operating Margin' ,
                      'Return on Assets' ,
                      'Return on Equity' ,
                      'Revenue Per Share' ,
                      'Market Cap' ,
                      'Enterprise Value' ,
                      'Forward P/E' ,
                      'PEG Ratio' ,
                      'Enterprise Value/Revenue' ,
                      'Enterprise Value/EBITDA' ,
                      'Revenue' ,
                      'Gross Profit' ,
                      'EBITDA' ,
                      'Net Income Avl to Common ' ,
                      'Diluted EPS' ,
                      'Earnings Growth' ,
                      'Revenue Growth' ,
                      'Total Cash' ,
                      'Total Cash Per Share' ,
                      'Total Debt' ,
                      'Current Ratio' ,
                      'Book Value Per Share' ,
                      'Cash Flow' ,
                      'Beta' ,
                      'Held by Insiders' ,
                      'Held by Institutions' ,
                      'Shares Short (as of' ,
                      'Short Ratio' ,
                      'Short % of Float' ,
                      'Shares Short (prior ']):
    stats_path = path + '/_KeyStats'
    stock_list = [x[0] for x in os.walk(stats_path)]
    # print(stock_list)
    df = pd.DataFrame(columns=['Date' ,
                               'Unix' ,
                               'Ticker' ,
                               'Price' ,
                               'stock_p_change' ,
                               'SP500' ,
                               'sp500_p_change' ,
                               'Difference' ,
                               ##############
                               'DE Ratio' ,
                               'Trailing P/E' ,
                               'Price/Sales' ,
                               'Price/Book' ,
                               'Profit Margin' ,
                               'Operating Margin' ,
                               'Return on Assets' ,
                               'Return on Equity' ,
                               'Revenue Per Share' ,
                               'Market Cap' ,
                               'Enterprise Value' ,
                               'Forward P/E' ,
                               'PEG Ratio' ,
                               'Enterprise Value/Revenue' ,
                               'Enterprise Value/EBITDA' ,
                               'Revenue' ,
                               'Gross Profit' ,
                               'EBITDA' ,
                               'Net Income Avl to Common ' ,
                               'Diluted EPS' ,
                               'Earnings Growth' ,
                               'Revenue Growth' ,
                               'Total Cash' ,
                               'Total Cash Per Share' ,
                               'Total Debt' ,
                               'Current Ratio' ,
                               'Book Value Per Share' ,
                               'Cash Flow' ,
                               'Beta' ,
                               'Held by Insiders' ,
                               'Held by Institutions' ,
                               'Shares Short (as of' ,
                               'Short Ratio' ,
                               'Short % of Float' ,
                               'Shares Short (prior ' ,
                               ##############
                               'Status'])

    sp500_df = pd.DataFrame.from_csv("YAHOO-INDEX_GSPC.csv.txt")
    # sp500_df = pd.read_csv("YAHOO-INDEX_GSPC.csv")
    tiker_list = []

    for each_dir in stock_list[1:]:
        each_file = os.listdir(each_dir)
        # each file get file names
        ticker = each_dir.split("\\")[1]
        tiker_list.append(ticker)

        starting_stock_value = False
        starting_sp500_value = False

        if len(each_file) > 0:
            for file in each_file:
                # date_stamp get the date and time from the file
                date_stamp = datetime.strptime(file, '%Y%m%d%H%M%S.html')
                unix_time = time.mktime(date_stamp.timetuple())
                # print(date_stamp, unix_time)
                full_file_path = each_dir + '/' + file
                # print(full_file_path)
                source = open(full_file_path, 'r').read()
                # print(source)
                try:
                    value_list =[]

                    for each_data in gather:

                        try:
                            regex = re.escape(each_data) + r'.*?(\d{1,8}\.\d{1,8}M?B?|N/A)%?</td>'
                            value = re.search(regex, source)
                            value = (value.group(1))

                            if "B" in value:
                                value = float(value.replace("B",''))*1000000000
                            elif "M" in value:
                                value = float(value.replace("M" , '')) * 1000000
                            value_list.append(value)

                        except Exception as e:
                            value = "N/A"
                            value_list.append(value)

                    try:
                        sp500_date = datetime.fromtimestamp(unix_time).strftime('%y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adjusted Close"])
                    except:
                        # 259200 is 3 days 60*60*60*24*3
                        sp500_date = datetime.fromtimestamp(unix_time - 259200).strftime('%y-%m-%d')
                        row = sp500_df[(sp500_df.index == sp500_date)]
                        sp500_value = float(row["Adj Close"])
                    try:
                        stock_price = float(source.split('</small><big><b>')[1].split('</b></big>')[0])
                        # print("stock_price:", stock_price, "Ticker:",ticker)
                    except Exception as e:
                        #  <span id = "yfs_l10_aep" > 39.52 </span>
                        try:
                            stock_price = (source.split('</small><big><b>')[1].split('</b></big>')[0])
                            stock_price = re.search(r'(\d{1,9}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            #print(stock_price)
                            time.sleep(15)
                        except Exception as e:
                            stock_price = (source.split('<span class="time_rtq_ticker">')[1].split('</span>')[0])
                            stock_price = re.search(r'(\d{1,9}\.\d{1,8})', stock_price)
                            stock_price = float(stock_price.group(1))
                            # print('latest',stock_price)
                            # print('stock price', str(e),ticker,file)
                            # time.sleep(15)
                    # print(str(e), ticker, file)

                    if not starting_stock_value:
                        starting_stock_value = stock_price
                    if not starting_sp500_value:
                        starting_sp500_value = sp500_value

                    stock_p_change = (stock_price - starting_stock_value) / starting_stock_value * 100
                    sp500_p_change = (sp500_value - starting_sp500_value) / starting_sp500_value * 100
                    difference = stock_p_change - sp500_p_change

                    if difference > 0:
                        status = "outperform"
                    else:
                        status = "underperform"

                    if value_list.count("N/A") > 0:
                        pass
                    else:

                        df = df.append({'Date': date_stamp ,
                                        'Unix': unix_time ,
                                        'Ticker': ticker ,

                                        'Price': stock_price ,
                                        'stock_p_change': stock_p_change ,
                                        'SP500': sp500_value ,
                                        'sp500_p_change': sp500_p_change ,
                                        'Difference': difference ,
                                        'DE Ratio': value_list[0] ,
                                        # 'Market Cap':value_list[1],
                                        'Trailing P/E': value_list[1] ,
                                        'Price/Sales': value_list[2] ,
                                        'Price/Book': value_list[3] ,
                                        'Profit Margin': value_list[4] ,
                                        'Operating Margin': value_list[5] ,
                                        'Return on Assets': value_list[6] ,
                                        'Return on Equity': value_list[7] ,
                                        'Revenue Per Share': value_list[8] ,
                                        'Market Cap': value_list[9] ,
                                        'Enterprise Value': value_list[10] ,
                                        'Forward P/E': value_list[11] ,
                                        'PEG Ratio': value_list[12] ,
                                        'Enterprise Value/Revenue': value_list[13] ,
                                        'Enterprise Value/EBITDA': value_list[14] ,
                                        'Revenue': value_list[15] ,
                                        'Gross Profit': value_list[16] ,
                                        'EBITDA': value_list[17] ,
                                        'Net Income Avl to Common ': value_list[18] ,
                                        'Diluted EPS': value_list[19] ,
                                        'Earnings Growth': value_list[20] ,
                                        'Revenue Growth': value_list[21] ,
                                        'Total Cash': value_list[22] ,
                                        'Total Cash Per Share': value_list[23] ,
                                        'Total Debt': value_list[24] ,
                                        'Current Ratio': value_list[25] ,
                                        'Book Value Per Share': value_list[26] ,
                                        'Cash Flow': value_list[27] ,
                                        'Beta': value_list[28] ,
                                        'Held by Insiders': value_list[29] ,
                                        'Held by Institutions': value_list[30] ,
                                        'Shares Short (as of': value_list[31] ,
                                        'Short Ratio': value_list[32] ,
                                        'Short % of Float': value_list[33] ,
                                        'Shares Short (prior ': value_list[34] ,
                                        'Status': status} ,
                                       ignore_index=True)
                except Exception as e:
                    pass

                # get the totle deb of each company for each file
                print(ticker + ":", value)

    # for each_ticker in tiker_list:
    #     try:
    #         plot_df = df[(df['Ticker'] == each_ticker)]
    #         plot_df = plot_df.set_index(['Date'])
    #
    #         if plot_df['Status'][-1] == "underperform":
    #             color = 'r'
    #         else:
    #             color = 'g'
    #
    #         plot_df['Difference'].plot(label=each_ticker, color=color)
    #
    #         plt.legend()
    #     except:
    #         pass
    # plt.show()

    # save = gather.replace(' ', '').replace(')', '').replace('(', '').replace('/', '') + str('.csv')
    # print(save)
    df.to_csv("key_stats.csv")
Key_Stats()
