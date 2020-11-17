from fbprophet import Prophet #Predict adj_cases
import pandas as pd #Dataframes

adj_df = pd.read_csv("../data/processed/adjacency_list.csv")
df = pd.read_csv('../data/raw/covid-19-data/us-counties.csv')
df = df[df['fips'] < 60000]
df = df.drop(['county','state','deaths'],1)
df['date'] = pd.to_datetime(df['date'])

ret_df = pd.DataFrame(columns={'fips','date','adj_cases'})

for fips in df.fips.unique():
    try:
        #Generates adjacency sums and appends to a new sub dataframe with cases and normalized flu data
        adjacent = adj_df.loc[adj_df.county == fips, ].values.flatten().tolist()
        adjacent = [x for x in adjacent if str(x) != 'nan']
        sub_df = df[df.fips.isin(adjacent)]
        sub_df = sub_df.groupby('date')['cases'].sum().to_frame()
        sub_df.reset_index(inplace=True)
        sub_df = sub_df.rename(columns = {'cases':'y','date':'ds'})
        sub_df = sub_df.dropna()

        print(sub_df)

        #Modeling
        model_p = Prophet(yearly_seasonality=True)
        model_p.fit(sub_df)
        future = model_p.make_future_dataframe(periods=115)
        forecast = model_p.predict(future)
        test = forecast[['ds','yhat']]
        test.insert(0,'fips',fips)
        test = test.rename(columns = {'ds':'date','yhat':'adj_cases'})
        test['adj_cases'] = test['adj_cases'].astype(int)
        test.loc[test['adj_cases'] < 0,'adj_cases'] = 0
        ret_df = ret_df.append(test)
    except:
        print(str(fips) + ": Failed")

ret_df.to_csv('../data/processed/adj_sum.csv',index=False)