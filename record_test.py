from riding_data import csv_generator as gen

logDir = '.\\log'
users = [
	'yjCBTfEVL0dwmUFzU3GvqroV0XC3', 'UInAG3crJHZmiMg5b6Jd2IlIgwp2',
	'yrAH0r8mtkQNNejCKdBi5towyCv1',	'0gVyJmbbAzf771Qk0SvD6c1RRYY2',
	'RwES6yjNLDaBcWQOj2w3REo2JJk2',	'dXDE2tUt5IPCIaA7hAefaCbKSLL2',
	'UW0IPlU2hGOWDLgLZwA451BQyml1',	'74mbmeYO4SMCBZ0zER2fPRwZxnA3',
	'KigNlhAAcbTLyGq1WQqijP8VAjD3',	'D4HcMfTVLJdESwqzteSnZZNXEdt1',
	'BcGek89jZPWdAIXQA1x0i4BYVqc2',	'O7idtyLERQUb1L9ozVm50uxbvCD2',
	'wQmN5JirFEdKQb00Cnaz7CvmYOp1',	'jaCLifo1GhMSrqG8bFAQmhS6rsi2',
	'MkavzATNZdgZt1UZXGjgJazTEmx1',	'WfzLYPdFFoTdyCBvgdYwZF4UlkH2',
	'SvzxyAfOKZXT4dYFRZGrVx2SnbG3',	'VXBUWwvjy2NyKEuNCLzPH65XVpv2',
	'Pfq7tqblXgfQjwwLaOkTNxKkurf2',	'wWORa3eelHPOIiNEMtqxqvvTxKq2',
	'zWpiirYETyPonGd1JQmoj31SQMX2', 'QxMU72RrTqgW6Ji41W8BVeE3X2R2',
	'2Ea7BdHDdPbCo4XngUzyIX2yBou1', 'pAlhJKn8MmXx7enCI5OpcWOuOLs1',
	'77Q8hcwlfPSslea9rjAEiXDPB3R2', 'pFuJJITglrYBNn7znM7GZR0Ywb52',
	'16viBpfO0tc2DcTfeTa9TjN6Nam2', 'MTRXrY3Cp3cjLHkH3p3Jxj8LqOo2',
	'vSLlqRJlexf01nJGC5Cs3F6zcaf2', '01WPXP7OfDQtMeFqczOs0yoKms32',
	's8uvVO2cXhXMuomKpKytiuFPG513', 'OMmQkOhTgUfNdgJ6Hx9EPe7zReg1',
	'YDTSNtW1C4cAcGlAY2jwRrwMSi82', 'ueyx35DAWfhXcO1BQo6aEOePWKe2',
	'gUE4cwlGNKhePf8g1S3cAfiKqw02', 'NlSC6XZw89SVqpbYnFBOl1dSQxw2',
	'qCnCGVTvptPul1yEO7VBDErX9Y43', 'cQfrq9eo6kYvaiBb09zmde8XjrD3',
	'V8slylEWh3aB9F7wwE4wjxZ3LMr1', 'b8Ele7MCw5h8yrQH4uHuulGaUbF3',
	'PToA1efEyuf87rzWZF0SkRXr8ny1', 'r9X4RGNo6UObgNBQURdSw7Gi8Fp1',
	'rVzIqYuDhvW0iTVfoFFspj3LwBi1', 'jIgXm6uwLuc9GwTxW4OoQausc162',
	'a48Ae0rgwGYoPP4eVsjHLcfhB673', 'tKmNprTfqPQZjjAEEhCmkjoP1fn1',
	'3mcU0KJNqJhB0m2QFAzkaFqqvEh1', 'uh1sF6AqiAQN0wYLQnsTFk5txsx1',
	'khqKi7ZjhqVE9eabxr5Wjkgrz1j1', 'iCqFox3xjbbzGfZooc94qduiPSN2',
	'yrNIQAh3qiOfYaOnfCBUloEftbm1', 'TKFcRouCL1U26Ajo0G292TDhRss2',
	'NUH9SAPIFPPj64aFgMRSrSpbdJA3', 'MsMsBYIva2SYvmInH8xwVjqeG9c2',
	'lBwAzGtnnxeEo2kpZmOC3k2CViS2', 'IUv7KaY2V1M0VJnAkGP13LrwEyB3',
	'oTHOxhZDxPhFGTRhNlF766BqWDk1', 'HEDmO1H56nd6rlI8bUhbuRe1zKA3',
	'UeWTlLoudahes7rCWdatYFdDBS33', '53hbvCs6pgMwZpEMtdsWWz0zeXJ2',
	'ryyzo1zsU6eOwnb1FweBpsDmDqN2', 'QhX1lsNlijfZrW0dxJ5TeQ8mzVn2',
	'b37jkn0qakQHncVR799uXg62LgS2', 'ahpAq1Fwj8eO594l3CJ1r6kFD1K2',
	'eEg0e2E1CoP3V6LSJxUQCDacNas1', 'Hcl9J8r0SZXoyhH3dYTZmtKfqxD2',
	'rbigLzJeR8fDaHhHUua847SpCOI2', 'i8vQtKDKUYWs2WLDpyxqfEtwvib2',
	'dN4AlgMOWhRAwauOvHGYEyvLRFX2', 'EI2hZ1zjwvTddNEzgwcXF06b67D2',
	'SYU5kGoloMUz09E64Z2UGfBasCF3', 'watlo38e0TU89EyhbKwxSXX5IPN2',
	'CjeeaVX0WKSvigBXrZXc4a7q7qL2', '4DLwsZ4LLwXGDZNn1YlJmXCGTMQ2',
	'XqEDRCT5DeZFLy2BHQVNUchBpfd2', 'VgIzK2mCFCMbj1q1DRGgKzw02kh2',
	'm081RBBeFLY3VWyRw6wqIPQOqZ02', 'b6D5uc9tOvaYJ1bcDBFoVgzpaqJ3',
	'vldxzgM7mDWgdaZ5OtT9x6dfczB2', 'UbHK0LU5TBTC9GBlziHNYO6256z1',
	'ZwdobI8WEvOeHVi1l6clapY1yfh2', 'JTXKl8ZBWFgdNWGHlxwXGvxJEbO2',
	'KK9m479uH5QZBM5CHZAqlDN5MIv2', '0ChSzKE66sQX8VyC96HbVj3dK3e2']

g = gen.CSVGenerator(logDir)
g.generate_csv_userList('mapo_users.csv', users)
# g.generate_csv_using_n_users("riding_data_1_user_on_Top.csv", 1)
# g.generate_csv_using_n_users("riding_data_10_user_on_Top.csv", 10)
# g.generate_csv_using_n_users("riding_data_100_user_on_Top.csv", 100)
# g.generate_csv_using_n_users("riding_data_1000_user_on_Top.csv", 1000)
# g.generate_csv("riding_data.csv")