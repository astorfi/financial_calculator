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
land_value = 0.2 * initial_purchase_price
tax_rate = 0.25

# def calculate_monthly_payment(principal, annual_interest_rate, total_months):
#     """
#     Calculates the monthly mortgage payment based on the principal, annual interest rate, and total number of months.

#     Args:
#         principal (float): The principal amount of the loan.
#         annual_interest_rate (float): The annual interest rate on the loan.
#         total_months (int): The total number of months of the loan term.

#     Returns:
#         float: The monthly mortgage payment.

#     """
#     monthly_interest_rate = annual_interest_rate / 12
#     return principal * (monthly_interest_rate * (1 + monthly_interest_rate) ** total_months) / ((1 + monthly_interest_rate) ** total_months - 1)


def calculate_monthly_payment(principal, annual_interest_rate, loan_term_months):
    """
    Calculates the monthly mortgage payment using the loan amortization formula.

    Args:
        principal (float): The loan amount.
        annual_interest_rate (float): The annual interest rate.
        loan_term_months (int): The number of months for the loan term.

    Returns:
        float: The monthly mortgage payment.
    """
    monthly_interest_rate = annual_interest_rate / 12
    return principal * monthly_interest_rate * (1 + monthly_interest_rate) ** loan_term_months / ((1 + monthly_interest_rate) ** loan_term_months - 1)


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

    for year in range(2, years_to_live + years_to_rent + 1):

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


# def simulate_market_vs_real_state(years_to_live, years_to_rent, initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return):
#     """
#     Simulates the financial outcome of renting versus buying a property and investing the difference.

#     Args:
#         years_to_live (int): The number of years the person plans to live in the property.
#         years_to_rent (int): The number of years the person plans to rent after living in the property.
#         initial_purchase_price (float): The initial purchase price of the property.
#         down_payment_percentage (float): The percentage of the initial purchase price paid as a down payment.
#         buyer_closing_costs_percentage (float): The percentage of the initial purchase price paid as buyer closing costs.
#         annual_interest_rate (float): The annual interest rate on the mortgage.
#         loan_term_years (int): The number of years of the mortgage loan term.
#         property_tax_rate (float): The annual property tax rate as a decimal.
#         home_insurance_initial (float): The initial annual home insurance cost.
#         maintenance_rate (float): The annual maintenance cost as a percentage of the initial purchase price.
#         hoa_fee_initial (float): The initial monthly HOA fee.
#         hoa_fee_annual_increase (float): The annual increase in the HOA fee as a decimal.
#         inflation_rate (float): The annual inflation rate as a decimal.
#         annual_appreciation_rate (float): The annual property appreciation rate as a decimal.
#         vacancy_rate (float): The vacancy rate as a decimal.
#         property_management_fee_rate (float): The property management fee rate as a decimal.
#         price_to_rent_ratio (float): The price-to-rent ratio.
#         annual_rent_increase_rate (float): The annual rent increase rate as a decimal.
#         agent_commission_rate (float): The agent commission rate as a decimal.
#         transfer_tax_rate (float): The transfer tax rate as a decimal.
#         fixed_selling_costs (float): The fixed selling costs.
#         annual_stock_market_return (float): The annual stock market return as a decimal.

#     Returns:
#         tuple: Final investment values for both scenarios.
#     """
#     # Initial investment in the stock market for Scenario A
#     initial_investment = initial_purchase_price * \
#         (down_payment_percentage + buyer_closing_costs_percentage)
#     investment_value_A = initial_investment

#     # Initial cost for Scenario B
#     total_cost_B = initial_investment
#     investment_value_B = 0  # Initial stock market investment for positive net rental income
#     positive_cash_flow_year = 10000

#     # Calculate mortgage payment
#     monthly_payment_estimate = calculate_monthly_payment(
#         initial_purchase_price - initial_purchase_price * down_payment_percentage, annual_interest_rate, loan_term_years * 12)
#     annual_mortgage_payment = monthly_payment_estimate * 12
    
#     # Rental value estimate at the purchase time
#     monthly_rent_estimate = (initial_purchase_price / price_to_rent_ratio) / 12

#     for year in range(1, years_to_live + years_to_rent + 1):

#         annual_property_tax = initial_purchase_price * property_tax_rate * (1 + inflation_rate) ** (year - 1)
#         annual_home_insurance = home_insurance_initial * (1 + inflation_rate) ** (year - 1)
#         annual_maintenance_cost = initial_purchase_price * maintenance_rate * (1 + inflation_rate) ** (year - 1)
#         annual_hoa_fee = hoa_fee_initial * 12 * (1 + hoa_fee_annual_increase) ** (year - 1)
#         total_annual_home_cost = annual_property_tax + annual_home_insurance + annual_maintenance_cost + annual_hoa_fee


#         if year <= years_to_live:

#             # Total annual home cost while living in the house
#             total_annual_cost = annual_mortgage_payment + total_annual_home_cost

#             # Scenario A: Invest this cost in the stock market
#             investment_value_A = (
#                 investment_value_A + total_annual_cost) * (1 + annual_stock_market_return)

#             # Scenario B: Accumulate this cost
#             total_cost_B += total_annual_cost

#         else:
#             # Calculate rental income
#             monthly_rent_income = (initial_purchase_price * (1 + annual_appreciation_rate) ** (year - years_to_live) /
#                                    price_to_rent_ratio) / 12 * (1 + annual_rent_increase_rate) ** (year - years_to_live - 1)
#             annual_rent_income = monthly_rent_income * 12
#             annual_rent_income_after_vacancy = annual_rent_income * \
#                 (1 - vacancy_rate)
#             annual_property_management_fee = annual_rent_income_after_vacancy * \
#                 property_management_fee_rate
#             annual_rent_income_net = annual_rent_income_after_vacancy - \
#                 annual_property_management_fee

#             # Net annual income while renting out the house
#             net_rental_income = annual_rent_income_net - total_annual_home_cost

#             # Scenario A: If net rental income is negative, invest the negative amount in the stock market
#             if net_rental_income < 0:
#                 investment_value_A = (
#                     investment_value_A - net_rental_income) * (1 + annual_stock_market_return)
#             else:
#                 investment_value_A *= (1 + annual_stock_market_return)

#             # Scenario B: Accumulate total costs and invest positive net rental income in the stock market
#             if net_rental_income > 0:
#                 positive_cash_flow_year = year
#                 investment_value_B = (
#                     investment_value_B + net_rental_income) * (1 + annual_stock_market_return)
#             else:
#                 total_cost_B += -net_rental_income

#     # Selling the property at the end of the living period
#     final_property_value = initial_purchase_price * \
#         (1 + annual_appreciation_rate) ** years_to_live
#     selling_costs = (final_property_value * agent_commission_rate) + \
#         (final_property_value * transfer_tax_rate) + fixed_selling_costs
#     net_sale_proceeds = final_property_value - selling_costs

#     # Scenario A: Add net sale proceeds to investment value
#     investment_value_A += net_sale_proceeds

#     # Scenario B: Calculate final profit from real estate investment and add investment value from positive net rental income
#     total_profit_B = net_sale_proceeds - total_cost_B + investment_value_B

#     return investment_value_A, total_profit_B, positive_cash_flow_year

#########
#########


def calculate_annual_depreciation(purchase_price, land_value):
    depreciable_basis = purchase_price - land_value
    annual_depreciation = depreciable_basis / 27.5
    return annual_depreciation

def calculate_remaining_mortgage(principal, annual_interest_rate, total_months, payments_made):
    monthly_interest_rate = annual_interest_rate / 12
    remaining_balance = principal * ((1 + monthly_interest_rate) ** total_months - (1 + monthly_interest_rate) ** payments_made) / ((1 + monthly_interest_rate) ** total_months - 1)
    return max(remaining_balance, 0)  # Ensures the remaining balance is not negative

def calculate_taxable_income(gross_rental_income, total_expenses, annual_depreciation, tax_rate):
    taxable_income = gross_rental_income - total_expenses - annual_depreciation
    taxes = taxable_income * tax_rate if taxable_income > 0 else 0
    return taxes

# Adjust the simulation function to include depreciation and taxes
def simulate_market_vs_real_estate(years_to_live, years_to_rent, initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return, tax_rate, land_value):
    # initial_investment = initial_purchase_price * (down_payment_percentage + buyer_closing_costs_percentage)
    # investment_value_A = initial_investment
    # total_cost_B = initial_investment
    # investment_value_B = 0
    # positive_cash_flow_year = -1

    # monthly_payment = calculate_monthly_payment(initial_purchase_price - initial_purchase_price * down_payment_percentage, annual_interest_rate, loan_term_years * 12)
    # annual_mortgage_payment = monthly_payment * 12
    # annual_depreciation = calculate_annual_depreciation(initial_purchase_price, land_value)

    initial_investment = initial_purchase_price * (down_payment_percentage + buyer_closing_costs_percentage)
    investment_value_A = initial_investment
    total_cost_B = initial_investment
    investment_value_B = 0
    positive_cash_flow_year = -1

    principal = initial_purchase_price - initial_purchase_price * down_payment_percentage
    monthly_payment = calculate_monthly_payment(principal, annual_interest_rate, loan_term_years * 12)
    annual_mortgage_payment = monthly_payment * 12
    annual_depreciation = calculate_annual_depreciation(initial_purchase_price, land_value)

    data = []

    for year in range(1, years_to_live + years_to_rent + 1):
        annual_property_tax = initial_purchase_price * property_tax_rate * (1 + inflation_rate) ** (year - 1)
        annual_home_insurance = home_insurance_initial * (1 + inflation_rate) ** (year - 1)
        annual_maintenance_cost = initial_purchase_price * maintenance_rate * (1 + inflation_rate) ** (year - 1)
        annual_hoa_fee = hoa_fee_initial * 12 * (1 + hoa_fee_annual_increase) ** (year - 1)
        total_annual_home_cost = annual_property_tax + annual_home_insurance + annual_maintenance_cost + annual_hoa_fee

        if year <= years_to_live:
            total_annual_cost = annual_mortgage_payment + total_annual_home_cost
            investment_value_A = (investment_value_A + total_annual_cost) * (1 + annual_stock_market_return)
            total_cost_B += total_annual_cost
        else:
            monthly_rent_income = (initial_purchase_price * (1 + annual_appreciation_rate) ** (year - years_to_live) / price_to_rent_ratio) / 12 * (1 + annual_rent_increase_rate) ** (year - years_to_live - 1)
            annual_rent_income = monthly_rent_income * 12
            annual_rent_income_after_vacancy = annual_rent_income * (1 - vacancy_rate)
            annual_property_management_fee = annual_rent_income_after_vacancy * property_management_fee_rate

            total_expenses = annual_mortgage_payment + annual_property_tax + annual_home_insurance + annual_maintenance_cost + annual_hoa_fee + annual_property_management_fee
            taxes = calculate_taxable_income(annual_rent_income_after_vacancy, total_expenses, annual_depreciation, tax_rate)
            net_rental_income = annual_rent_income_after_vacancy - total_expenses - taxes

            if net_rental_income < 0:
                investment_value_A = (investment_value_A - net_rental_income) * (1 + annual_stock_market_return)
            else:
                investment_value_A *= (1 + annual_stock_market_return)

            if net_rental_income > 0:
                if positive_cash_flow_year == -1:
                    positive_cash_flow_year = year
                investment_value_B = (investment_value_B + net_rental_income) * (1 + annual_stock_market_return)
            else:
                total_cost_B += -net_rental_income

    final_property_value = initial_purchase_price * (1 + annual_appreciation_rate) ** years_to_live
    selling_costs = (final_property_value * agent_commission_rate) + (final_property_value * transfer_tax_rate) + fixed_selling_costs
    net_sale_proceeds = final_property_value - selling_costs

    payments_made = (years_to_live + years_to_rent) * 12
    remaining_mortgage_balance = calculate_remaining_mortgage(principal, annual_interest_rate, loan_term_years * 12, payments_made)

    total_profit_B = net_sale_proceeds - total_cost_B + investment_value_B - remaining_mortgage_balance

    return investment_value_A, total_profit_B, positive_cash_flow_year

# Function to find the break-even point by iterating over different years_to_rent
def find_break_even_point(initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return, tax_rate, land_value, max_years):
    for years_to_rent in range(1, max_years + 1):
        investment_value_A, total_profit_B, positive_cash_flow_year = simulate_market_vs_real_estate(
            0, years_to_rent, initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return, tax_rate, land_value)

        if total_profit_B >= investment_value_A:
            return years_to_rent, investment_value_A, total_profit_B

    # Return default values if no break-even point is found
    return None, None, None

######
######

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

    # Calculate mortgage payment
    monthly_payment_estimate = calculate_monthly_payment(
        initial_purchase_price - initial_purchase_price * down_payment_percentage, annual_interest_rate, loan_term_years * 12)
    
    # Rental value estimate at the purchase time
    monthly_rent_estimate = (initial_purchase_price / price_to_rent_ratio) / 12


    # market_return, real_state_return, positive_cash_flow_year = simulate_market_vs_real_state(years_to_live, years_to_rent, initial_purchase_price,
    #                                                                                           down_payment_percentage, buyer_closing_costs_percentage,
    #                                                                                           annual_interest_rate, loan_term_years, property_tax_rate,
    #                                                                                           home_insurance_initial, maintenance_rate, hoa_fee_initial,
    #                                                                                           hoa_fee_annual_increase, inflation_rate,
    #                                                                                           annual_appreciation_rate, vacancy_rate,
    #                                                                                           property_management_fee_rate,
    #                                                                                           price_to_rent_ratio, annual_rent_increase_rate,
    #                                                                                           agent_commission_rate, transfer_tax_rate,
    #                                                                                           fixed_selling_costs, annual_stock_market_return)

    # Run the simulation
    market_return, real_estate_return, positive_cash_flow_year = simulate_market_vs_real_estate(years_to_live, years_to_rent, initial_purchase_price,
                                                                                                down_payment_percentage, buyer_closing_costs_percentage,
                                                                                                annual_interest_rate, loan_term_years, property_tax_rate,
                                                                                                home_insurance_initial, maintenance_rate, hoa_fee_initial,
                                                                                                hoa_fee_annual_increase, inflation_rate,
                                                                                                annual_appreciation_rate, vacancy_rate,
                                                                                                property_management_fee_rate,
                                                                                                price_to_rent_ratio, annual_rent_increase_rate,
                                                                                                agent_commission_rate, transfer_tax_rate,
                                                                                                fixed_selling_costs, annual_stock_market_return,
                                                                                                tax_rate, land_value)
        
    
    break_even_years, investment_value_A_at_break_even, total_profit_B_at_break_even = find_break_even_point(initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return, tax_rate, land_value, 30)


    # # Define a function to find the break-even point by iterating over different years_to_rent
    # def find_break_even_point(initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return, max_years):
    #     for years_to_rent in range(1, max_years + 1):
    #         investment_value_A, total_profit_B, positive_cash_flow_year = simulate_market_vs_real_state(
    #             0, years_to_rent, initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return)

    #         if total_profit_B >= investment_value_A:
    #             return years_to_rent, investment_value_A, total_profit_B

    #     return None

    # # Find the break-even point
    # break_even_years, investment_value_A_at_break_even, total_profit_B_at_break_even = find_break_even_point(
    #     initial_purchase_price, down_payment_percentage, buyer_closing_costs_percentage, annual_interest_rate, loan_term_years, property_tax_rate, home_insurance_initial, maintenance_rate, hoa_fee_initial, hoa_fee_annual_increase, inflation_rate, annual_appreciation_rate, vacancy_rate, property_management_fee_rate, price_to_rent_ratio, annual_rent_increase_rate, agent_commission_rate, transfer_tax_rate, fixed_selling_costs, annual_stock_market_return, 30)

    # Simulate the cost of renting only
    cost_rent_only = simulate_rent_only(
        years_to_live, initial_purchase_price, price_to_rent_ratio, annual_rent_increase_rate
    )

    scenarios = ["Buy, Live, Rent, and Sell", "Market Invest"]
    profits = [real_estate_return, market_return]
    optimal_scenario = scenarios[np.argmax(profits)]
    optimal_profit = max(profits)

    return render_template('result.html', profit_buy_live_sell=profit_buy_live_sell,
                           profit_buy_live_rent_sell=real_estate_return,
                           investment_market=market_return,
                           cost_rent_only=cost_rent_only,
                           break_even_years = break_even_years,
                           monthly_payment_estimate=monthly_payment_estimate,
                           monthly_rental_estimate=monthly_rent_estimate,
                           positive_cash_flow_year = positive_cash_flow_year,
                           years_to_live=years_to_live,
                           years_to_rent=years_to_rent,
                           optimal_scenario=optimal_scenario,
                           optimal_profit=optimal_profit)


if __name__ == '__main__':
    app.run(debug=False, port=int(os.environ.get('PORT', 5000)))

    # app.run(debug=True)
