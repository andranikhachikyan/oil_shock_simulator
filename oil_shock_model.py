import pandas as pd
import statsmodels.api as sm

# load data
monthly = pd.read_csv("processed_data/master_monthly.csv")
quarterly = pd.read_csv("processed_data/master_quarterly.csv")

monthly = monthly.dropna()
quarterly = quarterly.dropna()

def run_regression(df, y_col, x_cols): # all models ran by this func
    X = sm.add_constant(df[x_cols])
    y = df[y_col] 
    return sm.OLS(y, X).fit()

model_gas = run_regression(monthly, "Gas_pct", ["Brent_pct"])
model_energy = run_regression(monthly, "Energy_inf", ["Gas_pct", "Brent_pct"])
model_cpi = run_regression(monthly, "CPI_inf", ["Gas_pct", "Energy_inf"])
model_gdp = run_regression(quarterly, "GDP_growth", ["CPI_inf", "Energy_inf"])

def simulate_shock(shock):            # Shock sim function 

    brent = monthly['Brent_pct'].iloc[-1] + shock

    gas = model_gas.predict([1, brent])[0]

    energy = model_energy.predict([1, gas, brent])[0]

    cpi = model_cpi.predict([1, gas, energy])[0]

    gdp = model_gdp.predict([1, cpi, energy])[0]

    return {
        "Gas": gas,
        "Energy": energy,
        "CPI": cpi,
        "GDP": gdp
    }