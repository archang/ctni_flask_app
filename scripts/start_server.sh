cd /home/ubuntu/server
source environment/bin/activate
nohup flask run --host 0.0.0.0 > /home/ubuntu/output.txt 2> /home/ubuntu/erro.txt &