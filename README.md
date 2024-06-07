# Financial Calculator

echo "# Financial Calculator

This Financial Calculator is a web application built using Flask that allows users to simulate different real estate and investment scenarios to analyze their financial outcomes. The application provides insights into buying, living, renting, and investing in properties, helping users make informed financial decisions.

## Features

- **Simulation Scenarios**: Users can simulate various scenarios, including buying, living, renting, and selling properties, as well as investing in the stock market.
- **Financial Analysis**: The application calculates net profits, investment values, and total costs based on user inputs and predefined parameters.
- **Interactive Web Interface**: Users can interact with the application through a user-friendly web interface to input their financial parameters and view simulation results.

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

   \`\`\`bash
   cd financial-calculator
   \`\`\`

3. Install the required dependencies:

   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

### Running the Application Locally

1. Run the Flask application:

   \`\`\`bash
   python app.py
   \`\`\`

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

   \`\`\`bash
   heroku login
   \`\`\`

4. Create a new Heroku app:

   \`\`\`bash
   heroku create your-app-name
   \`\`\`

5. Deploy your code to Heroku:

   \`\`\`bash
   git push heroku master
   \`\`\`

6. Access your deployed application using the provided Heroku URL.

## Testing

To ensure the application runs smoothly, you can run automated tests on your local machine using the provided test script:

\`\`\`bash
./test_numpy_versions.sh
\`\`\`

This script tests various versions of NumPy for compatibility with the project.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, please follow these steps:

1. Fork the repository.
2. Create a new branch (\`git checkout -b feature/your-feature-name\`).
3. Make your changes and commit them (\`git commit -am 'Add new feature'\`).
4. Push your changes to your forked repository (\`git push origin feature/your-feature-name\`).
5. Create a new pull request.

## License

This project is licensed under the [MIT License](LICENSE).
" > README.md
