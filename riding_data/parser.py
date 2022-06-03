import struct
import datetime
import math
from typing import Iterator

ATTRIBUTE_COLUMNS = ["user", "log_file", "time", "speed", "distance", "altitude",
					 "cadence", "heart_rate", "power", "calories", "GPS_debug",
					 "battery_debug", "toque_logger", "balance_logger",
					 "bit11", "bit12", "bit13", "bit14", "bit15",
					 "start_latitude", "start_longitude", "current_latitude",
					 "current_longitude"]

RIDDING_TOPIC = ["hasPosition", "distance", "altitude", "cadence", "heart_rate",
				 "power", "calories", "GPS_debug", "battery_debug",
				 "toque_logger", "balance_logger", "bit11", "bit12",
				 "bit13", "bit14", "bit15"]

WORD_SIZE = 4
VERSION_NUMBER = 1
CONTROL_RESUME = 1
CONTROL_PAUSE = 2

class Parser:
	def __init__(self):
		self.filePath = ""
		self.__startRiddingTime = datetime.datetime(1970,1,1)
		self.__words = []
	
	def set_file_path(self, filePath) -> None:
		self.filePath = filePath

	def parse(self) -> list[dict]:
		try:
			print(f"[***]Parse {self.filePath}...", end="")
			self.__words = self.__slice_file_to_word_size(WORD_SIZE)
			records = self.__parse_words_to_records()
			print("Done!")
			return records
		except Exception as e:
			print(e, "=> Fail!")
		return list()

	# TODO:JUN need to refactoring
	def __slice_file_to_word_size(self, wordSize: int) -> list[int]:
		words = []
		with open(self.filePath, 'rb') as f:
			for chunk in iter(lambda: f.read(wordSize), ''):
				try:
					result = struct.unpack("<I", chunk)[0]
					words.append(result)
				except:
					break
		return words

	def __parse_words_to_records(self) -> list[dict]:
		version = self.__get_version()
		self.__check_invalid_version(version)
		self.__startRiddingTime = self.__get_ridding_start_datetime()
		self.__cut_version_and_ridding_start_time_from_words()
		return self.__make_records_from_words()
	
	def __get_version(self):
		return self.__words[0]

	def __check_invalid_version(self, version):
		if version != VERSION_NUMBER:
			raise ParseException("Invalid version: " + str(version))

	def __get_ridding_start_datetime(self) -> datetime:
		# NEED: 정확한 치환법 필요
		riding_start_time = f"{self.__words[2]:08x}" + f"{self.__words[1]:08x}"
		return datetime.datetime.utcfromtimestamp(int(riding_start_time, 16)/2**32) 

	def __cut_version_and_ridding_start_time_from_words(self) -> None:
		self.__words = self.__words[3:]

	def __make_records_from_words(self) -> list[dict]:
		records = [initialize_record()]
		words_iterator = iter(self.__words)
		
		isFirst = True # 첫 위치 기록을 위한 flag
		for word in words_iterator:
			record = initialize_record()
			record["user"] = self.__get_username()
			record["log_file"] = self.__get_log_file_name()
			duration = get_duration(word)
			self.__check_invalid_duration(duration)
			
			if is_control(duration):
				control = next(words_iterator)
				if is_pause_control(control):
					break
			else:
				word = next(words_iterator)
				if is_word_the_resume_control(word):
					continue
				
				record["time"] = self.__measure_time_from_start(duration)
				
				flag, speed = get_speed_n_flags(word)
				self.__check_invalid_flag(flag)
				self.__check_invalid_speed(speed)
				record["speed"] = speed

				write_ridding_topics_on_record(words_iterator, flag, record)
				isFirst = write_start_position_and_lower_flag(isFirst, flag[0], record, records[-1])

				records.append(record)
		return records[1:]

	def __get_username(self):
		return self.filePath.split('\\')[-3]

	def __get_log_file_name(self):
		return self.filePath.split('\\')[-1]

	def __check_invalid_duration(self, duration):
		if is_invalid_duration(duration):
			raise ParseException("Invalid duration: " + str(duration))

	def __measure_time_from_start(self, duration:float) -> datetime.datetime:
		if not math.isnan(duration):
			return self.__startRiddingTime + datetime.timedelta(seconds=duration)
		return datetime.datetime(1970,1,1)

	def __check_invalid_flag(self, flag):
		if is_invalid_flag(flag):
			raise ParseException("Invalid flag: " + str(flag))

	def __check_invalid_speed(self, speed):
		if is_invalid_speed(speed):
			raise ParseException("Invalid speed: " + str(speed))

def initialize_record() -> dict:
	return dict.fromkeys(ATTRIBUTE_COLUMNS, float('nan'))

def get_duration(durationInWords:int):
	return struct.unpack('!f', bytes.fromhex(f"{durationInWords:08x}"))[0]

def is_invalid_duration(duration):
	return math.isnan(duration)

def is_control(duration):
	return duration < 0

def is_pause_control(control):
	return control == CONTROL_PAUSE

def is_resume_control(control):
	return control == CONTROL_RESUME

def is_word_the_resume_control(word):
	return is_resume_control(word)

def get_speed_n_flags(data:int) -> tuple:
	flag = f"{data:032b}"[:16]
	# NEED: speed에 대한 정확한 치환법 필요
	speed = f"{data:08x}"[4:]
	if speed == "ffff":
		speed = float('nan')
		return flag, speed
	if speed == "fffe":
		return flag, speed
	speed = int(speed, base=16) / 256.0
	return flag, speed

def is_invalid_data(data):
	return data == -1

def is_invalid_flag(flag):
	return flag == "0000000000000000"

def is_invalid_speed(speed):
	return speed == "fffe"

def write_ridding_topics_on_record(words_iterator:Iterator[int], flag:str, record:dict) -> None:
	flagCpy = list(flag)
	hasPosition = False
	if flagCpy[0] == "1":
		hasPosition = True
		flagCpy[0] = "0"
	for idx, val in enumerate(flagCpy):
		if val == "1":
			record[RIDDING_TOPIC[idx]] = struct.unpack('!f', bytes.fromhex(f"{next(words_iterator):08x}"))[0]
	if hasPosition:
		mercX = next(words_iterator)
		mercY = next(words_iterator)
		record["current_latitude"] , record["current_longitude"] = get_position_from_merc(mercY, mercX)

def get_position_from_merc(mercY, mercX) -> tuple:
	latitude = math.atan(math.sinh(math.pi * (1.0 - float(mercY) / (1 << 31)))) * 180.0 / math.pi
	longitude = float(mercX) / (1 << 31) * 180.0 - 180.0
	return latitude, longitude

def write_start_position_and_lower_flag(isFirst:bool, positionIdx:str, curRecord:dict, prevRecord:dict) -> bool:
	if positionIdx == "0":
		return True
	if isFirst:
		curRecord["start_latitude"], curRecord["start_longitude"] = curRecord["current_latitude"], curRecord["current_longitude"]
	else:
		curRecord["start_latitude"], curRecord["start_longitude"] = prevRecord["start_latitude"], prevRecord["start_longitude"]
	return False

class ParseException(Exception):
	pass