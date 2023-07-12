from socket import *
import time
from packet import *
import pickle
import serial

frserverName = "192.168.2.2"
toserverName = '192.168.1.183'
toserverPort = 12345

port = serial.Serial("/dev/ttyACM0", "9600")
#con = sqlite3.connect('SensorData_0612.db')
#cur = con.cursor()



with socket(AF_INET, SOCK_STREAM) as clientSocket:
    while True:
        # tcp 소켓 객체 (IPv4, TCP소켓)
        # clientSocket = socket(AF_INET, SOCK_STREAM)
        # 서버와 연결
        try:
            clientSocket.connect((toserverName,toserverPort))
            print("server connected")
        except Exception as e:
            print(e)
            time.sleep(1)
            continue

        # 입력값으로 패킷 생성
        try:
            data_origin = port.readline()
            data = data_origin.decode('utf-8', 'ignore')
            data = data.split(",")
            sensortime = data[0]
            windspeed = data[1].split(':')[1]
            dust = data[2].split(':')[1]
            co = int(data[3].split(':')[1])
            temp = int(data[4].split(':')[1])
            humi = int(data[5].split(':')[1])
            print (data_origin)
            print(time, windspeed, dust, co, temp, humi)

            #cur.execute("insert into sensor (windspeed, dust, co, temp, humi) values (?,?,?,?,?)", (windspeed, dust, co, temp, humi))
            #con.commit()

            now = time
            sentence = ','.join([now.strftime('%Y-%m-%d %H:%M:%S')] + data[1:])

        except KeyboardInterrupt:
            break 
        except IndexError:
            continue
        except ValueError:
            continue
        # sentence = input("input lowercase sentence:")
        packet = Packet(fr=frserverName, to=toserverName, isResponse=0, data=sentence)


        # 서버로 입력값을 보냄
        print("send packet to ", toserverName)
        serialized_packet = pickle.dumps(packet)
        print("serialized_packet",serialized_packet)

        try:
            send_packet(serialized_packet, toserverName, toserverPort)
        except Exception as e:
            print(e)
            time.sleep(1)
            continue
        # 연결을 닫음

port.close()
#db.close()
#con.close()
