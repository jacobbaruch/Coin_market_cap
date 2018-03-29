import pandas as pd
import sys


def save_coins_statistics(i_coins_file='crypto_coins', i_out_file='crypto_coins_stats'
                          , i_precision = 3):
 '''
 :param str i_coins_file: crypto coins history file name
 :param str i_out_file: output csv file name
 :param int i_precision: precision point to the statistics fields
 writes to a csv file - adding coins basic statistics to the history file
 '''

 pd.options.mode.use_inf_as_na = True
 coins_file = i_coins_file + '.csv'
 coins_stats_file = i_out_file + '.csv'
 pd.set_option('precision', i_precision)

 df = read_coins_csv(coins_file)
 df = extend_daily_data(df)
 df_extended = attach_yesterday_data(df)
 df_extended = calc_yesterday_statistics(df_extended)
 write_extended_df_to_csv(df_extended, coins_stats_file)


def extend_daily_data(i_df):
 """
 :param dataframe i_df: Coins historic data
 :return dataframe: adds daily changes, average and rank
 """

 # Daily changes
 i_df['Day Change [open to high]'] = (i_df['High'] - i_df['Open']) / i_df['Open']
 i_df['Day Change [open to close]'] = (i_df['Close'] - i_df['Open']) / i_df['Open']
 i_df['Date'] = pd.to_datetime(i_df['Date'])
 i_df['Market Cap'] = i_df['Market Cap'].str.replace('-','')
 i_df['Market Cap'] = pd.to_numeric(i_df['Market Cap'].str.replace(',', ''))
 i_df['Volume'] = pd.to_numeric(i_df['Volume'].str.replace(',', ''))

 i_df = pd.merge(i_df, get_mean(i_df), how='left', on=['Coin'])
 i_df = get_ranks_per_date(i_df)

 return i_df


def get_mean(i_df):
 """
 :param dataframe i_df: contains coins data
 :return dataframe: contains Volume / High Averages
 """

 df_group_by_coin = (i_df.groupby(['Coin'], as_index=False)
  .agg({'High': 'mean', 'Volume': 'mean'})
  .rename(columns={'High': 'High Avg', 'Volume': 'Volume Avg.'}))
 return df_group_by_coin


def get_ranks_per_date(i_df):
 """
 :param dataframe i_df: contains coins data
 :return dataframe: contains daily ranking of volume and market cap for each coin
 """

 i_df['Daily rank Market Cap'] = i_df.groupby('Date')['Market Cap'].rank(method='dense',ascending=False)
 i_df['Daily rank Volume'] = i_df.groupby('Date')['Volume'].rank(method='dense',ascending=False)

 return i_df


def attach_yesterday_data(i_df):
 """
 :param dataframe i_df: contains coins data
 :return dataframe: attach data of yesterday date for each date
 """

 # prepare yesterday date key
 i_df['Yesterday'] = i_df['Date'].apply(pd.DateOffset(days=-1))

 # assign data frame that will merge into 'i_df'
 df_yesterday = i_df[['Coin', 'Date', 'High', 'Market Cap', 'Volume','Close']]
 df_yesterday = df_yesterday.rename(index=str, columns={'Date': 'Yesterday',
                                                        'High': 'High Yesterday',
                                                        'Close': 'Close Yesterday',
                                                        'Market Cap': 'Market Cap yesterday',
                                                        'Volume': 'Volume yesterday'})
 # merging the data frames based on Coin + Yesterday Date
 df_extended = pd.merge(i_df, df_yesterday, how='left', on=['Coin', 'Yesterday'])
 df_extended.drop(['Yesterday'], axis=1, inplace=True)
 df_extended.fillna(0, inplace=True)

 return df_extended


def calc_yesterday_statistics(i_df):
 """
 :param dataframe i_df: contains extended data
 :return dataframe: for each date we calc the changes in:
  Close, High, Market Cap, Volume, correlation between changes
 """
 i_df['Change [Close]'] = (i_df['Close'] - i_df['Close Yesterday']) /  i_df['Close Yesterday']
 i_df['Change [High]'] = (i_df['High'] - i_df['High Yesterday']) / i_df['High Yesterday']
 i_df['Change [Market Cap]'] = (i_df['Market Cap'] - i_df['Market Cap yesterday']) / i_df['Market Cap yesterday']
 i_df['Change [Volume]'] = (i_df['Volume'] - i_df['Volume yesterday']) / i_df['Volume yesterday']

 i_df.drop(['Close Yesterday'], axis=1, inplace=True)
 i_df.drop(['High Yesterday'], axis=1, inplace=True)
 i_df.drop(['Market Cap yesterday'], axis=1, inplace=True)
 i_df.drop(['Volume yesterday'], axis=1, inplace=True)

 return i_df


def read_coins_csv(i_file):
 try:
  df = pd.read_csv(i_file, index_col=0)
 except IOError as e:
  print(e)
  sys.exit(13)

 return df


def write_extended_df_to_csv(i_df, i_file):
 try:
  i_df.to_csv(i_file, float_format='%.3f')
 except IOError as e:
  print(e)
  sys.exit(13)