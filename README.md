# Stoat Steam Rich Presence Bridge

A lightweight, Dockerized Python script that syncs your current Steam game directly to your [Stoat.chat](https://stoat.chat/) custom status. It polls the Steam Web API and updates Stoat automatically, clearing your status when you stop playing.

It includes support for both the official Stoat instance and self-hosted instances.

## Prerequisites

* Docker and Docker Compose
* A Steam Web API Key (Get one [here](https://steamcommunity.com/dev/apikey))
* Your 17-digit SteamID64 (Find it using a site like [SteamID.io](https://steamid.io/))
* Your Stoat Chat session token

## Finding Your Stoat Session Token

1. Log into your Stoat instance in a web browser.
2. Open Developer Tools (`F12` or Right-Click -> Inspect).
3. Navigate to the **Network** tab and filter by **Fetch/XHR**.
4. Trigger an action in Stoat (like changing your status or sending a message).
5. Click on the resulting network request (usually named `@me` or similar).
6. Under the **Headers** tab, scroll down to **Request Headers** and copy the value next to `x-session-token`.
*Warning: Keep this token private. Never commit it to version control.*

## Setup & Deployment

1. Clone this repository to your server:
```bash
   git clone [https://github.com/YOUR_USERNAME/stoat-steam-bridge.git](https://github.com/YOUR_USERNAME/stoat-steam-bridge.git)
   cd stoat-steam-bridge

```

2. Create an environment file:
```bash
cp .env.example .env

```


3. Edit the `.env` file with your preferred text editor and add your tokens:
```env
# .env
STOAT_API_URL=[https://api.stoat.chat/users/@me](https://api.stoat.chat/users/@me)
STOAT_TOKEN=your_stoat_session_token_here
STEAM_API_KEY=your_steam_api_key_here
STEAM_ID=your_steam_id_64_here

```


*Note: If you are self-hosting Stoat, change `STOAT_API_URL` to point to your own instance.*
4. Start the container in the background:
```bash
docker compose up -d

```



## Checking Logs

If you need to verify the script is polling correctly or troubleshoot an issue, check the container logs:

```bash
docker compose logs -f

```

