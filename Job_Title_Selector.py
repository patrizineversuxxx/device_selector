import openpyxl


def check_vip(job_title):
    job_title = job_title.lower()
    if ("country manager" in job_title) | (("sr" in job_title) & ("manager" in job_title)) | \
        (("senior" in job_title) & ("manager" in job_title)) | ("gm" in job_title) | \
        ("president" in job_title) | ("director" in job_title):
        return True
    else:
        return False


def check_xlsx_for_vip(params):
    workbook = openpyxl.load_workbook(params['start_file'])
    spreadsheet = workbook.active
    result_book = openpyxl.Workbook()
    result_sheet = result_book.active

    for row in spreadsheet.iter_rows():
        if check_vip(row[10].value):
            continue
        else:
            row_data = []
            # Iterate through the cells in the current row
            for cell in row:
                # Append the cell value to the row data list
                row_data.append(cell.value)
            # Write the row data to the destination worksheet
            result_sheet.append(row_data)

    result_book.save(params['middle_file'])
