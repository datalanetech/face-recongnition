import xlrd 
from xlwt import Workbook
from  xlrd import open_workbook
import openpyxl
import sys
import sqlalchemy

  
# Give the location of the file 
  
wb = xlrd.open_workbook('data.xlsx') 
sheet = wb.sheet_by_index(0) 
sheet.cell_value(0, 0) 
  
# Extracting number of rows 
rows=sheet.nrows
def writedata(rowNumber,columnNumber,st):
    book = openpyxl.load_workbook('data.xlsx')
    sheet = book.get_sheet_by_name('Sheet2')
    sheet.cell(row=rowNumber, column=columnNumber).value = st
    book.save('data.xlsx')
# data via the write() method. 
name = sys.argv[1]
idd = sys.argv[2]
emp_id = idd
# name=input('Please Enter Your Name : ')
# emp_id=int(input('Please Enter Your Employee Id : '))
writedata(rows+1,1,rows)
writedata(rows+1,2,name)
writedata(rows+1,3,emp_id)

import sqlite3
import pandas as pd
filename="data"
con=sqlite3.connect("database.db")
wb=pd.ExcelFile(filename+'.xlsx')
for sheet in wb.sheet_names:
        df=pd.read_excel(filename+'.xlsx',sheetname=sheet,converters={'Name':str,'Emp_Id':str})
        
        df.to_sql(sheet,con, index=False,if_exists="replace")
con.commit()
con.close()
# Finally, close the Excel file 
# via the close() method
print('Your Data is Saved')