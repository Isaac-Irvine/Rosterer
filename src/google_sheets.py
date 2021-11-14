from time import time
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from tabulate import tabulate

from slot import PotentialSlots
from table_parsing import parse_table

print('connecting to and downloading from google sheets...')

# connect to google sheets and download roaster data
scope = ['https://www.googleapis.com/auth/spreadsheets',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('rostering-2021-5cb1f556a1a5.json', scope)
client = gspread.authorize(creds)
spreadsheet = client.open('Roster')
jobs_cycles = spreadsheet.get_worksheet_by_id(0).get_values()
people_jobs = spreadsheet.get_worksheet_by_id(1319304401).get_values()
people_availability = spreadsheet.get_worksheet_by_id(2017819441).get_values()
roaster_hard_coding = spreadsheet.get_worksheet_by_id(940515330).get_values()
roaster_sheet = spreadsheet.get_worksheet_by_id(1316761516)

print('Parsing spreadsheets...')

roaster = parse_table(jobs_cycles, people_availability, people_jobs, roaster_hard_coding)

print('finding roster...')
start_time = time()
roaster.fill()
print(f'Took {round(time() - start_time, 5)}s')
roaster_as_table = roaster.to_table()

print(tabulate(roaster_as_table, headers='firstrow'))
print()
print(tabulate(roaster.to_table_people(), headers='firstrow'))

# put on google sheets
print('uploading to google sheets...')
cells = []
for row_num, row in enumerate(roaster_as_table):
    for col_num, cell in enumerate(row):
        cells.append(gspread.Cell(row_num + 1, col_num + 1, roaster_as_table[row_num][col_num]))
roaster_sheet.clear()
roaster_sheet.update_cells(cells)

print('done')