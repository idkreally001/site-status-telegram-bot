import requests
import json
import logging
import asyncio
from telegram import Bot


# Function to send message via Telegram
async def send_telegram_message(message, severity='INFO'):
    bot = Bot(token=config_data['telegram_bot_token'])
    await bot.send_message(chat_id=config_data['telegram_chat_id'], text=f"[{severity}] {message}")


# Function to check website status
async def check_website(url):
    try:
        error_count = 0
        e = None  # Initialize e with None
        for attempt in range(config_data['max_retries'] + 1):
            try:
                response = requests.get(url)
                response.raise_for_status()
                logging.info(f"Successfully retrieved URL: {url}")
                return  # Exit the function if request succeeds
            except requests.exceptions.RequestException as exception:
                error_count += 1
                e = exception  # Assign the exception to e
                logging.warning(f"Error retrieving URL {url}: {str(exception)}")
                await asyncio.sleep(2 ** attempt)  # Exponential backoff

        # If all retries fail
        await send_telegram_message(f"Failed to retrieve URL {url} after {error_count} attempts. Last error: {str(e)}",
                                    severity='ERROR')
    except Exception as exception:
        logging.error(f"An error occurred while checking website {url}: {str(exception)}")
        await send_telegram_message(
            f"An error occurred while checking website {url}. Please check logs for more information.",
            severity='ERROR')


# Main function to run the checker
async def main():
    try:
        logging.info(
            "Deployment successful, beginning the downtime alerting system for " + ";".join(
                config_data['website_urls']) + ".")
        while True:
            tasks = [check_website(url) for url in config_data['website_urls']]
            await asyncio.gather(*tasks)
            await asyncio.sleep(180)  # 180 seconds = 3 minutes
    except Exception as e:
        logging.error(f"Deployment was unsuccessful. Error code: {str(e)}")
        await send_telegram_message(
            f"Deployment was unsuccessful. Error code: {str(e)}. You can check logs for more information.",
            severity='ERROR')


if __name__ == "__main__":
    # Load configurations from JSON file
    def load_config():
        with open('config.json') as json_file:
            return json.load(json_file)


    config_data = load_config()

    # Configure logging to output to console and file
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s',
                        filename='monitoring.log', filemode='a')

    # Validate configuration data
    required_fields = ['telegram_bot_token', 'telegram_chat_id', 'website_urls', 'max_retries']
    for field in required_fields:
        if field not in config_data:
            logging.error(f"Missing required field in configuration: {field}")
            raise ValueError(f"Missing required field in configuration: {field}")

    # Print and send message for deployment
    print("Deployment successful, beginning the downtime alerting system for", " ; ".join(config_data['website_urls']))
    asyncio.run(send_telegram_message("Deployment successful, beginning the downtime alerting system for " + " ; ".join(
        config_data['website_urls']) + "."))  # No need to await here

    # Main loop
    asyncio.run(main())
