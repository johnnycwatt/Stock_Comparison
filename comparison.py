
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf


def get_history(stock, period,interval):
    info = yf.download(tickers=stock, period=period, interval= interval, group_by="ticker")

    price = info.iloc[:, info.columns.get_level_values(1) == "Close"]
    price = round(price, 2)
    price.columns = price.columns.droplevel(1)

    percentage = round(price[stock].pct_change()*100,2)
    percentage["MONTH"] = pd.to_datetime(percentage.index).strftime("%Y-%m")
    percentage["YEAR"] = pd.to_datetime(percentage.index).strftime("%Y")

    price["MONTH"] = pd.to_datetime(price.index).strftime("%Y-%m")
    price["YEAR"] = pd.to_datetime(price.index).strftime("%Y")

    return price, percentage



def make_graph(price, perc, months, x):

    fig, (ax1, ax2) = plt.subplots(nrows=2, ncols=1, figsize=(10,10))

    ax1.plot(price[x], price[stock1])
    ax1.plot(price[x], price[stock2])

    ax2.plot(perc[x], perc[stock1])
    ax2.plot(perc[x], perc[stock2])

    ax1.set_title(f"{stock1} vs {stock2}  ({months} {x}S)")
    ax2.set_title(f"{stock1} vs {stock2} ({months} {x}S)")

    ax1.legend([stock1, stock2], loc=2)
    ax2.legend([stock1, stock2], loc=2)

    ax1.set_ylabel("STOCK PRICE")
    ax2.set_ylabel(f"{x}LY CHANGES %")

    #ax1.tick_params(labelrotation=90) #May be necessary if having two columns instead of two rows.
    #ax2.tick_params(labelrotation=90)

    plt.tight_layout
    return plt

def generate_table(perc, x):

    df = pd.DataFrame()
    df[x] = perc[x].sort_values().unique()
    df[stock1] = perc[stock1].groupby(perc[x]).sum().values
    df[stock2] = perc[stock2].groupby(perc[x]).sum().values
    df[stock1] = round(df[stock1],2)
    df[stock2] = round(df[stock2],2)
    df = df.tail(months)
    df.loc["TOTAL"] = round(df.sum(numeric_only=True, axis=0),2)
    df.loc["TOTAL", x] = ""
    df["HIGHEST"] = df[stock].idxmax(axis=1)
    df["MAX"] = round(df[stock].max(axis=1),2)


    return df

def comparison(period,interval,months, x):

    history = get_history(stock, period, interval)

    prices = history[0]
    percentages = history[1]

    graph = make_graph(prices,percentages, months, x)
    overview = get_info()

    comparison = generate_table(percentages, x)
    comparison.to_csv(f"{stock1} and {stock2} {months} {x} comparison.csv")
    overview.to_csv(f"{stock1} and {stock2} {months} {x} comparison.csv", mode='a', header="Hello")

    graph.savefig(f"{stock1} and {stock2} {months} {x} comparison")


def get_info():#Collects An Overview Of Each Stocks Informations
    rows = ["shortName", "sector", "industry",
            "marketCap", "trailingPE",
            "fiftyTwoWeekLow", "fiftyTwoWeekHigh",
            "dividendRate", "52WeekChange", "phone"]

    df = pd.DataFrame(index = rows, columns=stock)

    for x in stock:
        info = []
        y = yf.Ticker(x)
        for row in rows:
            if "date" in row.lower():
                date = pd.to_datetime(y.info[row])
                if date != None:
                    info.append(date.strftime("%Y-%m-%d"))
            else:
                try:
                    info.append(y.info[row])
                except:
                    info.append("")
        df[x] = info

    return df

stock1 = "GOOG"
stock2 = "AMZN"

stock = [stock1, stock2]
period = "5y"
interval = "1mo"
months = 12
years = 5

comparison(period,interval,years,"YEAR") #5 Year Comparison
comparison("1y", interval, months, "MONTH")#1 Year Comparison


