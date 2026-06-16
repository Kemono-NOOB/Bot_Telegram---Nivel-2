from pathlib import Path
from datetime import datetime as dt

def log(msg:str,funcion:str='',modulo:str='main',err: object ='NO ERROR'):
    lg_msg=(f'{err} | ({funcion} - {modulo}) | {msg} || {dt.now()}')
    return lg_msg
    
def rd_csv(path:Path):
    
    if not path.exists():
        print(f'Archivo inexistente {path.absolute()}')
        return []
    else:
        try:
            with open(path,'r',encoding='utf-8') as rch:
                fila: list= rch.read().split('\n')
                #! Ojalá no tener que ver más los desgraciados CSVs despues de BDD
                desgraciadas_lineas_limpias=[linea.strip(',"\'').replace('\t',' ').replace('"','') for linea in fila]
                fila=desgraciadas_lineas_limpias
                col: list= fila[0].split(',')
                usuarios=[]
		
            for i in range (1,len(fila)):
                    values:list=[f.strip() for f in fila[i].split(',')]
                    t_user={}
                    for j in range (len(values)):
                        mark=col[j].strip()
                        value=values[j]
                        t_user[mark]=value
                    usuarios.append(t_user)
            
            return usuarios
                
                
        except Exception as e:
            log('ERROR AL LEER ARCHIVO', 'rd_csv','motor_datos.py',e)
        
            return []

def rd_CI(lista:list, CI:str):
	msg=f'({CI} | No figura en los datos guardados...)'
	in_bdd=False
	index=0
	for i in lista:
		ref=i['Cedula']
		if ref == CI:
			in_bdd=True
			if i['Estatus'] == 'Activo':
				msg=f'{CI} | Encontrado'
				return in_bdd,msg,index
			else:
				msg=f'Usuario registrado pero inactivo'
				return False, msg, None
		index+=1
	if not in_bdd:
		return in_bdd, msg, None