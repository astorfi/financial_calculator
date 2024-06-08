from flask import Flask
from flask import render_template
from flask import request
import numpy as np
import os

app = Flask(__name__)

# Parameters
initial_purchase_price = 1000000
down_payment_percentage = 0.2
buyer_closing_costs_percentage = 0.03
annual_interest_rate = 0.075  # 7.5% current interest rate for home purchase
loan_term_years = 30
property_tax_rate = 0.01
home_insurance_initial = 1500
maintenance_rate = 0.01
hoa_fee_initial = 300
hoa_fee_annual_increase = 0.03
inflation_rate = 0.03
annual_appreciation_rate = 0.04
annual_stock_market_return = 0.07
vacancy_rate = 0.05
property_management_fee_rate = 0.1
price_to_rent_ratio = 20
monthly_rental_estimate = (initial_purchase_price / price_to_rent_ratio) / 12
print(f"monthly_rental_estimate: {monthly_rental_estimate}")
annual_rent_increase_rate = 0.04
agent_commission_rate = 0.055
transfer_tax_rate = 0.0025
# Title insurance, attorney fees, recording fees
fixed_selling_costs = 1500 + 1000 + 50

def calculate_monthly_payment(principal, annual_interest_rate, total_months):
    """
    Calculates the monthly mortgage payment based on the principal, annual interest rate, and total number of months.

    Args:
        principal (float): The principal amount of the loan.
        annual_interest_rate (float): The annual interest rate on the loan.
        total_months (int): The total number of months of the loan term.

    Returns:
        float: The monthly mortgage payment.

    """
    monthly_interest_rate = annual_interest_rate / 12
    return principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_months) / ((1 + monthly_interest_rate) ** total_months - 1)

def simulate_buy_live_sell(initial_purchase_price, years_to_live, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs):
    """
    Simulates the financial outcome of buying, living, and selling a home.

    Args:
        initial_purchase_price (float): The initial purchase price of the home.
        years_to_live (int): The number of years the person plans to live in the home.
        down_payment_percentage (float): The percentage of the initial purchase price paid as a down payment.
        buyer_closing_costs_percentage (float): The percentage of the initial purchase price paid as buyer closing costs.
        annual_interest_rate (float): The annual interest rate on the mortgage.
        loan_term_years (int): The number of years of the mortgage loan term.
        property_tax_rate (float): The annual property tax rate as a decimal.
        home_insurance_initial (float): The initial annual home insurance cost.
        maintenance_rate (float): The annual maintenance cost as a percentage of the initial purchase price.
        hoa_fee_initial (float): The initial monthly HOA fee.
        hoa_fee_annual_increase (float): The annual increase in the HOA fee as a decimal.
        inflation_rate (float): The annual inflation rate as a decimal.
        annual_appreciation_rate (float): The annual property appreciation rate as a decimal.
        agent_commission_rate (float): The agent commission rate as a decimal.
        transfer_tax_rate (float): The transfer tax rate as a decimal.
        fixed_selling_costs (float): The fixed selling costs.

    Returns:
        float: The net profit from selling the home after the specified number of years.

    """
    down_payment = initial_purchase_price * down_payment_percentage
    loan_amount = initial_purchase_price - down_payment
    buyer_closing_costs = initial_purchase_price * buyer_closing_costs_percentage
    monthly_payment = calculate_monthly_payment(
        loan_amount, annual_interest_rate, loan_term_years * 12)
    home_value = initial_purchase_price
    remaining_balance = loan_amount

    cumulative_home_cost = 0

    for year in range(1, years_to_live + 1):
        annual_property_tax = initial_purchase_price * \
            property_tax_rate * (1 + inflation_rate) ** (year - 1)
        annual_home_insurance = home_insurance_initial * \
            (1 + inflation_rate) ** (year - 1)
        annual_maintenance_cost = initial_purchase_price * \
            maintenance_rate * (1 + inflation_rate) ** (year - 1)
        annual_hoa_fee = hoa_fee_initial * 12 * \
            (1 + hoa_fee_annual_increase) ** (year - 1)
        total_annual_home_cost = annual_property_tax + \
            annual_home_insurance + annual_maintenance_cost + annual_hoa_fee

        for month in range(1, 13):
            interest_payment = remaining_balance * (annual_interest_rate / 12)
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

        home_value = initial_purchase_price * \
            (1 + annual_appreciation_rate) ** year
        cumulative_home_cost += total_annual_home_cost + (monthly_payment * 12)

    agent_commission = home_value * agent_commission_rate
    transfer_tax = home_value * transfer_tax_rate
    total_selling_costs = agent_commission + transfer_tax + fixed_selling_costs
    net_home_value = home_value - remaining_balance - total_selling_costs
    net_profit = net_home_value - \
        (down_payment + buyer_closing_costs + cumulative_home_cost)

    return net_profit

def simulate_buy_live_rent_sell(initial_purchase_price, years_to_live, years_to_rent, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs):
    """
    Simulates the financial outcome of buying, living, renting, and selling a home.

    Args:
        initial_purchase_price (float): The initial purchase price of the home.
        years_to_live (int): The number of years the person plans to live in the home.
        years_to_rent (int): The number of years the person plans to rent after living in the home.
        down_payment_percentage (float): The percentage of the initial purchase price paid as a down payment.
        buyer_closing_costs_percentage (float): The percentage of the initial purchase price paid as buyer closing costs.
        annual_interest_rate (float): The annual interest rate on the mortgage.
        loan_term_years (int): The number of years of the mortgage loan term.
        property_tax_rate (float): The annual property tax rate as a decimal.
        home_insurance_initial (float): The initial annual home insurance cost.
        maintenance_rate (float): The annual maintenance cost as a percentage of the initial purchase price.
        hoa_fee_initial (float): The initial monthly HOA fee.
        hoa_fee_annual_increase (float): The annual increase in the HOA fee as a decimal.
        inflation_rate (float): The annual inflation rate as a decimal.
        annual_appreciation_rate (float): The annual property appreciation rate as a decimal.
        vacancy_rate (float): The vacancy rate as a decimal.
        property_management_fee_rate (float): The property management fee rate as a decimal.
        price_to_rent_ratio (float): The price-to-rent ratio.
        annual_rent_increase_rate (float): The annual rent increase rate as a decimal.
        agent_commission_rate (float): The agent commission rate as a decimal.
        transfer_tax_rate (float): The transfer tax rate as a decimal.
        fixed_selling_costs (float): The fixed selling costs.

    Returns:
        float: The net profit from selling the home after the specified number of years, taking into account rental income.

    """
    down_payment = initial_purchase_price * down_payment_percentage
    loan_amount = initial_purchase_price - down_payment
    buyer_closing_costs = initial_purchase_price * buyer_closing_costs_percentage
    monthly_payment = calculate_monthly_payment(
        loan_amount, annual_interest_rate, loan_term_years * 12)
    home_value = initial_purchase_price
    remaining_balance = loan_amount

    cumulative_home_cost = 0
    rental_income = []

    for year in range(1, years_to_live + years_to_rent + 1):
        annual_property_tax = initial_purchase_price * \
            property_tax_rate * (1 + inflation_rate) ** (year - 1)
        annual_home_insurance = home_insurance_initial * \
            (1 + inflation_rate) ** (year - 1)
        annual_maintenance_cost = initial_purchase_price * \
            maintenance_rate * (1 + inflation_rate) ** (year - 1)
        annual_hoa_fee = hoa_fee_initial * 12 * \
            (1 + hoa_fee_annual_increase) ** (year - 1)
        total_annual_home_cost = annual_property_tax + \
            annual_home_insurance + annual_maintenance_cost + annual_hoa_fee

        for month in range(1, 13):
            interest_payment = remaining_balance * (annual_interest_rate / 12)
            principal_payment = monthly_payment - interest_payment
            remaining_balance -= principal_payment

        home_value = initial_purchase_price * \
            (1 + annual_appreciation_rate) ** year
        cumulative_home_cost += total_annual_home_cost + (monthly_payment * 12)

        if year > years_to_live:
            monthly_rent_income = (home_value / price_to_rent_ratio) / 12 * (
                1 + annual_rent_increase_rate) ** (year - years_to_live - 1)
            annual_rent_income = monthly_rent_income * 12
            annual_rent_income_after_vacancy = annual_rent_income * \
                (1 - vacancy_rate)
            annual_property_management_fee = annual_rent_income_after_vacancy * \
                property_management_fee_rate
            annual_rent_income_net = annual_rent_income_after_vacancy - annual_property_management_fee - \
                annual_property_tax - annual_home_insurance - annual_maintenance_cost
            rental_income.append(annual_rent_income_net)
        else:
            rental_income.append(0)

    agent_commission = home_value * agent_commission_rate
    transfer_tax = home_value * transfer_tax_rate
    total_selling_costs = agent_commission + transfer_tax + fixed_selling_costs
    net_home_value = home_value - remaining_balance - total_selling_costs
    net_profit = net_home_value - \
        (down_payment + buyer_closing_costs +
         cumulative_home_cost) + sum(rental_income)

    return net_profit

# Function to simulate renting and investing
def simulate_rent_invest(years_to_live, years_to_rent, initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return):
    """
    Simulates the financial outcome of renting versus buying a property and investing the difference.

    Args:
        years_to_live (int): The number of years the person plans to live in the property.
        years_to_rent (int): The number of years the person plans to rent after living in the property.
        initial_purchase_price (float): The initial purchase price of the property.
        down_payment_percentage (float): The percentage of the initial purchase price paid as a down payment.
        buyer_closing_costs_percentage (float): The percentage of the initial purchase price paid as buyer closing costs.
        annual_interest_rate (float): The annual interest rate on the mortgage.
        loan_term_years (int): The number of years of the mortgage loan term.
        property_tax_rate (float): The annual property tax rate as a decimal.
        home_insurance_initial (float): The initial annual home insurance cost.
        maintenance_rate (float): The annual maintenance cost as a percentage of the initial purchase price.
        hoa_fee_initial (float): The initial monthly HOA fee.
        hoa_fee_annual_increase (float): The annual increase in the HOA fee as a decimal.
        inflation_rate (float): The annual inflation rate as a decimal.
        annual_appreciation_rate (float): The annual property appreciation rate as a decimal.
        vacancy_rate (float): The vacancy rate as a decimal.
        property_management_fee_rate (float): The property management fee rate as a decimal.
        price_to_rent_ratio (float): The price-to-rent ratio.
        annual_rent_increase_rate (float): The annual rent increase rate as a decimal.
        agent_commission_rate (float): The agent commission rate as a decimal.
        transfer_tax_rate (float): The transfer tax rate as a decimal.
        fixed_selling_costs (float): The fixed selling costs.
        annual_stock_market_return (float): The annual stock market return as a decimal.

    Returns:
        float: The final investment value after the specified number of years.

    """
    initial_investment = initial_purchase_price * \
        (down_payment_percentage + buyer_closing_costs_percentage)
    investment_value = initial_investment

    # Calculate initial rent
    initial_monthly_rent = (initial_purchase_price / price_to_rent_ratio) / 12

    for year in range(1, years_to_live + years_to_rent + 1):
        
        # Calculate stock market return on last year's investment
        investment_value = investment_value * (1 + annual_stock_market_return)
        
        # Calculate costs of homeownership
        annual_property_tax = initial_purchase_price * \
            property_tax_rate * (1 + inflation_rate) ** (year - 1)
        annual_home_insurance = home_insurance_initial * \
            (1 + inflation_rate) ** (year - 1)
        annual_maintenance_cost = initial_purchase_price * \
            maintenance_rate * (1 + inflation_rate) ** (year - 1)
        annual_hoa_fee = hoa_fee_initial * 12 * \
            (1 + hoa_fee_annual_increase) ** (year - 1)
        total_annual_home_cost = annual_property_tax + \
            annual_home_insurance + annual_maintenance_cost + annual_hoa_fee

        if year <= years_to_live:
            # Calculate mortgage payment
            monthly_payment = calculate_monthly_payment(
                initial_purchase_price - initial_purchase_price * down_payment_percentage, annual_interest_rate, loan_term_years * 12)
            annual_mortgage_payment = monthly_payment * 12

            # Calculate difference and invest
            annual_rent = initial_monthly_rent * 12 * \
                (1 + annual_rent_increase_rate) ** (year - 1)
            investment_amount = (annual_mortgage_payment +
                                 total_annual_home_cost - annual_rent)
        else:
            # Calculate rental income
            monthly_rent_income = (initial_purchase_price * (1 + annual_appreciation_rate) ** (year - years_to_live) /
                                   price_to_rent_ratio) / 12 * (1 + annual_rent_increase_rate) ** (year - years_to_live - 1)
            annual_rent_income = monthly_rent_income * 12
            annual_rent_income_after_vacancy = annual_rent_income * \
                (1 - vacancy_rate)
            annual_property_management_fee = annual_rent_income_after_vacancy * \
                property_management_fee_rate
            annual_rent_income_net = annual_rent_income_after_vacancy - \
                annual_property_management_fee

            # Calculate difference and invest
            investment_amount = (annual_rent_income_net -
                                 total_annual_home_cost)

        # Update investment value
        investment_value = (investment_value + investment_amount)

    return investment_value


def simulate_rent_only(years_to_live, initial_purchase_price, price_to_rent_ratio, annual_rent_increase_rate):
    """
    Simulates the cumulative rent cost over a given number of years.

    Args:
        years_to_live (int): The number of years to simulate.
        initial_purchase_price (float): The initial purchase price of the property.
        price_to_rent_ratio (float): The price-to-rent ratio of the property.
        annual_rent_increase_rate (float): The annual increase rate of the rent.

    Returns:
        float: The cumulative rent cost over the specified number of years.
    """
    initial_monthly_rent = (initial_purchase_price / price_to_rent_ratio) / 12
    cumulative_rent_cost = 0

    for year in range(1, years_to_live + 1):
        annual_rent = initial_monthly_rent * 12 * \
            (1 + annual_rent_increase_rate) ** (year - 1)
        cumulative_rent_cost += annual_rent

    return cumulative_rent_cost


@app.route('/')
def index():
    return render_template('index.html',
                           initial_purchase_price=1000000,
                           down_payment_percentage=0.2,
                           buyer_closing_costs_percentage=0.03,
                           annual_interest_rate=0.075,
                           loan_term_years=30,
                           property_tax_rate=0.01,
                           home_insurance_initial=1500,
                           maintenance_rate=0.01,
                           hoa_fee_initial=300,
                           hoa_fee_annual_increase=0.03,
                           inflation_rate=0.03,
                           annual_appreciation_rate=0.04,
                           annual_stock_market_return=0.07,
                           vacancy_rate=0.05,
                           property_management_fee_rate=0.1,
                           price_to_rent_ratio=20,
                           annual_rent_increase_rate=0.04,
                           agent_commission_rate=0.055,
                           transfer_tax_rate=0.0025,
                           fixed_selling_costs=1500 + 1000 + 50,
                           years_to_live=5,
                           years_to_rent=5)


@app.route('/calculate', methods=['POST'])
def calculate():
    """
    Calculate the financial scenarios based on the form data and return the results.

    Returns:
        A rendered template with the calculated results.

    Raises:
        KeyError: If any of the required form fields are missing.

    """
    # Retrieve form data
    initial_purchase_price = float(request.form['initial_purchase_price'])
    down_payment_percentage = float(request.form['down_payment_percentage'])
    buyer_closing_costs_percentage = float(
        request.form['buyer_closing_costs_percentage'])
    annual_interest_rate = float(request.form['annual_interest_rate'])
    loan_term_years = int(request.form['loan_term_years'])
    property_tax_rate = float(request.form['property_tax_rate'])
    home_insurance_initial = float(request.form['home_insurance_initial'])
    maintenance_rate = float(request.form['maintenance_rate'])
    hoa_fee_initial = float(request.form['hoa_fee_initial'])
    hoa_fee_annual_increase = float(request.form['hoa_fee_annual_increase'])
    inflation_rate = float(request.form['inflation_rate'])
    annual_appreciation_rate = float(request.form['annual_appreciation_rate'])
    annual_stock_market_return = float(
        request.form['annual_stock_market_return'])
    vacancy_rate = float(request.form['vacancy_rate'])
    property_management_fee_rate = float(
        request.form['property_management_fee_rate'])
    price_to_rent_ratio = float(request.form['price_to_rent_ratio'])
    annual_rent_increase_rate = float(
        request.form['annual_rent_increase_rate'])
    agent_commission_rate = float(request.form['agent_commission_rate'])
    transfer_tax_rate = float(request.form['transfer_tax_rate'])
    fixed_selling_costs = float(request.form['fixed_selling_costs'])
    years_to_live = int(request.form['years_to_live'])
    years_to_rent = int(request.form['years_to_rent'])

    # Calculate the scenarios
    profit_buy_live_sell = simulate_buy_live_sell(
        initial_purchase_price, years_to_live, down_payment_percentage, buyer_closing_costs_percentage,
        annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial,
        maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate,
        annual_appreciation_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs
    )

    profit_buy_live_rent_sell = simulate_buy_live_rent_sell(
        initial_purchase_price, years_to_live, years_to_rent, down_payment_percentage,
        buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate,
        home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase,
        inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate,
        price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate,
        fixed_selling_costs
    )

    investment_rent_invest = simulate_rent_invest(
        years_to_live, years_to_rent, initial_purchase_price, down_payment_percentage,
        buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate,
        home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase,
        inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate,
        price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate,
        fixed_selling_costs, annual_stock_market_return
    )

    cost_rent_only = simulate_rent_only(
        years_to_live, initial_purchase_price, price_to_rent_ratio, annual_rent_increase_rate
    )

    scenarios = ["Buy, Live, and Sell", "Buy, Live, Rent, and Sell", "Rent and Invest", "Rent Only"]
    profits = [profit_buy_live_sell, profit_buy_live_rent_sell, investment_rent_invest, -cost_rent_only]
    optimal_scenario = scenarios[np.argmax(profits)]
    optimal_profit = max(profits)

    return render_template('result.html', profit_buy_live_sell=profit_buy_live_sell,
                        profit_buy_live_rent_sell=profit_buy_live_rent_sell,
                        investment_rent_invest=investment_rent_invest, 
                        cost_rent_only=cost_rent_only, 
                        years_to_live=years_to_live, 
                        years_to_rent=years_to_rent,
                        optimal_scenario=optimal_scenario,
                        optimal_profit=optimal_profit)



if __name__ == '__main__':
    app.run(debug=False, port=int(os.environ.get('PORT', 5000)))

    # app.run(debug=True)
