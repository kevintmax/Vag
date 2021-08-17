systemctl stop miner.service; rm -rf auto*; git clone https://github.com/kevintmax/auto.git; mkdir ~/automation; mv ~/auto/* ~/automation/; chmod +x -R ~/automation && cd ~/automation
rm /var/lite-client/ton-lite-client-test1.config.json
mv ~/automation/liteserver/1.json /var/lite-client/ton-lite-client-test1.config.json
mv ~/automation/env ~/automation/.env
rm /etc/systemd/system/miner.service; mv ~/automation/miner.service /etc/systemd/system/miner.service && systemctl daemon-reload && systemctl start miner.service
cd; rm -rf malarm.py; sudo apt-get update; apt-get install -y build-essential git cmake ccache zlib1g-dev libssl-dev python3-pip python3-requests python3-psutil && pip3 install python-telegram-bot; cp ~/automation/malarm.py ~/malarm.py; crontab ~/automation/cron*
