
#coding: utf-8

from smbus2 import SMBus
import time
import datetime
import json
import conllections as cl
import temperature

def readData_mk2():
        data = []
        for i in range (0xF7, 0xF7+8):
                data.append(bus.read_byte_data(i2c_address,i))
        pres_raw = (data[0] << 12) | (data[1] << 4) | (data[2] >> 4)
        temp_raw = (data[3] << 12) | (data[4] << 4) | (data[5] >> 4)
        hum_raw  = (data[6] << 8)  |  data[7]

        temp_data = temperature.compensate_T(temp_raw)
        pres_data = temperature.compensate_P(pres_raw)
        hum_data = temperature.compensate_H(hum_raw)

	return temp_data, pres_data, hum_data


if __name__ == '__main__':
	DataName_list = ["time", "temp", "pressure", "hum"]
	value_list = []

	ys = cl.OrderedDict()
	i = 0
	while 1:
        	time.sleep(1)
        	i++
        	if(i == 10):
        		dt_now = datetime.datetime.now()
        		print(dt_now)
			value = readData_mk2()
			value_list = [dt_now, value[0], value[1], value[2]]

			data = cl.OrderedDict()
			data["time"] = value_list[0]
			data["temp"] = value_list[1]
			data["pressure"] = value_list[2]
			data["hum"] = value_list[3]

			ys[DataName_list] = data
