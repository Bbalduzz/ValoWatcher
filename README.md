```
          ____   ____      .__         __      __        __         .__                  
          \   \ /   _____  |  |   ____/  \    /  _____ _/  |_  ____ |  |__   ___________ 
           \   Y   /\__  \ |  |  /  _ \   \/\/   \__  \\   ___/ ___\|  |  \_/ __ \_  __ \
            \     /  / __ \|  |_(  <_> \        / / __ \|  | \  \___|   Y  \  ___/|  | \/
             \___/  (____  |____/\____/ \__/\  / (____  |__|  \___  |___|  /\___  |__|   
                         \/                  \/       \/          \/     \/     \/       
                             Watch your valorant accounts locally. 
```

## 📌 Features
- **Multiple Account Support**
  - Lauch valorant with your alts easly :))
- **Profile view**
  - Level
  - XP
  - MMR
  - Rank
  - Balances
 - **Shop Checker**
   - Daily Shop
   - NightMarket (if available)
 - Last **competitive matches updates**
 - **Account Manager** (launcher)
 - **Supports 2FA Auth**. Stay safe out there.
 
 <img width="1194" alt="Screenshot 2022-10-07 at 19 48 59" src="https://user-images.githubusercontent.com/81587335/194698195-36422c6c-983b-4ece-9263-7428c7675fb5.png">
 
 ## 📝 How to get started
 1) add your valorant account(s) in `config.ini` as:
 ```ini
 [ACCOUNT1]
 riot_username = your_username_to_log_in
 password = your_password
 [ACCOUNT2]
 riot_username = your_username_to_log_in
 password = your_password
 [ACCOUNT3]
 ...
 ```
 2) install the needed modules
    - install manually with `pip install`
    - install by `requirements.txt` with `pip install -r requirements.txt`
 3) Change in `launcher.py` the `RIOTCLIENT_PATH` to the path of your `RiotClientServices.exe`
 4) run `gui.py` once inside GUI folder
   
 ## 🧱 Contributions 
Everything is welcomed :) If u want to add something and improve this tool just make a pull request and i'll check it
