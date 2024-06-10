#!/bin/sh
# /etc/init.d/mjpg-streamer.sh
# Autor:    Ingmar Stapel
# Datum:    20190706
# Version:  1.3
# Homepage: http://custom-build-robots.com
### BEGIN INIT INFO
# Provides:          mjpg-streamer.sh
# Required-Start:    $network
# Required-Stop:     $network
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: mjpg-streamer for webcam
# Description:       Streams /dev/video0 to http://IP/?action=stream
### END INIT INFO

f_message(){
        echo "[+] $1"
}
case "$1" in
        start)
                f_message "Starting mjpg-streamer"
                /opt/mjpg-streamer/mjpg_streamer -i "/opt/mjpg-streamer/input_uvc.so -d /dev/video0 -r 800x640 -f 25" -o "/opt/mjpg-streamer/output_http.so -p 8080 -w /opt/mjpg-streamer/www -n" >> /home/pi/mjpg-streamer.log 2>&1 &
                f_message "mjpg-streamer started"
                ;;
        stop)
                f_message "Stopping mjpg-streamer..."
                killall mjpg_streamer
                f_message "mjpg-streamer stopped"
                ;;
        restart)
                f_message "Restarting daemon: mjpg-streamer"
                killall mjpg_streamer
                /opt/mjpg-streamer/mjpg_streamer -i "/opt/mjpg-streamer/input_uvc.so -d /dev/video0 -r 800x640 -f 25" -o "/opt/mjpg-streamer/output_http.so -p 8080 -w /opt/mjpg-streamer/www -n" >> /home/pi/mjpg-streamer.log 2>&1 &
                f_message "Restarted daemon: mjpg_streamer"
                ;;
        status)
                pid=`ps -A | grep mjpg_streamer | grep -v "grep" | grep -v mjpg_streamer. | awk '{print $1}' | head -n 1`
                if [ -n "$pid" ];
                then
                        f_message "mjpg-streamer is running with pid ${pid}"
                        f_message "mjpg-streamer was started with the following command line"
                        cat /proc/${pid}/cmdline ; echo ""
                else
                        f_message "Could not find mjpg-streamer running"
                fi
                ;;
        *)
                f_message "Usage: $0 {start|stop|status|restart}"
                exit 1
                ;;
esac
exit 0
