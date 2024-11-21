
$excel = New-Object -ComObject Excel.Application
$excel.Visible = $false
$workbook = $excel.Workbooks.Add()
$sheet = $workbook.Worksheets.Item(1)

# Escribe datos en las celdas
$sheet.Cells.Item(1,1) = 'Nombre del proceso'
$sheet.Cells.Item(1,2) = 'Tiempo en uso (s)'
$sheet.Cells.Item(2,1) = 'opera'
$sheet.Cells.Item(2,2) = 745

# Guarda el archivo
$file = 'C:\users\danie\desktop\archivo.xlsx'
$workbook.SaveAs($file)
$excel.Quit()
