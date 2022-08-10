import requests
import numpy_financial as npf
import pandas as pd
company = 'NVDA'
demo = 'demo_api_key'
wacc_company = 0.073
LTGrowth = 0.02

IS = requests.get(f'https://financialmodelingprep.com/api/v3/income-statement/{company}?apikey={demo}').json()
count = 0
#get revenue growth to estimate future sales
print ("start revenue growth")
revenue_g = []
for item in IS:
  if count < 4:
    print(item)
    revenue_g.append(item['revenue'])
    count = count + 1
revenue_g = (revenue_g[0] - revenue_g[1]) /revenue_g[0]
print(revenue_g)
# revenue_g = 0.10

#ouctome
# 0.15469210475913925
print ("end revenue growth")
#Get net income
net_income = IS[0]['netIncome']
BS = requests.get(f'https://financialmodelingprep.com/api/v3/balance-sheet-statement/{company}?apikey={demo}').json()
#get income statement as % of revenue for future predictions and forecast 5 next IS years
income_statement = pd.DataFrame.from_dict(IS[0],orient='index')
#The [5:26] below get rids of not needed items coming from the API

print ("start income statement")

income_statement = income_statement[8:36]
income_statement.columns = ['current_year']
income_statement['as_%_of_revenue'] = income_statement / income_statement.iloc[0]
#forecasting 5 next years income statement
income_statement['next_year'] =  (income_statement['current_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue']
income_statement['next_2_year'] =  (income_statement['next_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue']
income_statement['next_3_year'] =  (income_statement['next_2_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue']
income_statement['next_4_year'] =  (income_statement['next_3_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue']
income_statement['next_5_year'] =  (income_statement['next_4_year']['revenue'] * (1+revenue_g)) * income_statement['as_%_of_revenue']
#Get Balance sheet as a percentage of revenue
print ("end income statement")

print ("start balance sheet")
balance_sheet = pd.DataFrame.from_dict(BS[0],orient='index')
balance_sheet = balance_sheet[8:-2]
balance_sheet.columns = ['current_year']
balance_sheet['as_%_of_revenue'] = balance_sheet / income_statement['current_year'].iloc[0]
#forecasting the next 5 years Balance Sheet.
balance_sheet['next_year'] =  (income_statement['next_year'] ['revenue']) * (balance_sheet['as_%_of_revenue'])
balance_sheet['next_2_year'] =  (income_statement['next_2_year'] ['revenue']) * (balance_sheet['as_%_of_revenue'])
balance_sheet['next_3_year'] =  (income_statement['next_3_year']['revenue']) * (balance_sheet['as_%_of_revenue'])
balance_sheet['next_4_year'] =  (income_statement['next_4_year']['revenue']) * (balance_sheet['as_%_of_revenue'])
balance_sheet['next_5_year'] =  (income_statement['next_5_year']['revenue']) * (balance_sheet['as_%_of_revenue'])
print ("end balance sheet")

print ("start cash flow forecast")

CF_forecast = {}
CF_forecast['next_year'] = {}
CF_forecast['next_year']['netIncome'] = income_statement['next_year']['netIncome']
CF_forecast['next_year']['inc_depreciation'] = income_statement['next_year']['depreciationAndAmortization'] - income_statement['current_year']['depreciationAndAmortization']
CF_forecast['next_year']['inc_receivables'] = balance_sheet['next_year']['netReceivables'] - balance_sheet['current_year']['netReceivables']
CF_forecast['next_year']['inc_inventory'] = balance_sheet['next_year']['inventory'] - balance_sheet['current_year']['inventory']
CF_forecast['next_year']['inc_payables'] = balance_sheet['next_year']['accountPayables'] - balance_sheet['current_year']['accountPayables']
CF_forecast['next_year']['CF_operations'] = CF_forecast['next_year']['netIncome'] + CF_forecast['next_year']['inc_depreciation'] + (CF_forecast['next_year']['inc_receivables'] * -1) + (CF_forecast['next_year']['inc_inventory'] *-1) + CF_forecast['next_year']['inc_payables']
CF_forecast['next_year']['CAPEX'] = balance_sheet['next_year']['propertyPlantEquipmentNet'] - balance_sheet['current_year']['propertyPlantEquipmentNet'] + income_statement['next_year']['depreciationAndAmortization']
CF_forecast['next_year']['FCF'] = CF_forecast['next_year']['CAPEX'] + CF_forecast['next_year']['CF_operations']
CF_forecast['next_2_year'] = {}
CF_forecast['next_2_year']['netIncome'] = income_statement['next_2_year']['netIncome']
CF_forecast['next_2_year']['inc_depreciation'] = income_statement['next_2_year']['depreciationAndAmortization'] - income_statement['next_year']['depreciationAndAmortization']
CF_forecast['next_2_year']['inc_receivables'] = balance_sheet['next_2_year']['netReceivables'] - balance_sheet['next_year']['netReceivables']
CF_forecast['next_2_year']['inc_inventory'] = balance_sheet['next_2_year']['inventory'] - balance_sheet['next_year']['inventory']
CF_forecast['next_2_year']['inc_payables'] = balance_sheet['next_2_year']['accountPayables'] - balance_sheet['next_year']['accountPayables']
CF_forecast['next_2_year']['CF_operations'] = CF_forecast['next_2_year']['netIncome'] + CF_forecast['next_2_year']['inc_depreciation'] + (CF_forecast['next_2_year']['inc_receivables'] * -1) + (CF_forecast['next_2_year']['inc_inventory'] *-1) + CF_forecast['next_2_year']['inc_payables']
CF_forecast['next_2_year']['CAPEX'] = balance_sheet['next_2_year']['propertyPlantEquipmentNet'] - balance_sheet['next_year']['propertyPlantEquipmentNet'] + income_statement['next_2_year']['depreciationAndAmortization']
CF_forecast['next_2_year']['FCF'] = CF_forecast['next_2_year']['CAPEX'] + CF_forecast['next_2_year']['CF_operations']
CF_forecast['next_3_year'] = {}
CF_forecast['next_3_year']['netIncome'] = income_statement['next_3_year']['netIncome']
CF_forecast['next_3_year']['inc_depreciation'] = income_statement['next_3_year']['depreciationAndAmortization'] - income_statement['next_2_year']['depreciationAndAmortization']
CF_forecast['next_3_year']['inc_receivables'] = balance_sheet['next_3_year']['netReceivables'] - balance_sheet['next_2_year']['netReceivables']
CF_forecast['next_3_year']['inc_inventory'] = balance_sheet['next_3_year']['inventory'] - balance_sheet['next_2_year']['inventory']
CF_forecast['next_3_year']['inc_payables'] = balance_sheet['next_3_year']['accountPayables'] - balance_sheet['next_2_year']['accountPayables']
CF_forecast['next_3_year']['CF_operations'] = CF_forecast['next_3_year']['netIncome'] + CF_forecast['next_3_year']['inc_depreciation'] + (CF_forecast['next_3_year']['inc_receivables'] * -1) + (CF_forecast['next_3_year']['inc_inventory'] *-1) + CF_forecast['next_3_year']['inc_payables']
CF_forecast['next_3_year']['CAPEX'] = balance_sheet['next_3_year']['propertyPlantEquipmentNet'] - balance_sheet['next_2_year']['propertyPlantEquipmentNet'] + income_statement['next_3_year']['depreciationAndAmortization']
CF_forecast['next_3_year']['FCF'] = CF_forecast['next_3_year']['CAPEX'] + CF_forecast['next_3_year']['CF_operations']
CF_forecast['next_4_year'] = {}
CF_forecast['next_4_year']['netIncome'] = income_statement['next_4_year']['netIncome']
CF_forecast['next_4_year']['inc_depreciation'] = income_statement['next_4_year']['depreciationAndAmortization'] - income_statement['next_3_year']['depreciationAndAmortization']
CF_forecast['next_4_year']['inc_receivables'] = balance_sheet['next_4_year']['netReceivables'] - balance_sheet['next_3_year']['netReceivables']
CF_forecast['next_4_year']['inc_inventory'] = balance_sheet['next_4_year']['inventory'] - balance_sheet['next_3_year']['inventory']
CF_forecast['next_4_year']['inc_payables'] = balance_sheet['next_4_year']['accountPayables'] - balance_sheet['next_3_year']['accountPayables']
CF_forecast['next_4_year']['CF_operations'] = CF_forecast['next_4_year']['netIncome'] + CF_forecast['next_4_year']['inc_depreciation'] + (CF_forecast['next_4_year']['inc_receivables'] * -1) + (CF_forecast['next_4_year']['inc_inventory'] *-1) + CF_forecast['next_4_year']['inc_payables']
CF_forecast['next_4_year']['CAPEX'] = balance_sheet['next_4_year']['propertyPlantEquipmentNet'] - balance_sheet['next_3_year']['propertyPlantEquipmentNet'] + income_statement['next_4_year']['depreciationAndAmortization']
CF_forecast['next_4_year']['FCF'] = CF_forecast['next_4_year']['CAPEX'] + CF_forecast['next_4_year']['CF_operations']
CF_forecast['next_5_year'] = {}
CF_forecast['next_5_year']['netIncome'] = income_statement['next_5_year']['netIncome']
CF_forecast['next_5_year']['inc_depreciation'] = income_statement['next_5_year']['depreciationAndAmortization'] - income_statement['next_4_year']['depreciationAndAmortization']
CF_forecast['next_5_year']['inc_receivables'] = balance_sheet['next_5_year']['netReceivables'] - balance_sheet['next_4_year']['netReceivables']
CF_forecast['next_5_year']['inc_inventory'] = balance_sheet['next_5_year']['inventory'] - balance_sheet['next_4_year']['inventory']
CF_forecast['next_5_year']['inc_payables'] = balance_sheet['next_5_year']['accountPayables'] - balance_sheet['next_4_year']['accountPayables']
CF_forecast['next_5_year']['CF_operations'] = CF_forecast['next_5_year']['netIncome'] + CF_forecast['next_5_year']['inc_depreciation'] + (CF_forecast['next_5_year']['inc_receivables'] * -1) + (CF_forecast['next_5_year']['inc_inventory'] *-1) + CF_forecast['next_5_year']['inc_payables']
CF_forecast['next_5_year']['CAPEX'] = balance_sheet['next_5_year']['propertyPlantEquipmentNet'] - balance_sheet['next_4_year']['propertyPlantEquipmentNet'] + income_statement['next_5_year']['depreciationAndAmortization']
CF_forecast['next_5_year']['FCF'] = CF_forecast['next_5_year']['CAPEX'] + CF_forecast['next_5_year']['CF_operations']


#add the forecasted cash flows into a Pandas
CF_forec = pd.DataFrame.from_dict(CF_forecast,orient='columns')
#add below option to format the dataframe with thousand separators
pd.options.display.float_format = '{:,.0f}'.format
print(CF_forec)

print ("end cash flow forecast")

print ("start wacc")
# need to add logic to derive WACC
print (wacc_company)
print ("end wacc")

print ("start net present value")

#FCF List of CFs for each year
FCF_List = CF_forec.iloc[-1].values.tolist()
npv = npf.npv(wacc_company,FCF_List)
print (npv)
print ("end net present value")

print ("start terminal value discounted")

#Terminal value
Terminal_value = (CF_forecast['next_5_year']['FCF'] * (1+ LTGrowth)) /(wacc_company  - LTGrowth)
Terminal_value_Discounted = Terminal_value/(1+wacc_company)**4
print (Terminal_value_Discounted)

print ("end terminal value discounted")

print ("start target price per share")

target_equity_value = Terminal_value_Discounted + npv
debt = balance_sheet['current_year']['totalDebt']
target_value = target_equity_value - debt
numbre_of_shares = requests.get(f'https://financialmodelingprep.com/api/v3/enterprise-values/{company}?apikey={demo}').json()
numbre_of_shares = numbre_of_shares[0]['numberOfShares']
target_price_per_share = target_value/numbre_of_shares
print (target_price_per_share)

print ("end target price per share")

print(company + ' forecasted price per stock is ' + str(target_price_per_share) )
print('the forecast is based on the following assumptions: '+ 'revenue growth: ' + str(revenue_g) + ' Cost of Capital: ' + str(wacc_company) )
print('perpetuity growth: ' + str(LTGrowth))
#outcome
# GOOG forecasted price per stock is 4828.474984873333
# the forecast is based on the following assumptions: revenue growth: 0.15469210475913925 Cost of Capital: 0.07348998226517206
# perpetuity growth: 0.02



