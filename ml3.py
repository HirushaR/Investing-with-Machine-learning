import pandas as pd
import os
import quandl
import time

auth_tok = open("auth.txt", "r").read()

# data = quandl.get("WIKI/KO", trim_strat="2000-12-12",trim_end="2014-12-13", authtoken=auth_tok)
#
# print(data["Adj. Close"])

path = "E:/hiru/works/ml/project1/intraQuarter"

def Stock_Prices():
    df = pd.DataFrame()
    statspath = path + "/_KeyStats"
    stock_list = [x[0] for x in os.walk(statspath)]

    for each_dir in stock_list[1:]:
        try:
            tiker = each_dir.split("\\")[1]
            print(tiker)
            name = "WIKI/"+tiker.upper()
            data = quandl.get(name,
                              trim_strat="2000-12-12",
                               trim_end="2014-12-13",
                               authtoken=auth_tok)

            data[tiker.upper()] = data["Adj. Close"]
            df=pd.concat([df, data[tiker.upper()]], axis=1)
        except Exception as e:
            print(str(e))
            time.sleep(5)
            try:
                tiker = each_dir.split("\\")[1]
                print(tiker)
                name = "WIKI/" + tiker.upper()
                data = quandl.get(name ,
                                  trim_strat="2000-12-12" ,
                                  trim_end="2014-12-13" ,
                                  authtoken=auth_tok)

                data[tiker.upper()] = data["Adj. Close"]
                df = pd.concat([df, data[tiker.upper()]] , axis=1)
            except Exception as e:
                print(str(e))
    df.to_csv("stock_prices.csv")

Stock_Prices()
