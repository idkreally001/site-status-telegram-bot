import json
import logging
import asyncio
from datetime import datetime
from telegram import Bot
import aiohttp

# Logging configuration
logging.basicConfig(filename='logs.txt', format='%(asctime)s - %(levelname)s - %(message)s', level=logging.INFO)

interval = 60 #define default interval

async def fetch_site_status(session, site):
    try:
        async with session.get(site) as response:
            status = response.status
            if status != 200:
                logging.warning(f"Unexpected response status {status} for {site}")
            return status
    except Exception as e:
        logging.error(f"Error fetching {site}: {e}")
        return None

async def send_telegram_message(bot_token, chat_id, message):
    bot = Bot(token=bot_token)
    try:
        await bot.send_message(chat_id=chat_id, text=message)
    except Exception as e:
        logging.error(f"Error sending Telegram message: {e}")

async def send_notification(bot_token, chat_id, site, previous_status, current_status):
    if current_status == 200:
        await send_available_notification(bot_token, chat_id, site, previous_status, current_status)
    else:
        await send_unavailable_notification(bot_token, chat_id, site, previous_status, current_status)

async def send_available_notification(bot_token, chat_id, site, previous_status, current_status):
    message = f"🟢{site} is now available. Status changed from {previous_status} to {current_status}."
    await send_telegram_message(bot_token, chat_id, message)

async def send_unavailable_notification(bot_token, chat_id, site, previous_status, current_status):
    message = f"🔴{site} is now unavailable. Status changed from {previous_status} to {current_status}."
    await send_telegram_message(bot_token, chat_id, message)

async def main():
    try:
        with open("config.json") as f:
            config = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        logging.error(f"Error reading config file: {e}")
        return
    
    sites = config.get("sites", [])
    chat_id = config.get("chat_id")
    bot_token = config.get("bot_token")
    
    if not all([sites, chat_id, bot_token]):
        logging.error("Missing configuration information. Please check your config.json file.")
        return
    
    # Log "Code has been deployed successfully"
    logging.info(f"Code has been deployed with {interval} sec check interval.")
    
    # Prepare message for sites
    sites_message = "\n".join(f"• {site}" for site in sites)
    await send_telegram_message(bot_token, chat_id, f"Monitoring has started for the following sites with the interval of {interval} sec:\n\n{sites_message}")

    for site in sites:
        logging.info(f"Start monitoring {site}")
        
    previous_statuses = {}

    while True:
        current_statuses = {}
        try:
            async with aiohttp.ClientSession() as session:
                tasks = [fetch_site_status(session, site) for site in sites]
                results = await asyncio.gather(*tasks)
                
                for site, status in zip(sites, results):
                    if site in previous_statuses:
                        previous_status = previous_statuses[site]
                        if status is not None and previous_status is not None and status != previous_status:
                            await send_notification(bot_token, chat_id, site, previous_status, status)
                    current_statuses[site] = status
        except Exception as e:
            logging.error(f"An error occurred: {e}")
        
        previous_statuses = current_statuses
        await asyncio.sleep(interval)

if __name__ == "__main__":
    asyncio.run(main())
