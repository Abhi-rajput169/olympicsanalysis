import pandas as pd



def preprocess(df,region_df):
   
   #merge with region_df
   df=df.merge(region_df,on='NOC',how='left')
   #one hot encoding medals
   df=pd.concat([df,pd.get_dummies(df['Medal'])],axis=1)
   return df

 