import itertools
import os
from os import listdir
import csv
from typing import Iterator
from .parser import Parser
from .parser import ATTRIBUTE_COLUMNS

# TODO:Jun Parallel Processing
class CSVGenerator:
	def __init__(self, dataDirPath):
		assert self.__is_valid_dir(dataDirPath), "Invalid Path"
		self.dataDirPath = dataDirPath
		self.to_csv = []
		self.__parser = Parser()
	
	def count_user(self) -> int:
		return len(self.get_users())
	
	def get_users(self) -> list:
		return listdir(self.dataDirPath)
	
	def generate_csv(self, csvFileName:str) -> None:
		self.to_csv = self.__get_total_parsing_data_from_dirpath()
		print("[***]Writing csv ...", end="")
		self.__write_csv_file(csvFileName)
		print("Done!")

	def generate_csv_using_n_users(self, csvFileName:str, n:int) -> None:
		self.to_csv = self.__get_n_users_parsing_data_from_dirpath(n)
		print("[***]Writing csv ...", end="")
		self.__write_csv_file(csvFileName)
		print("Done!")

	def generate_csv_userList(self, csvFileName:str, userList:list) -> None:
		self.to_csv = self.__get_userList_parsing_data_from_dirpath(userList)
		print("[***]Writing csv ...", end="")
		self.__write_csv_file(csvFileName)
		print("Done!")

	def __is_valid_dir(self, dirPath:str) -> bool:
		return os.path.isdir(dirPath)
	
	def __get_total_parsing_data_from_dirpath(self) -> list[dict]:
		filePaths = self.__get_total_log_file_paths()
		return self.__merge_parsing_data_in_file_paths(filePaths)	

	def __get_n_users_parsing_data_from_dirpath(self, n:int) -> list[dict]:
		filePaths = self.__get_n_users_log_file_paths(n)
		return self.__merge_parsing_data_in_file_paths(filePaths)

	def __get_userList_parsing_data_from_dirpath(self, userList:list) -> list[dict]:
		filePaths = self.__get_userList_log_file_paths(userList)
		return self.__merge_parsing_data_in_file_paths(filePaths)

	def __get_total_log_file_paths(self)->list[str]:
		filePaths = []
		dirTreeIterator = self.__get_directory_tree_iterator_without_root()
		for (root, _, files) in dirTreeIterator:
			if self.__has_log(root):
				filePaths.extend(os.path.join(root,file) for file in files if self.__is_log_file(file))
		return filePaths

	def __get_n_users_log_file_paths(self, n:int) -> list[str]:
		filePaths = []
		dirTreeIterator = self.__get_directory_tree_iterator_without_root()
		while n > 0:
			root, _, files = next(dirTreeIterator)
			if self.__has_log(root):
				n -= 1
				filePaths.extend(os.path.join(root,file) for file in files if self.__is_log_file(file))
		return filePaths

	def __get_userList_log_file_paths(self, userList:list) -> list[dict]:
		filePaths = []
		for hash in userList:
			logDir = os.path.join(self.dataDirPath, hash, 'HistoryLog')
			for (root, _, files) in os.walk(logDir):
				filePaths.extend(os.path.join(root,file) for file in files if self.__is_log_file(file))
		return filePaths

	def __merge_parsing_data_in_file_paths(self, filePaths:str) -> list[dict]:
		result = []
		for filePath in filePaths:
			self.__parser.set_file_path(filePath)
			result += self.__parser.parse()
		return result

	def __get_directory_tree_iterator_without_root(self) -> Iterator:
		iterator = os.walk(self.dataDirPath)
		next(iterator)
		return iterator

	def __has_log(self, path:str) -> bool:
		return path.endswith("HistoryLog")

	def __is_log_file(self, fileName:str)->bool:
		return fileName.endswith(".log")

	def __write_csv_file(self, csvFileName:str) -> None:
		with open(csvFileName, 'w', newline='') as output_file:
			dict_writer = csv.DictWriter(output_file, ATTRIBUTE_COLUMNS)
			dict_writer.writeheader()
			dict_writer.writerows(self.to_csv)
