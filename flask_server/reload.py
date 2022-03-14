import os

os.system('systemctl daemon-reload')
os.system('systemctl restart nginx')
os.system('systemctl restart flaga.service')
os.system('systemctl status flaga.service')