import pandas as pd
from fuzzywuzzy import process

file_path1 = '########'
file_path2 = '########'

df1 = pd.read_excel(file_path1)
df2 = pd.read_excel(file_path2)

print("Columns in Dataframe 1 (Backmarket):", df1.columns)
print("Columns in Dataframe 2 (Modified Final):", df2.columns)

df2.rename(columns={'name': 'model'}, inplace=True)

df1['model'] = df1['model'].str.strip().str.lower()
df2['model'] = df2['model'].str.strip().str.lower()

print("Standardized 'model' column in Dataframe 1:")
print(df1[['model']].head())

print("Standardized 'model' column in Dataframe 2:")
print(df2[['model']].head())

df1_filtered = df1[['brand', 'model', 'capacity', 'color', 'state', 'price']]
df2_filtered = df2[['Marque', 'model', 'additional_text', 'price_new', 'price_old', 'image_url', 'category']]

print("Samsung models in Backmarket dataframe:")
samsung_df1 = df1_filtered[df1_filtered['brand'].str.lower() == 'samsung']
print(samsung_df1['model'].unique())

print("Samsung models in Modified Final dataframe:")
samsung_df2 = df2_filtered[df2_filtered['Marque'].str.lower() == 'samsung']
print(samsung_df2['model'].unique())

model_mapping = {}
for model in samsung_df1['model'].unique():
    closest_match, score = process.extractOne(model, samsung_df2['model'].unique())
    if score > 80:  
        model_mapping[model] = closest_match

print("Model mappings:", model_mapping)

df1_filtered['model_mapped'] = df1_filtered['model'].apply(lambda x: model_mapping.get(x, x))

df_combined = pd.merge(df1_filtered, df2_filtered, left_on='model_mapped', right_on='model', how='left')

print("Merged dataframe (Samsung models):")
print(df_combined[df_combined['brand'].str.lower() == 'samsung'])

df_combined.drop(columns=['model_mapped'], inplace=True)

df_combined.sort_values(by='brand', inplace=True)

output_combined_path = '#######'
df_combined.to_excel(output_combined_path, index=False)

print("Combined file created successfully")