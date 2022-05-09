import os
import originpro as op
import pandas as pd

file = "D:\\Researcher\\JYCheon\\DATA\\Electrochemistry\\2022\\Raw\\0317 PANI CNT film with press\\Tot\\output\\GCD_tot.xlsx"

df = pd.read_excel(file)


wks = op.find_sheet()
wks.from_df(df)

graph = op.new_graph(template = 'GCD ref2')

#plot = graph[0].add_plot(wks, colx = 0, coly = 1)
#plot2 = graph[0].add_plot(wks, colx = 2, coly = 3)


n = df.shape[1]

print(n)
for i in range(0, n, 2):
    graph[0].add_plot(wks, colx = i, coly = i+1)