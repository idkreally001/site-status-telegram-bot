# Site Downtime Alerter with Telegram Bot

A Python project that monitors websites for downtime and sends alerts to Telegram.

## Features

- Monitors a configurable list of websites.
- Sends instant Telegram notifications when a site is down.
- Retries with exponential backoff for temporary outages.
- Logging to keep track of monitoring activity.

## Prerequisites

- [Python 3](https://www.python.org/)
- [pip](https://packaging.python.org/tutorials/installing-packages/) (usually included with Python)

## Installation

1. Clone this repository using terminal:

    ```bash
    git clone https://github.com/idkreally001/site-status-telegram-bot.git
    ```

2. Install dependencies:

    ```bash
    cd site-status-telegram-bot
    pip install requests python-telegram-bot
    ```

## Configuration

- Get a Telegram Bot Token: Follow the instructions with Telegram's BotFather to create a new bot and get the API token. [BotFather](https://telegram.me/BotFather)
- Get your Telegram Chat ID: There are several ways to find your chat ID. There are often bots that help with this on Telegram.
- Create a `config.json` file: Place it in the root directory of the project, and specify your settings.

## Running the Application

- Start the script: 

    ```bash
    python script.py
    ```

## Additional Notes

- Log File: The script creates a file `monitoring.log` for log messages.
- Customization: The `config.json` offers several parameters to tailor the alerting behavior.
- Deployment (Optional): If deploying to a server, consider running the script as a background process for continuous monitoring.

This application can be deployed on cloud platforms for convenience and continuous monitoring. Here are a couple of popular options:

- PythonAnywhere: [PythonAnywhere](https://www.pythonanywhere.com) – PythonAnywhere offers a user-friendly platform specifically tailored for Python applications.
- Heroku: [Heroku](https://heroku.com) – Heroku is a versatile cloud platform supporting various languages, including Python.

## Contributing

This is a basic foundation! Feel free to contribute by suggesting enhancements, reporting bugs, or submitting pull requests with features or fixes.

## License

This project is licensed under the MIT License – see the [LICENSE](LICENSE) file for details.
