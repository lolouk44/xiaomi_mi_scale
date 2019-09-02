set -e

if [ ! -z "$CRON_TAIL" ]
then
    # crond running in background and log file reading every second by tail to STDOUT
    crond -s /var/spool/cron/crontabs -b -L /var/log/cron/cron.log "$@" && tail -f /var/log/cron/cron.log
else
    # crond running in foreground. log files can be retrive from /var/log/cron mount point
    crond -s /var/spool/cron/crontabs -f -L /var/log/cron/cron.log "$@"
fi