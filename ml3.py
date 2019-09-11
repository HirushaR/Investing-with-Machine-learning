import pandas as pd
import os
import quandl
import time

auth_tok = open("auth.txt", "r").read()

data = quandl.get("WIKI/KO", trim_strat="2000-12-12",trim_end="2014-12-13", authtoken=auth_tok)

print(data["Adj. Close"])
