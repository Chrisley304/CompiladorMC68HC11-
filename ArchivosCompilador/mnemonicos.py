import xlrd
import json

mnemonicos = {}

book = xlrd.open_workbook('68HC11 SET DE INSTRUCCIONES  SIN ERRORES UNAM.xls')
sheet = book.sheet_by_index(0)

# Para los mnemonicos 1 a 77
for row in range(8,85):
	col = 1
	mnemonicos[sheet.cell_value(row,col)] = {}

    # 'IMM'
	if(sheet.cell_value(row,col + 1) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 1), str)):
			mnemonicos[sheet.cell_value(row,col)]['IMM'] = [sheet.cell_value(row,col + 1).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 3))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['IMM'] = [str(int(sheet.cell_value(row,col + 1))), int(float(str(sheet.cell_value(row,col + 3))))]
   
    # 'DIR'     
	if(sheet.cell_value(row,col + 4) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 4), str)):
			mnemonicos[sheet.cell_value(row,col)]['DIR'] = [sheet.cell_value(row,col + 4).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 6))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['DIR'] = [str(int(sheet.cell_value(row,col + 4))), int(float(str(sheet.cell_value(row,col + 6))))]
   
    # IND,X
	if(sheet.cell_value(row,col + 7) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 7), str)):
			mnemonicos[sheet.cell_value(row,col)]['IND,X'] = [sheet.cell_value(row,col + 7).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 9))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['IND,X'] = [str(int(sheet.cell_value(row,col + 7))), int(float(str(sheet.cell_value(row,col + 9))))]
   
    # IND,Y
	if(sheet.cell_value(row,col + 10) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 10), str)):
			mnemonicos[sheet.cell_value(row,col)]['IND,Y'] = [sheet.cell_value(row,col + 10).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 12))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['IND,Y'] = [str(int(sheet.cell_value(row,col + 10))), int(float(str(sheet.cell_value(row,col + 12))))]
   
    # EXT
	if(sheet.cell_value(row,col + 13) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 13), str)):
			mnemonicos[sheet.cell_value(row,col)]['EXT'] = [sheet.cell_value(row,col + 13).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 15))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['EXT'] = [str(int(sheet.cell_value(row,col + 13))), int(float(str(sheet.cell_value(row,col + 15))))]
   
    # INH
	if(sheet.cell_value(row,col + 16) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 16), str)):
			mnemonicos[sheet.cell_value(row,col)]['INH'] = [sheet.cell_value(row,col + 16).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 18))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['INH'] = [str(int(sheet.cell_value(row,col + 16))), int(float(str(sheet.cell_value(row,col + 18))))]
   
    # REL
	if(sheet.cell_value(row,col + 19) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 19), str)):
			mnemonicos[sheet.cell_value(row,col)]['REL'] = [sheet.cell_value(row,col + 19).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 21))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['REL'] = [str(int(sheet.cell_value(row,col + 19))), int(float(str(sheet.cell_value(row,col + 21))))]
   
for row in range(97,165):
	col = 1
	mnemonicos[sheet.cell_value(row,col)] = {}

    # 'IMM'
	if(sheet.cell_value(row,col + 1) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 1), str)):
			mnemonicos[sheet.cell_value(row,col)]['IMM'] = [sheet.cell_value(row,col + 1).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 3))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['IMM'] = [str(int(sheet.cell_value(row,col + 1))), str(sheet.cell_value(row,col + 3))]
   
    # 'DIR'     
	if(sheet.cell_value(row,col + 4) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 4), str)):
			mnemonicos[sheet.cell_value(row,col)]['DIR'] = [sheet.cell_value(row,col + 4).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 6))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['DIR'] = [str(int(sheet.cell_value(row,col + 4))), int(float(str(sheet.cell_value(row,col + 6))))]
   
    # IND,X
	if(sheet.cell_value(row,col + 7) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 7), str)):
			mnemonicos[sheet.cell_value(row,col)]['IND,X'] = [sheet.cell_value(row,col + 7).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 9))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['IND,X'] = [str(int(sheet.cell_value(row,col + 7))), int(float(str(sheet.cell_value(row,col + 9))))]
   
    # IND,Y
	if(sheet.cell_value(row,col + 10) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 10), str)):
			mnemonicos[sheet.cell_value(row,col)]['IND,Y'] = [sheet.cell_value(row,col + 10).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 12))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['IND,Y'] = [str(int(sheet.cell_value(row,col + 10))), int(float(str(sheet.cell_value(row,col + 12))))]
   
    # EXT
	if(sheet.cell_value(row,col + 13) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 13), str)):
			mnemonicos[sheet.cell_value(row,col)]['EXT'] = [sheet.cell_value(row,col + 13).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 15))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['EXT'] = [str(int(sheet.cell_value(row,col + 13))), int(float(str(sheet.cell_value(row,col + 15))))]
   
    # INH
	if(sheet.cell_value(row,col + 16) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 16), str)):
			mnemonicos[sheet.cell_value(row,col)]['INH'] = [sheet.cell_value(row,col + 16).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 18))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['INH'] = [str(int(sheet.cell_value(row,col + 16))), int(float(str(sheet.cell_value(row,col + 18))))]
   
    # REL
	if(sheet.cell_value(row,col + 19) != '-- '):
		if(isinstance(sheet.cell_value(row,col + 19), str)):
			mnemonicos[sheet.cell_value(row,col)]['REL'] = [sheet.cell_value(row,col + 19).replace(' ', ''), int(float(str(sheet.cell_value(row,col + 21))))]
		else:
			mnemonicos[sheet.cell_value(row,col)]['REL'] = [str(int(sheet.cell_value(row,col + 19))), int(float(str(sheet.cell_value(row,col + 21))))]
   

mnemonicos_file = open('mnemonicos.json','w')
mnemonicos_file = json.dump(mnemonicos, mnemonicos_file)		
