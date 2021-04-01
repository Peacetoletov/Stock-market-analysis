# napřed musím pullnout z yahoo finance 2 čísla: average a current
# (analyst price targets)

import requests
from bs4 import BeautifulSoup
from datetime import date


def get_tickers(file_name="vbr.txt"):
    tickers_file = open(file_name, "r")
    lines = tickers_file.readlines()
    tickers_file.close()

    tickers = []
    for line in lines:
        no_newline = line.rstrip('\n')
        tickers.append(no_newline)

    return tickers


def get_current_and_target_price(ticker: str):
    # returns the ratio of estimated price and current price
    url = "https://finance.yahoo.com/quote/" + ticker
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    spans = soup.find_all("span")

    current = None
    target = None
    next_important = False
    """
    for span in spans:
        as_string = str(span.text)
        print(as_string)
        
        if next_important:
            if ask is None:
                ask = as_string.split()[0]
            else:
                target = as_string

        next_important = as_string == "Ask" or as_string == "1y Target Est"
        """
    i = 0
    while i < len(spans):
        as_string = str(spans[i].text)
        # print(as_string)

        if next_important:
            if current is None:
                current = as_string
            else:
                target = as_string

        if as_string == "Add to watchlist":
            next_important = True
            i += 1
        else:
            next_important = as_string == "1y Target Est"

        i += 1


    # print("Ask =", ask)
    # print("Target =", target)

    return float(current), float(target)


def get_sample_size(ticker: str):
    # returns the number of analysts for "Next Qtr."
    url = "https://finance.yahoo.com/quote/" + ticker + "/analysis"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    spans = soup.find_all("span")

    sample_size = None
    counter = None
    for span in spans:
        #print(span.text)
        if str(span.text) == "No. of Analysts":
            counter = 0

        if counter is not None:
            if counter == 2:
                sample_size = str(span.text)
                break
            counter += 1

    return int(sample_size)


def create_file_with_prices():
    tickers = get_tickers()
    companies_by_value = []
    for i in range(0, len(tickers)):  # for i in range(0, len(tickers)):
        ticker = tickers[i]
        print("current ticker =", ticker)
        try:
            current, target = get_current_and_target_price(ticker)
            sample_size = get_sample_size(ticker)

            if current < 1:
                # skip penny stocks
                continue

            if sample_size < 3:
                # skip companies with irrelevant sample size
                continue
            elif sample_size == 3:
                # arbitrarily adjusting for low sample size
                target *= 0.85

            # print(ticker + ":", sample_size, target)
            companies_by_value.append((ticker, current, target / current))

        except ValueError:
            # print("FAIL:", ticker)
            pass
        except TypeError:
            pass
        except ZeroDivisionError:
            pass

    companies_by_value.sort(key=lambda x: x[2], reverse=True)
    for ticker, current, value in companies_by_value:
        print(ticker, value)

        today = date.today()
        f = open("phantom_portfolio/" + str(today), "a")
        f.write(ticker + " " + str(current) + " " + str(value) + "\n")
        f.close()


def main():

    create_file_with_prices()

    pass


main()
