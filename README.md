# Coin_market_cap
Here you can find a simple way to get crypto coins historical data and basic statistics out of ‘coinmarketcap.com’.

# Usage
## Coins_history.py 
### Main method to run: get_crypto_coins_history 
  
  #### Parameters
  
  | Parameter |	Description	| Default Value
  | --- | --- | --- |
  | i_rank_start |	Pull data from current rank [includes] |	1
  | i_rank_end |	Pull data to current rank [includes]	| 10
  | i_coin_file_path |	Csv file name	| crypto_coins
  | i_from_date |	Pull data from this date [YYYY-MM-DD] | 30 days ago
  | i_to_date	|Pull data till this date [YYYY-MM-DD]	| Yesterday
  | i_min_volume | Pull data when 24 Hrs. volume bigger than this |100,000 [usd]
  | i_coin_markets | pull data when coins traded on those markets, if empty ignore | empty list

  #### Output
  CSV file contains the following columns: Coin, Cur. rank, Close, Date, High, Low, Market cap, Open, Volume

### Method: get_specific_coin_historical_data
  
  #### Parameters:
 
  | Parameter |	Description	| Format
  | --- | --- | --- |
  | i_coin | Coin name | string
  | i_from_date | Pull data from this date | string 'YYYYmmdd'
  | i_to_date | Pull data till this date | string 'YYYYmmdd'
  
  #### Output
  Dataframe contains the following columns: Close, Date, High, Low, Market cap, Open, Volume
    
## Coins_statistics.py
### Main method to run: save_coins_statistics 
 
  #### Parameters:
  
  Parameter |	Description	| Default Value
  | --- | --- | --- |
  | i_rank_start |	Pull data from current rank [includes] |	1
  | i_rank_end |	Pull data to current rank [includes]	| 10
  | i_coin_file_path |	Csv file name	| crypto_coins
 
#### Output
CSV file contains the following columns:

| Column | Calculation description
| --- | --- |
| Change [Close] | ([Close] – [Yesterday Close])/ [Yesterday Close]
| Change [High] | ([High] – [Yesterday High])/ [Yesterday High]
| Change [Market Cap] | ([Market Cap] – [Market Cap High])/ [Market Cap High]
| Change [Volume] | ([Volume] – [Volume High])/ [Volume High]
| Daily rank market cap | Rank of each coin market cap per each date
| Daily rank volume | Rank of each coin volume per each date
| Day Change [Open to high] | ([High] – [Open]) / [Open]
| Day change [Open to close] | ([Close] – [Open]) / [Open]
| High average	| High average of all dates appear in file
| Market cap average | Market cap average of all dates appear in file


# Acknowledgements

Data is scrapped from [coinmarketcap](https://coinmarketcap.com/)


