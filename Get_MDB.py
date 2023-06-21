import pyodbc

# 连接到MDB文件
dir_path = r'D:\chicony\Report\R1K3LB01P\20230509_PriBA96_SecB5FC\AMB00\R1K3LA01P-CT01-ATS5_Multi_Single_20221005\R1K3LA01P-CT01-ATS5_Multi_Single_20221005@20230510.MDB'
conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb)};DBQ=' + dir_path)

# 创建游标
cursor = conn.cursor()

# 执行SQL查询
cursor.execute('SELECT * FROM SPCVar')

# 获取查询结果
results = cursor.fetchall()

# 遍历结果
for row in results:
    print(row)

# 关闭连接
conn.close()


# import pyodbc

# # 列出已安装的 ODBC 驱动程序
# drivers = [driver for driver in pyodbc.drivers()]

# if drivers:
#     print("已安装的 ODBC 驱动程序：")
#     for driver in drivers:
#         print(driver)
# else:
#     print("没有找到已安装的 ODBC 驱动程序。")

# print()

# # 列出已配置的 DSN
# dsns = [dsn for dsn in pyodbc.dataSources()]

# if dsns:
#     print("已配置的 DSN：")
#     for dsn in dsns:
#         print(dsn)
# else:
#     print("没有找到已配置的 DSN。")

