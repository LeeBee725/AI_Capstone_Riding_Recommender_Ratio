from riding_data import csv_generator as gen

# r = rc.Record()
# print(r)

log_dir = ".\\only_logs_with_user"

# user_log = "tsNTHAedYHTXAyOMs3cu0K6eKqf1\\log545975969.log"
# user_log = "01WPXP7OfDQtMeFqczOs0yoKms32\\log636094189.log"
# p = Parser()
# p.set_file_path(f"{log_dir}\\{user_log}")
# records = p.parse()
# print(records)

g = gen.CSVGenerator(log_dir)
g.count_user()
# g.generate_csv_using_n_users("riding_data_1_user_on_Top.csv", 1)
# g.generate_csv_using_n_users("riding_data_2_user_on_Top.csv", 2)
# g.generate_csv_using_n_users("riding_data_100_user_on_Top.csv", 100)
# g.generate_csv_using_n_users("riding_data_1000_user_on_Top.csv", 1000)
# g.generate_csv("riding_data.csv")
