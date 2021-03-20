for pid in $(ps -ef |grep -i gunicorn | grep -v grep| awk '{print$2}')
do
  kill -9 $pid
done