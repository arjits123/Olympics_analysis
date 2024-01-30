import pandas as pd 

def preprocess(df, region_df):
    
    # need only summer data 
    df = df[df['Season'] == 'Summer']

    #Merging with the NOC data
    df = df.merge(region_df, on = 'NOC', how = 'left')

    #dropping the duplicates
    df.drop_duplicates(inplace=True)

    # Since we have no missing values in NOC , so we will group by NOC for the medals
    # we check the gold silver and bronze
    df = pd.concat([df,pd.get_dummies(df['Medal'])],axis =1) # it will create dummy variables/ one hot encoding

    return df