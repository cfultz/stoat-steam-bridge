#!/usr/bin/env python3

import os
import time
import requests
import sys

STOAT_API_URL = os.environ.get("STOAT_API_URL", "https://api.stoat.chat/users/@me")
STOAT_TOKEN = os.environ.get("STOAT_TOKEN")
STEAM_API_KEY = os.environ.get("STEAM_API_KEY")
STEAM_ID = os.environ.get("STEAM_ID")

def check_env():
    if not all([STOAT_TOKEN, STEAM_API_KEY, STEAM_ID]):
        print("Error: Missing required environment variables.", file=sys.stderr)
        sys.exit(1)

def get_steam_game():
    url = f"https://api.steampowered.com/ISteamUser/GetPlayerSummaries/v2/?key={STEAM_API_KEY}&steamids={STEAM_ID}"
    
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()
        
        players = data.get("response", {}).get("players", [])
        if not players:
            return None
            
        player = players[0]
        return player.get("gameextrainfo")
        
    except Exception as e:
        print(f"Error fetching from Steam: {e}", file=sys.stderr)
        return None

def update_stoat_status(game_name):
    headers = {
        "x-session-token": STOAT_TOKEN,
        "Content-Type": "application/json"
    }
    
    if game_name:
        status_text = f"Playing {game_name}"
        presence = "Busy"
    else:
        status_text = ""
        presence = "Online"

    payload = {
        "status": {
            "text": status_text,
            "presence": presence
        }
    }

    try:
        response = requests.patch(STOAT_API_URL, headers=headers, json=payload, timeout=10)
        response.raise_for_status()
        print(f"Updated Stoat status to: '{status_text}'" if status_text else "Cleared Stoat status.")
    except Exception as e:
        print(f"Error updating Stoat: {e}", file=sys.stderr)

def main():
    check_env()
    print("Starting direct Steam-to-Stoat Rich Presence bridge in Docker...")
    last_game = None
    
    while True:
        current_game = get_steam_game()
        
        if current_game != last_game:
            update_stoat_status(current_game)
            last_game = current_game
            
        time.sleep(30)

if __name__ == "__main__":
    main()
