echo "chameleon-lights: startup.sh: Beginning"
export CHAMELEON_LOGS_FILE=/home/pi/Desktop/chameleon-logs.txt
> $CHAMELEON_LOGS_FILE
cd /home/pi/Code/chameleon-lights/python
echo "chameleon-lights: startup.sh: inside dir $(pwd)"
echo "chameleon-lights: startup.sh: about to run main.py script..."
sudo python3 ./main.py &> $CHAMELEON_LOGS_FILE