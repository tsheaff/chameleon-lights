echo "Inside startup.sh"
export CHAMELEON_LOGS_FILE=/home/pi/Desktop/chameleon-logs.txt
echo "CHAMELEON_LOGS_FILE script is $CHAMELEON_LOGS_FILE"
echo "CHAMELEON_LOGS_FILE contents 1 is $(cat $CHAMELEON_LOGS_FILE)"
> $CHAMELEON_LOGS_FILE
echo "CHAMELEON_LOGS_FILE contents 2 is $(cat $CHAMELEON_LOGS_FILE)"
cd /home/pi/Code/chameleon-lights/python
echo "$(ls -la1)"
sudo python3 ./main.py >> $CHAMELEON_LOGS_FILE
echo "CHAMELEON_LOGS_FILE contents 3 is $(cat $CHAMELEON_LOGS_FILE)"
sleep 3
echo "CHAMELEON_LOGS_FILE contents 4 is $(cat $CHAMELEON_LOGS_FILE)"