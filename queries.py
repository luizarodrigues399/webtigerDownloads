# -*- coding: utf-8 -*-
from gluon import DAL,Field
import Config, re

def resultList(rows, usuario):
	result=[]
	for index, row in enumerate(rows):
		#if ('prm_usr' in row) and usuario!=1: #usuario = 1 igual Administrador, que tem acesso a tudo
		#	prm_usr= row['prm_usr'].split(',')
		#	if str(usuario) in prm_usr:
				tupla={
				'cod': row['cod'],
				'nom':row['nom']	
				}
				result.append(tupla)
		#else:
		#	tupla={
		#		'cod': row['cod'],
		#		'nom':row['nom']	
		#		}
		#	result.append(tupla)
	return result

def operation(login):
	try: ############### TERMINAR ########################
		db=DAL(Config.DBInfoOperacaoWeb, pool_size=Config.DBPoolSize, db_codec='latin1') 
		db.define_table('opr', Field('cod'), Field ('nom'), Field('prm_usr'), rname='dbo.opr', migrate=False)
		db.define_table('usuario', Field('cod'), Field ('lgn'), rname='dbo.usr', migrate=False)
		usuario = db(db.usuario.lgn==login).select(db.usuario.cod)
		rows = db().select(db.opr.nom, db.opr.cod, db.opr.prm_usr, orderby=db.opr.nom)
		db.close()

		operations= resultList(rows, usuario[0].cod) 
		return operations	

	except Exception as e:
		print e 
		return False 	

def agent():
	try:
		db=DAL(Config.DBInfoOperacaoWeb, pool_size=Config.DBPoolSize, db_codec='latin1') 
		db.define_table('agt', Field('cod'), Field ('nom'), rname='dbo.agt', migrate=False)
		rows =  db().select(db.agt.nom, db.agt.cod, orderby=db.agt.nom)
		db.close()
		agents = resultList(rows, None)
		return agents
		
	except Exception as e:
		print e 
		return False		

def target(cod_opr):
	try:
		db=DAL(Config.DBInfoOperacaoWeb, pool_size=Config.DBPoolSize, db_codec='latin1') 

		targetAndTelephone = """select distinct alv_tel_opr.cod_alv, alv_tel_opr.cod_opr, alv_tel_opr.cod_tel, alv.cod, alv.nom, tel.num, tel.ddd from 
		operacaoWeb.dbo.cmo_alv_tel_opr alv_tel_opr join  operacaoWeb.dbo.alv alv on alv_tel_opr.cod_alv = alv.cod left join operacaoWeb.dbo.tel tel 
		on tel.cod = alv_tel_opr.cod_tel join operacaoWeb.dbo.opr opr on opr.cod= alv_tel_opr.cod_opr and alv_tel_opr.cod_opr="""+str(cod_opr)+""" order by alv.nom;"""

		alvo = db.executesql(targetAndTelephone) 
		db.close()

		result=[]
		for row in alvo:
			tupla={
				'cod': row['cod'],
				'nom': row['nom'],
				'tel': row['num'],	
				'ddd': row['ddd']
			}
			result.append(tupla)
		return result
		
	except Exception as e:
		print e 
		return False	

#==================================================================================================
def CreatingQuery (fields): 
	auxiliar = """select * from (select ROW_NUMBER() OVER (ORDER BY opr_lig.cod ASC) as row, opr_lig.cod, opr_lig.dat_hor, opr_lig.dur, alv.nom, alv.apl, alv.fot1, 
	tel.num, tel.ddd, tel.imei, opr_lig.direcao, opr_lig.num_lig, opr_lig.trs, opr_lig.obs, files.path, files.memo, interlocutor.nome """

	string ="""from operacaoWeb.dbo.cmo_opr_lig opr_lig 
	left join operacaoWeb.dbo.tel tel on opr_lig.cod_tel = tel.cod left join operacaoWeb.dbo.opr opr on opr_lig.cod_opr = opr.cod left join
	operacaoWeb.dbo.alv alv on alv.cod = opr_lig.cod_alv left join operacaoWeb.dbo.interlocutor interlocutor on opr_lig.num_lig = interlocutor.telefone
	join Wytron_voice.dbo.files files on files.id = opr_lig.id_files """ 

	if fields['agent'] != None and fields['agent'] != 'todos':
				string = string+"""join operacaoWeb.dbo.cmo_agt_opr agt_opr on opr.cod = agt_opr.cod_opr join operacaoWeb.dbo.agt agt on agt.cod = agt_opr.cod_agt where """
				string = string +  "agt.cod = '"+fields['agent']+"' and "
	else:
		string = string+' where '

	if fields['IDCall'] != None and fields['IDCall'] != '':
			string = string + "opr_lig.cod = '"+fields['IDCall']+"' and "

	if fields['directionCall'] != None and fields['directionCall'] != '':
				string = string +  "opr_lig.direcao = '"+fields['directionCall']+"' and "

	if fields['priority'] != None and fields['priority'] != '':
				string = string +  "opr_lig.prioridade = '"+fields['priority']+"' and "

	if fields['listening'] != None and fields['listening'] != '':
		if fields['listening'] == '0':
				string = string +  "(opr_lig.escutado = '"+fields['listening']+"' or opr_lig.escutado IS NULL) and "		
		else:	
				string = string +  "opr_lig.escutado = '"+fields['listening']+"' and "	

	if fields['transcription'] != None and fields['transcription'] != 'todas':
		if fields['transcription']=='naoTranscritas':
				string = string +  "(opr_lig.trs IS NULL or opr_lig.trs like '' or opr_lig.trs like ' ') and "			
		else:		
			if fields['transcriptionPart'] != None and fields['transcriptionPart'] != '':
					string = string +  "opr_lig.trs like '%"+fields['transcriptionPart']+"%' and "
			else: 	
			    string = string +  "CONVERT(VARCHAR, opr_lig.trs) <>'' and "		

	if fields['initialDate'] != None and fields['initialDate'] != '':
		initialDate= fields['initialDate'].split('-',2)
		if len(initialDate[0])<4:
			fields['initialDate'] = initialDate[2] +'-'+ initialDate[1]+'-'+initialDate[0]

		if fields['initialHour'] != None and fields['initialHour'] != '':
			string = string +  "opr_lig.dat_hor > '"+fields['initialDate']+" "+fields['initialHour']+":00.000' and "
		else: 
			string = string +  "opr_lig.dat_hor > '"+fields['initialDate']+" 00:00:00.000' and "
		
	if fields['endDate'] != None and fields['endDate'] != '':
		endDate= fields['endDate'].split('-',2)
		if len(endDate[0])<4:
			fields['endDate'] = endDate[2] +'-'+ endDate[1]+'-'+endDate[0]

		if fields['endHour'] != None and fields['endHour'] != '':
			string = string +  "opr_lig.dat_hor < '"+fields['endDate']+" "+fields['endHour']+":00.000' and "
		else: 
			string = string +  "opr_lig.dat_hor < '"+fields['endDate']+" 00:00:00.000' and "


	#===========  TELEFONE INTERLOCUTOR ==================		
	if fields['telephoneInter'] != None and fields['telephoneInter'] != '':
			if fields['DDDtelephoneInter'] != None and fields['DDDtelephoneInter'] != '':
				string = string +  "opr_lig.num_lig like '("+fields['DDDtelephoneInter']+") "+fields['telephoneInter']+"%' and "
			else:
				string = string +  "opr_lig.num_lig like '%"+fields['telephoneInter']+"%' and "	
	else:
		if fields['DDDtelephoneInter'] != None and fields['DDDtelephoneInter'] != '':
				string = string +  "opr_lig.num_lig like '("+fields['DDDtelephoneInter']+") %' and "		

	#=============================

	if fields['sinopse'] != None and fields['sinopse'] != 'todas':
		if fields['sinopse'] == 'semSinopse':
			string = string +  "(opr_lig.obs IS NULL or opr_lig.obs like '') and "	
		else:
			if fields['sinopsePart'] != None and fields['sinopsePart'] != '':
				string = string + "opr_lig.obs like '%"+fields['sinopsePart']+"%' and "
			else:
				string = string +  "CONVERT(VARCHAR, opr_lig.obs) <>'' and "

    # ========= OUTRAS TABELAS ========

    #===========  TELEFONE ALVO ==================	
	if fields['telephoneTarget'] != None and fields['telephoneTarget'] != '':
		if fields['DDDtelephoneTarget'] != None and fields['DDDtelephoneTarget'] != '':
				string = string +  "tel.ddd like '%"+fields['DDDtelephoneTarget']+"%' and tel.num like '%"+fields['telephoneTarget']+"%' and "
		else:
				string = string +  "tel.num like '%"+fields['telephoneTarget']+"%' and "
	else:
		if fields['DDDtelephoneTarget'] != None and fields['DDDtelephoneTarget'] != '':
				string = string +  "tel.ddd like '%"+fields['DDDtelephoneTarget']+"%' and "	
	#=============================				

	if fields['operation'] != None and fields['operation'] != '0': #todas
				string = string +  "opr.cod = '"+fields['operation']+"' and "
				nomOper= "select nom from operacaoWeb.dbo.opr opr where opr.cod = "+fields['operation']+";"
	else:
		nomOper= 'select nom from operacaoWeb.dbo.opr opr where opr.cod = 0'

	if fields['target'] != None and fields['target'] != 'todos':
				string = string +  "alv.cod = '"+fields['target']+"' and "

	if fields['process'] != None and fields['process'] != '':
				string = string +  "opr.num_processo = '"+fields['process']+"' and "

	if fields['callswithAudio'] != None and fields['callswithAudio'] != '':
		if fields['callswithAudio'] == 'semAudio':
				string = string +  "files.path like '' or files.path IS NULL and "
		elif fields['callswithAudio'] == 'comAudio':		
				string = string +  "files.path like '%:%' and "	 #C%	

	if re.search('and', string):			
		string = string.rsplit('and ', 1)	
	else:
		string = string.rsplit('where ', 1)	

	lenght= 'select count (opr_lig.cod) as qto '+string[0]+';'
	string = auxiliar +string[0] + ') result'
			
	result = {
		'lenght' : lenght,
		'query' : string,
		'nomOper': nomOper
	}

	return result

def Lenght_RawQuery(fields):
	try:
		query= CreatingQuery(fields) 
		#print query,'\n'

		db = DAL(Config.DBInfoOperacaoWeb, pool_size=Config.DBPoolSize, db_codec='latin1')

		lenght = db.executesql(query['lenght'], as_dict = True)
		nomOper = db.executesql(query['nomOper'], as_dict = True) 
		lenght = lenght[0]['qto']
		#print 'LENGHT:',lenght	

		result = {
		'lenght' : lenght,
		'rawQuery' : query['query'],
		'nomOper' : nomOper
		}

		return result

	except Exception as e:
		print e 
		return False

def SearchingQuery (rawQuery, start, end):
	try:
		limit= " WHERE result.row > "+start+" and result.row <= "+end+" ;"

		db = DAL(Config.DBInfoOperacaoWeb, pool_size=Config.DBPoolSize, db_codec='latin1')
		rows = db.executesql(rawQuery+limit, as_dict = True)
	  	db.close()

		return rows

	except Exception as e:
		print e 
		return False

def SearchingAll (rawQuery):
	try:
		db = DAL(Config.DBInfoOperacaoWeb, pool_size=Config.DBPoolSize, db_codec='latin1')
		rows = db.executesql(rawQuery+';', as_dict = True)
	  	db.close()

		return rows

	except Exception as e:
		print e 
		return 'Error'


def SearchingSpecific (TotalIds):
	try:
		db = DAL(Config.DBInfoOperacaoWeb, pool_size=Config.DBPoolSize, db_codec='latin1')

		fields = {
			'IDCall': None,
			'initialDate': None,
			'initialHour':None,
			'endDate':None,
			'endHour': None,
			'DDDtelephoneTarget': None,
			'telephoneTarget': None,
			'DDDtelephoneInter': None,
			'telephoneInter': None,
			'operation': None,
			'target': None,
			'agent': None,
 			'transcription': None,
 			'transcriptionPart': None,
 			'sinopse': None,
 			'sinopsePart': None,
 			'priority': None,
			'directionCall': None,
			'listening': None,
			'process': None,
			'callswithAudio': None
			}

		query= CreatingQuery (fields)
		query=query['query'].split(') result') 
		string = ','.join(TotalIds)
		rawQuery = query[0]+' where opr_lig.cod in ('+string+') ) result'
		rows = db.executesql(rawQuery, as_dict = True)		
		db.close()				
		return rows

	except Exception as e:
			print e
			return False
