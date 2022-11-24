#!/usr/bin/env python3

## Imports
import requests
import telebot
import time
import json
import sys
import os

## Config
token = "your token"
bot = telebot.TeleBot(token)

## Start command
@bot.message_handler(commands=["start"])
def start(message):
    user = message.from_user.first_name
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, f"Welcome {user}")

## Usage command
@bot.message_handler(commands=["usage"])
def start(message):
    usage = "check [page] [id]\n\n--Each page has 19 IDs includes id 0"
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, usage)

## About command
@bot.message_handler(commands=["about"])
def start(message):
    about = "With this bot you can check the wanted people in FBI wanted list\nUsage: /usage\nTotal wanted: /wanted"
    bot.send_chat_action(message.chat.id, "typing")
    bot.reply_to(message, usage)

## Wanted command
@bot.message_handler(commands=["wanted"])
def wanted(message):
    response = requests.get('https://api.fbi.gov/wanted/v1/list')
    data = json.loads(response.content)
    bot.send_chat_action(
        chat_id = message.chat.id, 
        action = "typing"
    )
    bot.reply_to(
        message = message, 
        text = f"Total wanted: {data['total']}"
    )
    
## Handle messages startst with 'check'
@bot.message_handler(func=lambda message:message.text.startswith("check"))
def check(message):
    page = message.text.split()[1] 
    indx = message.text.split()[2] 

    if page.isnumeric() and indx.isnumeric():
        null = "null"
        d = "d"
        response = requests.get('https://api.fbi.gov/wanted/v1/list', params={'page': page})
        data = json.loads(response.content)
        
        target = data["items"][int(indx)]
        files_url = target["files"][0]["url"]
        reward_text = target["reward_text"]
        title = target["title"]
        description = target["description"]
        nationality = target["nationality"]
        locations = target["locations"]
        images = target["images"][0]["original"]

        result = (f"Page {page} - ID {indx}\nTerget: {title}\nNationality: {nationality}\nLocation: {locations}\n\nDescription: {description}\n\nReward: {reward_text}\n\nCheck report:\n{files_url}\n")
        bot.send_chat_action(
            chat_id = message.chat.id,
            action = "upload_photo"
            )
        bot.send_photo(
            message.chat.id, 
            images, 
            result
        )
    else:
        bot.reply_to(
            message = message, 
            text = "Invalid page or index value"
        )

## Run
bot.infinity_polling()