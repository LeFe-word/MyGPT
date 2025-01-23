sudo apt update
sudo apt install python3 python3-pip -y
pip3 install python-telegram-bot openai configparser

mkdir marmelad
cd marmelad

wget https://raw.githubusercontent.com/LeFe-word/MyGPT/main/marm5.py
wget https://raw.githubusercontent.com/LeFe-word/MyGPT/main/marmelad-bot.service
mv marmelad-bot.service /etc/systemd/system/

echo "Please enter bot token:"
read TOKEN
echo "Please enter bot open AI key:"
read APIKEY
echo "Users"
read CHAT_ID

echo "[Telegram]" > gpt.ini
echo "TOKEN = $TOKEN/n" >> gpt.ini
echo "[OpenAI]" >> gpt.ini
echo "API_KEY = $APIKEY/n" >> gpt.ini
echo "[Access]" >> gpt.ini
echo "ALLOWED_USERS = $CHAT_ID" >> gpt.ini

cd $home
sudo systemctl daemon-reload
sudo systemctl enable marmelad-bot
sudo systemctl start marmelad-bot
sudo systemctl status marmelad-bot

#sudo journalctl -u chatgpt-bot -f
