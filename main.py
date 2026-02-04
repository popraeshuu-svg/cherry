import mysql.connector
import re
from grpc_clients.client import RemnaClient
import schedule
import time
from dotenv import load_dotenv
import os

load_dotenv()

DB_HOST = os.getenv('DB_HOST')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_NAME = os.getenv('DB_NAME')
API_KEY = os.getenv('API_KEY')
RENMA_IP = os.getenv('RENMA_IP')
PORT = os.getenv('PORT')

def run_script():
    #🤘
    remna_client = RemnaClient(RENMA_IP)
    #мефедрон
    conn = mysql.connector.connect(
        host=DB_HOST, 
        port=PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME
    )

    cursor = conn.cursor()



    result = []
    users = remna_client.get_users().users
    records = remna_client.get_srh_history().records

    for user in users:
        temp = []
        for record in records:
            if record.user_uuid == user.uuid:
                if not re.match(r'^192\.168\.', record.request_ip):
                    temp.append(record.request_ip)
        devices = remna_client.get_user_hwid_devices(user.uuid).devices
        for device in devices:
            result.append({
                'user_uuid': user.uuid,
                'ips': ','.join(temp),
                'user_agent': device.user_agent,
                'model': device.device_model,
                'platform': device.platform,
                'hwid': device.hwid,
                'os_version': device.os_version
            })

    # print(result[0 python main.py])

    cursor.execute('DELETE FROM client_device')
    conn.commit()
    sql = "INSERT INTO client_device (user_uuid, ips, user_agent, model, platform, hwid, os_version) VALUES (%s, %s, %s, %s, %s, %s, %s)"

    record = result[0]

    for record in result:
        val = (
            record['user_uuid'],
            record['ips'],
            record['user_agent'],
            record['model'],
            record['platform'],
            record['hwid'],
            record['os_version']
        )
        cursor.execute(sql, val)
    conn.commit()

    print("запись добавлена.")
    cursor.close()
    conn.close()

    
schedule.every(2).hours.do(run_script)

while True:
    schedule.run_pending()
    time.sleep(60)

