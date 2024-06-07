# Financial Calculator

This Financial Calculator is a web application built using Flask that allows users to simulate different real estate and investment scenarios to analyze their financial outcomes. The application provides insights into buying, living, renting, and investing in properties, helping users make informed financial decisions.

## Features

- **Simulation Scenarios**: Users can simulate various scenarios, including buying, living, renting, and selling properties, as well as investing in the stock market.
- **Financial Analysis**: The application calculates net profits, investment values, and total costs based on user inputs and predefined parameters.
- **Interactive Web Interface**: Users can interact with the application through a user-friendly web interface to input their financial parameters and view simulation results.


## Parameters

- **Initial Purchase Price**: The initial purchase price of the home.
- **Down Payment Percentage**: The percentage of the initial purchase price paid as a down payment.
- **Buyer Closing Costs Percentage**: The percentage of the initial purchase price paid as buyer closing costs.
- **Annual Interest Rate**: The annual interest rate on the mortgage.
- **Loan Term Years**: The number of years of the mortgage loan term.
- **Property Tax Rate**: The annual property tax rate as a decimal.
- **Home Insurance Initial**: The initial annual home insurance cost.
- **Maintenance Rate**: The annual maintenance cost as a percentage of the initial purchase price.
- **HOA Fee Initial**: The initial monthly HOA fee.
- **HOA Fee Annual Increase**: The annual increase in the HOA fee as a decimal.
- **Inflation Rate**: The annual inflation rate as a decimal.
- **Annual Appreciation Rate**: The annual property appreciation rate as a decimal.
- **Annual Stock Market Return**: The annual stock market return as a decimal.
- **Vacancy Rate**: The vacancy rate as a decimal.
- **Property Management Fee Rate**: The property management fee rate as a decimal.
- **Price to Rent Ratio**: The price-to-rent ratio.
- **Annual Rent Increase Rate**: The annual rent increase rate as a decimal.
- **Agent Commission Rate**: The agent commission rate as a decimal.
- **Transfer Tax Rate**: The transfer tax rate as a decimal.
- **Fixed Selling Costs**: Title insurance, attorney fees, and recording fees.

## More details

### 1. Scenario: Buy, Live, and Sell

In this scenario, you decide to purchase a home, live in it for a specified number of years, and then sell it. Here's how it works:

- **Initial Purchase**: You buy a property at a specified initial purchase price.
- **Down Payment**: You make a down payment, which is a percentage of the purchase price. The remainder is financed through a mortgage.
- **Mortgage Payments**: You pay monthly mortgage payments, which include both principal and interest, over the loan term.
- **Living Costs**: While living in the home, you incur additional costs such as property taxes, home insurance, maintenance, and Homeowners Association (HOA) fees. These costs can increase annually due to inflation and other factors.
- **Appreciation**: Over time, the value of your home is expected to appreciate at a specified annual rate.
- **Selling the Home**: After living in the home for the specified number of years, you sell it. The net profit is calculated by subtracting the remaining mortgage balance, selling costs (agent commissions, transfer taxes, and fixed selling costs), and the cumulative costs incurred during the years of ownership from the selling price of the home.

This scenario helps you understand the potential financial outcome of buying a home, living in it, and selling it after a certain period.

### 2. Scenario: Buy, Live, Rent, and Sell

This scenario involves buying a home, living in it for a specified number of years, renting it out for additional years, and then selling it. Here's how it works:

- **Initial Purchase**: Similar to the first scenario, you buy a property and make a down payment.
- **Living Phase**: You live in the home for a specified number of years, paying mortgage payments and incurring living costs.
- **Rental Phase**: After living in the home, you rent it out for additional years. During this period, you receive rental income, which helps offset the costs of homeownership. However, you also incur additional costs such as vacancy rates and property management fees.
- **Appreciation and Rent Increase**: Both the home value and rental income are expected to appreciate annually.
- **Selling the Home**: After the rental phase, you sell the home. The net profit is calculated similarly to the first scenario, but it also includes the rental income earned during the rental phase.

This scenario provides insights into the financial implications of renting out a home after living in it and then selling it.

### 3. Scenario: Rent and Invest

In this scenario, instead of buying a home, you choose to rent and invest the money that would have been used for the down payment and other homeownership costs. Here's how it works:

- **Initial Investment**: You invest the money that would have been used for the down payment and buyer closing costs in the stock market or other investment vehicles.
- **Renting Costs**: You rent a property and pay monthly rent, which can increase annually due to inflation.
- **Investment Growth**: Your initial investment grows over time at a specified annual stock market return rate.
- **Living Costs**: Similar to homeownership, renting also incurs living costs such as property taxes, home insurance, maintenance, and HOA fees.
- **Comparison**: The simulation calculates the final investment value after the specified number of years. This value is compared to the costs of renting to determine the financial outcome.

This scenario helps you evaluate the potential financial benefits of renting a property and investing the money that would have been used for buying a home.

### 4. Scenario: Rent Only

In this straightforward scenario, you choose to rent a property for the entire duration under consideration without any intention of purchasing a home. Here's how it works:

- **Rental Agreement**: You decide to rent a property for a specified number of years.
- **Financial Considerations**: Renting incurs regular rental payments to the landlord or property management company. These payments cover the cost of living in the rented property.
- **Rent Increase**: Over time, the rent may increase annually due to factors like inflation or adjustments in the rental market.
- **Cumulative Rent Cost**: The simulation calculates the total cost of renting over the specified number of years, considering the initial rent amount and any annual increases.

This scenario provides clarity on the total cost of renting over the designated period, helping you budget and plan your finances accordingly.

### Conclusion

These scenarios collectively offer a comprehensive view of different housing and investment strategies. By simulating each scenario, you can compare the financial outcomes and make informed decisions about whether to buy, rent, or invest your money. The application allows you to customize various parameters, providing personalized insights based on your financial situation and goals.


## Project Structure

```
├── LICENSE
├── Procfile
├── README.md
├── app.py
├── requirements.txt
├── templates
│   ├── index.html
│   └── result.html
└── test_numpy_versions.sh
```

- **LICENSE**: The license file containing the project's license information.
- **Procfile**: A file used by Heroku to specify the commands that are executed by the app on startup.
- **README.md**: This file, providing detailed information about the project.
- **app.py**: The main Python file containing the Flask application code.
- **requirements.txt**: A file listing all dependencies required to run the application.
- **templates**: A directory containing HTML templates used by the Flask application.
  - **index.html**: The HTML template for the input form page.
  - **result.html**: The HTML template for displaying simulation results.
- **test_numpy_versions.sh**: A shell script to test various versions of NumPy for compatibility with the project.

## Usage

### Installation

1. Clone the repository to your local machine:

   ```bash
   git clone https://github.com/your-username/financial-calculator.git
   ```

2. Navigate to the project directory:

   ```bash
   cd financial-calculator
   ```

3. Install the required dependencies:

   ```bash
   pip install -r requirements.txt
   ```

### Running the Application Locally

1. Run the Flask application:

   ```bash
   python app.py
   ```

2. Access the application in your web browser at \`http://localhost:5000\`.

### Usage Instructions

1. Input your financial parameters and scenario preferences on the input form page (\`index.html\`).
2. Click the "Calculate" button to simulate the selected scenario.
3. View the simulation results on the result page (\`result.html\`), including net profits, investment values, and total costs.

## Deployment

### Heroku Deployment

1. [Sign up](https://signup.heroku.com/) for a Heroku account if you don't have one.
2. Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) on your local machine.
3. Log in to Heroku using the command:

   ```bash
   heroku login
   ```

4. Create a new Heroku app:

   ```bash
   heroku create your-app-name
   ```

5. Deploy your code to Heroku:

   ```bash
   git push heroku main
   ```

6. Access your deployed application using the provided Heroku URL. Alternatively, you can use 'heroku open' in terminal.

## Testing (for Numpy only)

To ensure the application runs smoothly, you can run automated tests on your local machine using the provided test script:

```bash
./test_numpy_versions.sh
```

This script tests various versions of NumPy for compatibility with the project.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/your-feature-name`).
3. Make your changes and commit them (`git commit -am 'Add new feature'`).
4. Push your changes to your forked repository (\`git push origin feature/your-feature-name\`).
5. Create a new pull request.

## License

This project is licensed under the [MIT License](LICENSE).
" > README.md
