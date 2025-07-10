import gspread

def push_to_gsheet(data_frame, file_key, sheet_name):
    gc = gspread.service_account()
    sh = gc.open_by_key(file_key)
    worksheet = sh.worksheet(sheet_name)
    for _, row in data_frame.iterrows():
        worksheet.append_row(row.tolist(), value_input_option='RAW')