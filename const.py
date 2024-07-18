import os
import csv
import datetime
import traceback
import openai

dirs = [] 

ROOT_DIR = 'C:\VS_Code/MY_discord_bot' 
dirs.append(ROOT_DIR)

LICHESS_JSON_FILEPATH = ROOT_DIR + '/lichess_accounts.json'
dirs.append(LICHESS_JSON_FILEPATH)

MONEY_JSON_FILEPATH = ROOT_DIR + '/money.json'
dirs.append(MONEY_JSON_FILEPATH)

TIMEOUT_COUNT_DIR = ROOT_DIR + '/timeout_counts.csv'
dirs.append(TIMEOUT_COUNT_DIR)

EXCEPTION_FILE = ROOT_DIR + '/exception.csv'
dirs.append(EXCEPTION_FILE)



CACHE_DIR = ROOT_DIR + '/cache_dir'
dirs.append(CACHE_DIR)

STOCK_LOGO_DIR = CACHE_DIR + '/logos'
dirs.append(STOCK_LOGO_DIR)

CACHE_DIR_PFP = CACHE_DIR + '/pfps'
dirs.append(CACHE_DIR_PFP)



PNGS_DIR = ROOT_DIR + '/pngs'
dirs.append(PNGS_DIR)

DEFUALT_PROFILE_PIC = PNGS_DIR + '/defualt.png'
dirs.append(DEFUALT_PROFILE_PIC)

LEADERBOARD_PIC = PNGS_DIR + '/leaderboard.png'
dirs.append(LEADERBOARD_PIC)

STOCK_GRAPH_PIC = PNGS_DIR + '/stock_graph.png'
dirs.append(STOCK_GRAPH_PIC)



STOCKS_DIR = ROOT_DIR + '/stocks'
dirs.append(STOCKS_DIR)

USER_STOCKS = STOCKS_DIR + '/stocks.json'
dirs.append(USER_STOCKS)

STOCK_HISTORY_FILE = STOCKS_DIR + '/stock_history.json'
dirs.append(STOCK_HISTORY_FILE)



EXCEPTION_MESSAGE = 'Something went wrong, please take a screen shot of the messages regarding the error, and use the `$bug` command to report it. Any addetional information would be helpful.'

UNSPLASH_ACCESS_KEY = 'Hml8JmR7UZk1bxjqVnac99UdBRGId69CUbtdHmC2aW0'
DEV_BOT_TOKEN = "MTIzMDk2MjI2OTc0ODQ2NTY2Ng.G99PQ1.04Ch0VvwZbQqS0ZnbPKMjjAra8t2dHv38M9BQ0"
PROD_BOT_TOKEN = 'MTE3NTg5MDY0NDE5MTk1NzAxMw.GZtdjv.4039BrLsym-_rBJd1OV8W7GdSVysVomGA9xHC4'

def write_exception(traceback):
    current_time = datetime.datetime.now()
    formatted_time = current_time.strftime("%H:%M:%S")
    current_date = datetime.date.today()

    file_exists = os.path.exists(EXCEPTION_FILE)
    with open(EXCEPTION_FILE, 'a', newline='') as file:
        writer = csv.writer(file)
        if not file_exists:
            writer.writerow(['time', 'date', 'file', 'line', 'exception'])  # Write header only if the file is newly created

        writer.writerow([traceback])

#use os to check if ROOT dir is vaild
for i in range(len(dirs)):
    if not os.path.isdir(dirs[i]):
        if not os.path.isfile(dirs[i]):
            write_exception(traceback.format_exc())