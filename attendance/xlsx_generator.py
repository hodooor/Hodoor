from django.http import HttpResponse
import xlsxwriter
from datetime import datetime

def make_administration_report(context):
    
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename=administration_report.xlsx'
    
    workbook = xlsxwriter.Workbook(response)
    
    #formats
    bold = workbook.add_format({'bold': True})
    float_format = workbook.add_format({'num_format': '0.00'})
    
    #First Sheet
    worksheet = workbook.add_worksheet("Date")
    
    worksheet.set_column("A:A", 15)
    worksheet.set_column("B:B", 30)
    worksheet.write(0, 0, "Showed year:", bold)
    worksheet.write(0, 1, context["year"])
    worksheet.write(1, 0, "Showed month:", bold)
    worksheet.write(1, 1, context["month"])
    worksheet.write(2, 0, "Made:", bold)
    worksheet.write(2, 1, str(datetime.now()))
    
    #Second Sheet
    worksheet = workbook.add_worksheet("Users with sessions")

    worksheet.set_column("A:H", 15)
    worksheet.write(0, 0, "Last name", bold)
    worksheet.write(0, 1, "First name", bold)
    worksheet.write(0, 2, "Username", bold)
    worksheet.write(0, 3, "Work hours", bold)
    worksheet.write(0, 4, "Not work hours", bold)
    worksheet.write(0, 5, "Hours unassigned", bold)
    worksheet.write(0, 6, "Hours total", bold)
    worksheet.write(0, 7, "Status", bold)
    row = 1
    col = 0
    for user in context["user_data"]:
        worksheet.write(row, col, user["user"].last_name)
        worksheet.write(row, col + 1, user["user"].first_name)
        worksheet.write(row, col + 2, user["user"].username)
        worksheet.write_number(row, col + 3, user["hours_work"], float_format)
        worksheet.write_number(row, col + 4, user["hours_not_work"], float_format)
        worksheet.write_number(row, col + 5, user["hours_unassigned"], float_format)
        worksheet.write_number(row, col + 6, user["hours_total"], float_format)
        if user["looks_ok"]:
            worksheet.write(row, col + 7, "OK")
        else:
            worksheet.write(row, col + 7, "NOT OK")
        row += 1        
    
    #Third Sheet
    worksheet = workbook.add_worksheet("Users without sessions")

    worksheet.set_column("A:J", 15)
    worksheet.write(0, 0, "Last name", bold)
    worksheet.write(0, 1, "First name", bold)
    worksheet.write(0, 2, "Username", bold)
    row = 1
    col = 0
    for user in context["empty_users"]:
        worksheet.write(row, col, user.last_name)
        worksheet.write(row, col + 1, user.first_name)
        worksheet.write(row, col + 2, user.username)
        row += 1
    
    workbook.close()
    
    return response
