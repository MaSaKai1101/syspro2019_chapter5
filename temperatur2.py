
#coding: utf-8

from smbus2 import SMBus
import time
from datetime import date, datetime
import json
import collections as cl
import temperature

i2c_address = 0x76
bus_number = 1
bus = SMBus(bus_number)

def json_serial(obj):
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()

    raise TypeError ("Type %s not serializable" % type(obj))

def print_json(filename):
    file = open(filename, 'r')
    json_data = json.load(file)

    print("{}".format(json.dumps(json_data, indent = 4, default = json_serial)))


def write_json(filename):
	DataName_list = ["time", "temp", "pressure", "hum"]
	dt_now = datetime.now()
        value = readData_mk2()
	value_list = [dt_now, value[0], value[1], value[2]]

	ys = cl.OrderedDict()
	for g in range(len(DataName_list)):
       		data = cl.OrderedDict()
        	data["time"] = value_list[0]
        	data["temp"] = value_list[1]
        	data["pressure"] = value_list[2]
        	data["hum"] = value_list[3]

        	ys[DataName_list[g]] = data

   	file = open(filename, 'w')
    	json.dump(ys, file, indent = 4, default = json_serial)

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
	i = 0
	m = 0
	while 1:
        	time.sleep(1)
        	if(i == m * 10):
			m = m + 1			
			write_json("sample.json")
			print_json("sample.json")
		i = i + 1
