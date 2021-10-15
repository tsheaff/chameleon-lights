echo "Inside startup.sh"
export CHAMELEON_LOGS_FILE=/home/pi/Desktop/chameleon-logs.txt
> $CHAMELEON_LOGS_FILE
cd /home/pi/Code/chameleon-lights/python
sudo python3 ./main.py &> $CHAMELEON_LOGS_FILE