📄 README.md (Template)
Pi Network Uptime and Weather Monitor

[Overview]
Self-hosted Raspberry Pi monitoring solution that tracks:
Internet downtime
Network availability
Ethernet status
Weather conditions (temperature and weather descriptions)
Accessible via a mobile-responsive dashboard over LAN.

[Installation Instructions]
Clone the Repository:
```
git clone [YOUR_REPO_URL]
cd pi-network-monitor
```
Create and Activate Virtual Environment
```
python3 -m venv venv
source venv/bin/activate
```
Install Python Requirements
```
pip install -r requirements.txt
```

Add OpenWeatherMap API Key
Open config.py
Replace 'your_openweathermap_api_key_here' with your actual API key.

Initialize Database
```
python3 migrations/init_db.py
```
Set Up Systemd Services
```
sudo cp monitor.service /etc/systemd/system/monitor.service
sudo systemctl daemon-reload
sudo systemctl enable monitor.service
sudo systemctl start monitor.service
```

(Webapp service setup will be covered after Frontend is built)
[System Components]
Component	Description
monitor.service	Monitors internet, network, ethernet, and logs weather.
webapp.service	Hosts Flask dashboard (coming next).
SQLite database	Stores network and weather logs.

[Notes]
Logs stored under /home/pi/pi-network-monitor/database/monitor.db.
Weather data refreshed every 30 minutes.
Internet status checked every 4 seconds.
No authentication needed (internal LAN only).
