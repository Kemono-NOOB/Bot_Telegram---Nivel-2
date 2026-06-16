from datetime import datetime as dt
from pathlib import Path
from openpyxl import load_workbook
import shutil
import os
from Modulos.motor_datos import rd_CI, rd_csv, log


Cwd = Path.cwd()
Data= Cwd / 'Archivos' / 'Departamento.csv'
rch_tplt= Cwd / 'Archivos' / 'Plantilla.xlsx'
log_arch = Cwd / 'Archivos' / 'Registro.txt'
rch_tmp = Cwd / 'Archivos' / 'temp' / 'nota_temp.xlsx'

def rch_temporal(users:list, CI:str):
	archivo=load_workbook(rch_tplt, data_only=True)
	hoja=archivo.active
	
	rch_nm:str
	try:
		in_bd=rd_CI(users,CI)
		if not in_bd[0]:
			return '',in_bd[1]
		
		else:
			ind=users[in_bd[2]]
			n1=float(ind['#1'])
			n2=float(ind['#2'])
			n3=float(ind['#3'])
			ind['Final']= str(float((n1+n2+n3)/3))
			fila=list(ind.values())
			hoja.append(fila)
			rch_nm=f"{ind['Nombre']}_NOTAS.xlsx"
		archivo.save(rch_tmp)
		print('Guardado')
		return rch_nm, in_bd[1]


	except Exception as e:
		log('ERROR AL GUARDAR TEMPORAL','rch_temporal','motor_documento.py',e)
		return '',''


def rch_final(CI: str):
	final_data=rch_temporal(rd_csv(Data), CI)
	final_lctn: Path = Cwd / 'archivos'

	if not final_data[0].endswith('.xlsx'):
		print(log(f'WRONG EXTENSION O {final_data[1]}','rch_final','motor_documento.py', final_data))
		return None, final_data[1]
	
	else:
	
		try:

			final_lctn = final_lctn / final_data[0]
			shutil.copy(rch_tmp, final_lctn)
			

			if rch_tmp.exists():
				os.remove(rch_tmp)
				return final_lctn, final_data[1]	
				

		except Exception as e:
			print(log('ERROR AL COPIAR EL ARCHIVO','rch_final', 'motor_documento.py', e))
			return None, final_data[1]

def session_data (user, msg):
	try:
		with open(log_arch,'a',encoding='utf-8') as logs:
			logs.write(f'{dt.now()}: {msg} | \t{user}\n')
			print('WASD')
	except Exception as e:
		print(log('ERROR AL GUARDAR ACTIVIDAD', 'session_data','motor_documento',e))