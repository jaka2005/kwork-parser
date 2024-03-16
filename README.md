# Kwork Parser (from now: Kwork Notifier)
***Kwork Parser*** is a [*Telegram Bot*](https://core.telegram.org/bots) to recieve notifications about the new offers in the [*Kwork*](https://kwork.ru/seller) service. (And in the future, a more convenient wrapper for its use)

# Setup
For setup the ***Kwork notifier***:

## Clone
Clone it to any place on your machine:
```bash
git clone https://github.com/jaka2005/kwork-parser.git
```
## Install requirements
```bash
pip install -r reqs.txt
```
## Set the environment variables
Create A file with name `.env` in the root of project. And fill it in as shown below:
```bash
DATABASE_URL=<database_url> # as a simple case is may be like: sqlite:///database.db
BOT_TOKEN=<bot_token> # your telegram bot token, detail here: https://core.telegram.org/bots/features#botfather
CATEGORY=<category_code> # i actually use 41 that mean `scripts and bots` in kwork service
CHAT_ID=<chat_id> # your telegram id, you can get it here: https://t.me/getmyid_bot
PERIOD=<period> # interval in minutes between parsing executings
```
To find out the category code, go to the Kwork exchange, select the desired category and get it from url as shown below:

![category_example](/docs/category.png)

# Using
And now you can just run it
```bash
python main.py
```