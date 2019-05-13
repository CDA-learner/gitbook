#!/bin/sh
PROG_NAME="/2ibot/run.py"
PROG_LOG="/2ibot/run.log"
PROG_PID=`p grep -f $PROG_NAME`
startme() {
    if  [ $PROG_PID ];then
        echo "$PROG_NAME (pid $PROG_PID) already running."
        exit 1
    fi
    source /opt/py3/bin/activate
    nohup python ${PROG_NAME} > ${PROG_LOG} 2>&1 &
    if [ "$?" != 0 ] ; then
        echo "Start failed."
        exit 1
    else
        echo " done"
        ps -ef |grep ${PROG_NAME} |grep -v grep
    fi
}

stopme() {
    pkill -f ${PROG_NAME}
    if [ "$?" != 0 ] ; then
        echo "Stop failed."
        exit 1
    else
        echo " done"
    fi 
}

case "$1" in 
    start)   startme ;;
    stop)    stopme ;;
    restart) stopme; startme ;;
    *) echo "usage: $0 start|stop|restart" >&2
       exit 1
       ;;
esac

