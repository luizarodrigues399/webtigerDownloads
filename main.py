# -*- coding: utf-8 -*-
from flask import Flask, request, render_template, send_file, send_from_directory, redirect, make_response, stream_with_context, Response #session,
import Config, Login, queries, download, os, sys, time
from flask_jsonpify import jsonify
from datetime import datetime

session ={}

#========= FUNCOES AUXILIARES ==============
def decodeUTF_Latin(query):
	for index, item in enumerate(query):
		
		if item['trs']:
			try:
				query[index]['trs']= item['trs'].decode(encoding='UTF-8',errors='strict')
			except Exception as e:
				#print '1:',e
				try:
					query[index]['trs']= item['trs'].decode(encoding='latin-1',errors='strict') 
				except Exception as e:
					#print '2:',e
					pass
		if item['obs']:
			try:
				query[index]['obs']= item['obs'].decode(encoding='UTF-8',errors='strict') 
			except Exception as e:
				#print '1:',e
				try:
					query[index]['obs']= item['obs'].decode(encoding='latin-1',errors='strict') 
				except Exception as e:
					#print '2:',e
					pass

		if item['apl']:
			try:
				query[index]['apl']= item['apl'].decode(encoding='UTF-8',errors='strict') 
			except Exception as e:
				#print '1:',e
				try:
					query[index]['apl']= item['apl'].decode(encoding='latin-1',errors='strict') 
				except Exception as e:
					#print '2:',e
					pass

		if item['memo']:
			try:
				query[index]['memo']= item['memo'].decode(encoding='UTF-8',errors='strict') 
			except Exception as e:
				print '1:',e
				try:
					query[index]['memo']= item['memo'].decode(encoding='latin-1',errors='strict') 
				except Exception as e:
					#print '2:',e
					pass

		if item['nome']:
			try:
				query[index]['nome']= item['nome'].decode(encoding='UTF-8',errors='strict') 
			except Exception as e:
				print '1:',e
				try:
					query[index]['nome']= item['nome'].decode(encoding='latin-1',errors='strict') 
				except Exception as e:
					#print '2:',e
					pass
	return query

def decode(objeto):
	for index, item in enumerate(objeto):
		try:
				objeto[index]['nom']= item['nom'].decode(encoding='UTF-8',errors='strict') # passando str para unicode. Sem isso, dá erro. Dar Print parece não alterar nada, mas no html muda
		except Exception as e:
				#print '1:',e
				try:
					query[index]['nom']= item['nom'].decode(encoding='latin-1',errors='strict') 
				except Exception as e:
					#print '2:',e
					pass
	return objeto

def ChangeNoneToEmpty(rows):
	for index, item in enumerate(rows):  #direcao, cod, dat_hor, path, dur, row, fot1 nao avaliados
		if not item['nome']: #nome do interlocutor
			rows[index]['nome']='' 
		if not item['nom']:
			rows[index]['nom']=''
		if not item['apl']:
			rows[index]['apl']=''
		if not item['memo']:
			rows[index]['memo']=''
		if not item['trs']:
			rows[index]['trs']=''
		if not item['num']:
			rows[index]['num']=''
		if not item['imei']:
			rows[index]['imei']=''
		if not item['obs']:
			rows[index]['obs']=''
		if not item['num_lig']:
			rows[index]['num_lig']=''
		if not item['ddd']:
			rows[index]['ddd']=' '	
	return rows

def ChangingPhotoPath(rows, nameDir):
	for index, item in enumerate(rows):
		if item['fot1']:
			path= Config.ProjectDir+nameDir+'/Fotos/'+(item['fot1'])
			if os.path.isfile(path):
				rows[index]['fot1']= path
			else:
				rows[index]['fot1']=None
	return rows

def ChangingAudioPath(rows, nameDir):
	for index, item in enumerate(rows):
		path= Config.ProjectDir+nameDir+'/Audios/'+str(item['cod'])+'.wav'
		if os.path.isfile(path):
			rows[index]['path']= path
		else:
			rows[index]['path']=''
	return rows

def ChangeTimeDuration(rows):
	for index, item in enumerate(rows):
		if item['dur']:
			m, s = divmod((int)(item['dur']), 60)
			h, m = divmod(m, 60)
			rows[index]['dur']= "%dh%02dm%02ds" % (h, m, s)
		else:
			rows[index]['dur']= '00h00m00s'
	return rows	

def ChangingHTML(data, nameDir, lenght):
	data= data.replace('%20',' ')
	data= data.replace('<input type="checkbox" name="checkbox"','<input type="hidden"') 
	data= data.replace('href="/webtiger/downloads/static/favicon.ico"/','href="static/favicon.ico"')
	data= data.replace('href="/webtiger/downloads/static/style.css"','href="static/style.css"')
	data= data.replace("<form action='/webtiger/downloads/voltarPagina' style='float:right'>", '')
	data= data.replace("<button type='submit' onclick='window.stop()'>Voltar Pesquisa</button>",'')
	data= data.replace ("</form>", '', 1)
	data= data.replace ('/'+Config.ProjectDir+nameDir+'/','')
	data= data.replace('<input type="checkbox" name="checkbox"','<input type="hidden"') 
	data= data.replace('<table id="cabecalho">','<table><tr><td style="text-align: center"><div id="totalReg"><b>Total de Registros:'+str(lenght)+'</b></div> </tr></table> <table id="cabecalho" style="display:none">') 
	data= data.replace('<input type="checkbox" name="checkbox"','<input type="hidden"') 
	data= data.replace('<script src="/webtiger/downloads/static/javascript.js"></script>','')
	data= data.replace('<img src= \'/static/loading-icon.gif\' id="loading" class="modal-content"/>','') 
	data= data.replace('<button id="sair" type="submit" onclick="window.stop();">Sair</button>','') 
	data= data.replace('/webtiger/downloads/imageAudio','')
	data= data.replace('Carregando ...','')
	data= data.replace('None','')
	return data

def sortCheckboxes(quaisCheckboxes):
	TotalIds = (quaisCheckboxes.strip()).split(' ') 
	for index, item in enumerate(TotalIds):
		TotalIds [index] = (int)(item)
	TotalIds= sorted (TotalIds)	
	for index, item in enumerate(TotalIds):
		TotalIds [index] = (unicode)(item)	

	return TotalIds

def clearSession():
	session['login']=None
	session['hash']=None
	session['lenght'] = None
	session['start'] = None
	session['end'] = None
	session['rawQuery'] = None
	session['NameDir'] = None
	session['quaisCheckboxes'] = None
	session['callswithPhoto'] = None
	session['browser'] = None
	session['WORD'] = None
	session['PDF'] = None

#############################
# Total Call Function Route #
#############################

app = Flask(__name__)

@app.errorhandler(Exception)
def all_exception_handler(error):
   print '========================== \nERRO: ', error, '\n=========================='
   clearSession()
   return redirect("/")

@app.route("/voltarPagina", methods=['GET','POST'])
def voltarPagina():
	os.chdir(Config.ProjectDir) 
	return redirect("interfaceInicial")

@app.route("/carregamentoAlvo", methods=['POST'])
def LoadingTarget():
	return jsonify({ 'target': queries.target (request.json['opr']) })

@app.route('/imageAudio/<path:filename>', methods=['GET','POST'])  #'/<path:filename>'
def imageAudio(filename):
	filename = filename.rsplit('/', 1)
	return send_from_directory (filename[0], filename[1], as_attachment=True)  

@app.route('/mp3/<path:filename>', methods=['GET','POST'])   
def imageMP3(filename):
	filename = filename.rsplit('/', 1)
	file = (filename[1].rsplit('.', 1))[0]+'.mp3'
	return send_from_directory (filename[0], file, as_attachment=True)  

@app.route('/checkboxAll', methods=['POST'])
def checkboxAll():
	rowsToDownload= queries.SearchingAll(request.json['rawQuery'])
	resultado=''
	for item in rowsToDownload:
		resultado=resultado+str(item['cod'])+' '
	return jsonify(resultado)

#========================================================================================
@app.route("/")
def index():
	clearSession()
	#print 'Sessao Index:', session
	os.chdir(Config.ProjectDir) 
	return render_template('interfaceLogin.html')

@app.route("/login", methods=['GET','POST'])
def login():
	#print '\n'
	#print '*****************************'
	#print '*          Login            *'
	#print '*****************************'

	username= request.json['username'] 
	password= request.json['password']
	access= Login.run(username,password)
	if access== True:
		return jsonify(u'Login inválido ou usuário sem permissão para download de áudios')
	elif access== False:
		return jsonify(u'Erro de conexão com o Banco de Dados')
	else:
		session['login']= access['user']
		session['hash']= access['hash']
	return jsonify('ok')

@app.route("/interfaceInicial", methods=['POST','GET'])
def interfaceInicial():
	#print 'Sessao Inicio:',session
	
	if session and Login.Re_check_user(session['login'], session['hash']):
		operation= queries.operation(session['login'])
		agent = queries.agent()

		if operation == False: 
			return render_template('mainInterface.html', erro=u'Erro de carregamento de opções na Operação. Contacte o administrador do sistema')
		elif agent == False:
			return render_template('mainInterface.html', erro=u'Erro de carregamento de opções no Agente. Contacte o administrador do sistema')
		else:		
			operation= decode (operation)
			agent= decode (agent)

			#print '\n'
			#print '*****************************'
			#print '*     BUSCAR PESQUISA       *'
			#print '*****************************'
			return render_template('mainInterface.html', operation= operation, agent= agent)

	return redirect('/')

@app.route("/firstLastPage", methods=['POST', 'GET'])
def firstPage():
	#print '\n'
	#print '*****************************'
	#print '* PRIMEIRA OU ULTIMA PAGINA *'
	#print '*****************************'

	if Login.Re_check_user(session['login'], session['hash']):
		if request.method == 'POST':
			lenght= request.form['lenght'] 
			start= request.form['start'] 
			end= request.form['end'] 
			rawQuery= request.form['rawQuery'] 
			NameDir= request.form['NameDir']
			quaisCheckboxes = request.form['quaisCheckboxes']
			callswithPhoto= request.form['comFotos']	
			browser= request.form['browser']

			checkboxTotal = request.form['checkBoxTotalHidden']

			WORD = request.form['WORDhidden']	
			PDF = request.form['PDFhidden']
			print WORD, PDF

			session['lenght'] = lenght
			session['start'] = start
			session['end'] = end
			session['rawQuery'] = rawQuery
			session['NameDir'] = NameDir
			session['quaisCheckboxes'] = quaisCheckboxes
			session['callswithPhoto'] = callswithPhoto
			session['browser'] = browser

			session['checkboxTotal'] = checkboxTotal

			session['WORD'] = WORD
			session['PDF'] = PDF

		else: #GET PAGE
			lenght=	session['lenght'] 
			start=	session['start'] 
			end= session['end']  
			rawQuery= session['rawQuery'] 
			NameDir= session['NameDir'] 
			quaisCheckboxes = session['quaisCheckboxes']
			callswithPhoto = session['callswithPhoto'] 
			browser= session['browser'] 

			checkboxTotal = session['checkboxTotal']

			WORD= session['WORD'] 
			PDF= session['PDF']	

		rows= queries.SearchingQuery (rawQuery, str(start), str(end))
		rows= decode(rows)
		rows= decodeUTF_Latin(rows)
		rows = ChangeNoneToEmpty(rows)
		rows=ChangingPhotoPath(rows, NameDir)
		rows=ChangingAudioPath(rows, NameDir)
		rows= ChangeTimeDuration(rows)
		for index, item in enumerate(rows):
			rows[index]['dat_hor']=datetime.strftime(item['dat_hor'], '%d/%m/%Y %H:%M:%S')	

		return render_template('infoInterface.html', lenght = lenght, start = ((int)(start)), end = ((int)(end)), rawQuery = rawQuery, 
		query = rows, NameDir=NameDir, QueriesPerPage = Config.QueriesPerPage, quaisCheckboxes= quaisCheckboxes, fotos=callswithPhoto, 
		WORD= WORD, PDF = PDF, browser=browser, checkboxTotal=checkboxTotal)

	return redirect('/')
	
@app.route("/previousPage", methods=['POST', 'GET'])
def previousPage():
	#print '\n'
	#print '*****************************'
	#print '*     PAGINA ANTERIOR       *'
	#print '*****************************'

	if Login.Re_check_user(session['login'], session['hash']):
		if request.method == 'POST':
			lenght= request.form['lenght'] 
			start= request.form['start'] 
			end= request.form['end'] 
			rawQuery= request.form['rawQuery'] 
			NameDir = request.form['NameDir']
			quaisCheckboxes = request.form['quaisCheckboxes']
			callswithPhoto= request.form['comFotos']
			browser= request.form['browser']

			checkboxTotal = request.form['checkBoxTotalHidden']

			WORD = request.form['WORDhidden']	
			PDF = request.form['PDFhidden']
			print WORD, PDF		

			session['lenght'] = lenght
			session['start'] = start
			session['end'] = end
			session['rawQuery'] = rawQuery
			session['NameDir'] = NameDir
			session['quaisCheckboxes'] = quaisCheckboxes
			session['callswithPhoto'] = callswithPhoto
			session['browser'] = browser

			session['checkboxTotal'] = checkboxTotal

			session['WORD'] = WORD
			session['PDF'] = PDF

		else: #GET PAGE
			lenght=	session['lenght'] 
			start=	session['start'] 
			end= session['end'] 
			rawQuery= session['rawQuery'] 
			NameDir= session['NameDir'] 
			quaisCheckboxes = session['quaisCheckboxes']
			callswithPhoto = session['callswithPhoto'] 
			browser= session['browser'] 

			checkboxTotal = session['checkboxTotal']

			WORD= session['WORD'] 
			PDF= session['PDF'] 


		end= (int)(start)
		start= (int)(start) - Config.QueriesPerPage

		rows= queries.SearchingQuery (rawQuery, str(start), str(end))
		rows= decode(rows)
		rows= decodeUTF_Latin(rows)
		rows = ChangeNoneToEmpty(rows)
		rows=ChangingPhotoPath(rows, NameDir)
		rows=ChangingAudioPath(rows, NameDir)
		rows= ChangeTimeDuration(rows)
		for index, item in enumerate(rows):
			rows[index]['dat_hor']=datetime.strftime(item['dat_hor'], '%d/%m/%Y %H:%M:%S')	

		return render_template('infoInterface.html', lenght = lenght, start = start, end = end, rawQuery = rawQuery, query = rows, 
		NameDir=NameDir, QueriesPerPage = Config.QueriesPerPage, quaisCheckboxes= quaisCheckboxes, fotos=callswithPhoto, WORD= WORD, PDF = PDF,
		 browser=browser, checkboxTotal=checkboxTotal)
	
	return redirect('/')	
		
@app.route("/nextPage", methods=['POST', 'GET'])
def nextPage():
	#print '\n'
	#print '*****************************'
	#print '*      PROXIMA PAGINA       *'
	#print '*****************************'

	if Login.Re_check_user(session['login'], session['hash']):
		if request.method == 'POST':
			lenght= request.form['lenght'] 
			start= request.form['start'] 
			end= request.form['end'] 
			rawQuery= request.form['rawQuery'] 
			NameDir = request.form['NameDir']
			quaisCheckboxes = request.form['quaisCheckboxes']
			callswithPhoto= request.form['comFotos']
			browser= request.form['browser']

			checkboxTotal = request.form['checkBoxTotalHidden']

			WORD = request.form['WORDhidden']	
			PDF = request.form['PDFhidden']
			print WORD, PDF
	
			session['lenght'] = lenght
			session['start'] = start
			session['end'] = end
			session['rawQuery'] = rawQuery
			session['NameDir'] = NameDir
			session['quaisCheckboxes'] = quaisCheckboxes
			session['callswithPhoto'] = callswithPhoto
			session['browser'] = browser

			session['checkboxTotal'] = checkboxTotal

			session['WORD'] = WORD
			session['PDF'] = PDF

		else: #GET PAGE
			lenght=	session['lenght'] 
			start=	session['start'] 
			end= session['end']  
			rawQuery= session['rawQuery'] 
			NameDir= session['NameDir'] 
			quaisCheckboxes = session['quaisCheckboxes']
			callswithPhoto = session['callswithPhoto'] 
			browser= session['browser'] 

			checkboxTotal = session['checkboxTotal'] 

			WORD= session['WORD'] 
			PDF= session['PDF'] 

		start =  (int)(end)
		end = (int)(end) + Config.QueriesPerPage

		rows= queries.SearchingQuery (rawQuery, str(start), str(end))
		rows= decode(rows)
		rows= decodeUTF_Latin(rows)
		rows = ChangeNoneToEmpty(rows)
		rows= ChangingPhotoPath(rows, NameDir)
		rows= ChangingAudioPath(rows, NameDir)
		rows= ChangeTimeDuration(rows)
		for index, item in enumerate(rows):
			rows[index]['dat_hor']=datetime.strftime(item['dat_hor'], '%d/%m/%Y %H:%M:%S')	

		return render_template('infoInterface.html', lenght = lenght, start = start, end = end, rawQuery = rawQuery, query = rows, NameDir=NameDir, 
		QueriesPerPage = Config.QueriesPerPage, quaisCheckboxes= quaisCheckboxes, fotos=callswithPhoto, WORD= WORD, PDF = PDF, 
		browser=browser, checkboxTotal=checkboxTotal) 
	return redirect('/')			
	
@app.route("/search", methods=['POST']) 
def search():
	if Login.Re_check_user(session['login'], session['hash']):
		#print '\n'
		#print '*****************************'
		#print '*          FIELDS           *'
		#print '*****************************'

		fields = {
				'IDCall': request.json['IDCall'],
				'initialDate': request.json['initialDate'],
				'initialHour': request.json['initialHourHidden'],
				'endDate': request.json['endDate'],
				'endHour': request.json['endHourHidden'],
				'DDDtelephoneTarget':request.json['DDDtelephoneTarget'],
				'telephoneTarget': request.json['telephoneTarget'],
				'DDDtelephoneInter':request.json['DDDtelephoneInter'],
				'telephoneInter': request.json['telephoneInter'],
				'operation': request.json['operation'],
				'target': request.json['target'],
				'agent': request.json['agent'],
	 			'transcription': request.json['transcription'],
	 			'transcriptionPart': request.json['transcriptionPartHidden'],
	 			'sinopse': request.json['sinopse'],
	 			'sinopsePart': request.json['sinopsePartHidden'],
	 			'priority': request.json['priority'],
				'directionCall': request.json['directionCall'],
				'listening': request.json['listening'],
				'process': request.json['process'],
				'callswithAudio': request.json['callswithAudio'],
				'callswithPhoto': request.json['callswithPhoto']
			}

		browser= request.json['browser']

		#print fields,'\n'

		#print '*****************************'
		#print '*          QUERY            *'
		#print '*****************************'
		result =  queries.Lenght_RawQuery(fields)
		if result == False:
			return jsonify(u'Erro de conexão com o Banco de Dados')

		lenght = result['lenght']
		rawQuery = result ['rawQuery']
		nomOper = result ['nomOper']
		comFoto= fields['callswithPhoto']
		rows= queries.SearchingQuery (rawQuery, '0', str(Config.QueriesPerPage))
		rowsToDownload= queries.SearchingAll(rawQuery)

		if rows !=False or rowsToDownload !=False:
			if len (rows)>0: 
				rows= decode(rows)
				rows= decodeUTF_Latin(rows)
				rows = ChangeNoneToEmpty(rows)
				rowsToDownload= decode(rowsToDownload)
				rowsToDownload= decodeUTF_Latin(rowsToDownload)
				NameDir=download.nameDir(nomOper)
				download.CreateDir(NameDir)

				for index, item in enumerate(rows):
					rows[index]['dat_hor']=datetime.strftime(item['dat_hor'], '%d/%m/%Y %H:%M:%S')

				data={
					'rows': rows,
					'rowsToDownload': rowsToDownload,
					'lenght': lenght,
					'rawQuery': rawQuery,
					'nomOper': nomOper,
					'browser': browser, 
					'comFoto': comFoto,
					'NameDir': NameDir
				}

				return jsonify(data)
			return jsonify(render_template('infoInterface.html', lenght = lenght, start = 0, end = Config.QueriesPerPage, rawQuery= rawQuery, query =rows, 
			NameDir= '', QueriesPerPage = Config.QueriesPerPage, quaisCheckboxes= '', fotos=comFoto, browser=browser)) # nao existe registro (tela)
		else:
			return jsonify(u'Erro de conexão com o Banco de Dados')
	return jsonify(u'Sessão Expirada') 
		
@app.route("/transferDataServer", methods=['POST']) 
def transferDataServer():
	file= request.json['file']
	NameDir= request.json['NameDir']
	i = request.json['i']

	erroConexao = download.transferAudios(file, i, NameDir)
	if erroConexao == False:
		return jsonify(u'Erro de conexão com o FTP')
	else:
		download.convertAudio(file, NameDir, i)
		if request.json['comFoto']=='comFoto':
			download.transferPhotos(file, NameDir, i)
		return jsonify( {'data':file, 'i': str(i)})

@app.route("/renderPage", methods=['POST']) 
def renderPage():
	rows= request.json['rows']
	NameDir= request.json['NameDir']
	lenght = request.json['lenght']
	rawQuery = request.json['rawQuery']
	comFoto = request.json['comFoto']
	browser = request.json['browser']

	rows= ChangingPhotoPath(rows, NameDir)
	rows= ChangingAudioPath(rows, NameDir)
	rows= ChangeTimeDuration(rows)

	return jsonify(render_template('infoInterface.html', lenght = lenght, start = 0, end = Config.QueriesPerPage, rawQuery= rawQuery, query =rows, 
	NameDir= NameDir, QueriesPerPage = Config.QueriesPerPage, quaisCheckboxes= '', fotos=comFoto, browser=browser)) #checkboxAll='n',	

@app.route("/downloadHTML", methods=['POST']) 
def downloadsHTML():
	#print '\n'
	#print '*****************************'
	#print '*   DOWNLOAD NO CLIENTE     *'
	#print '*****************************'

	if Login.Re_check_user(session['login'], session['hash']):
		NameDir= request.json['NameDir']
		downloadToken = request.json['downloadToken']
		quaisCheckboxes = request.json['quaisCheckboxes']
		callswithPhoto = request.json['callswithPhoto']

		TotalIds = sortCheckboxes(quaisCheckboxes)
		if download.staticFiles(NameDir) == False:
			return jsonify(u'Erro para baixar arquivos estáticos')
		fileRows= queries.SearchingSpecific (TotalIds)
		if fileRows == False:
			return jsonify(u'Erro de conexão com o Banco de Dados')

		fileRows= decode(fileRows)
		fileRows= decodeUTF_Latin(fileRows)
		fileRows= ChangingPhotoPath(fileRows, NameDir)
		fileRows= ChangingAudioPath(fileRows, NameDir)
		fileRows= ChangeTimeDuration(fileRows)
		for index, item in enumerate(fileRows):
			item['dat_hor']= datetime.strftime(item['dat_hor'], '%d/%m/%Y %H:%M:%S')
			fileRows[index]=item

		result= render_template('infoInterface.html', lenght = (index+1), start = 0, end = (index+1), rawQuery= '', query =fileRows, NameDir=NameDir, QueriesPerPage = Config.QueriesPerPage, fotos=callswithPhoto)
		result= ChangingHTML(result, NameDir, (index+1))

		if os.path.exists(Config.ProjectDir+NameDir+'/WebTigerDownloads.html'):
			os.remove(Config.ProjectDir+NameDir+'/WebTigerDownloads.html')
		if download.HTML(result, NameDir) == False:
			return jsonify('Erro ao baixar o HTML')

		return jsonify(fileRows)	
	return jsonify(u'Sessão Expirada')		
			
@app.route("/downloadWord", methods=['POST']) 
def downloadsWord():
	#print '\n'
	#print '*****************************'
	#print '*           WORD            *'
	#print '*****************************'
	NameDir= request.json['NameDir']
	fileRows= request.json['fileRows']
	callswithPhoto = request.json['callswithPhoto']

	if os.path.exists(Config.ProjectDir+NameDir+'/WebTigerDownloads.docx'):	
		os.remove(Config.ProjectDir+NameDir+'/WebTigerDownloads.docx')
	
	if request.json['WORDdownload']:
		if download.WORD(NameDir,fileRows, callswithPhoto) == False:
			return jsonify('Erro ao criar o documento Word')

	return jsonify('ok')

@app.route("/downloadPDF", methods=['POST']) 
def downloadsPDF():
	#print '\n'	
	#print '*****************************'
	#print '*            PDF            *'
	#print '*****************************'
	NameDir= request.json['NameDir']
	fileRows= request.json['fileRows']
	callswithPhoto = request.json['callswithPhoto']

	if os.path.exists(Config.ProjectDir+NameDir+'/WebTigerDownloads.pdf'):	
		os.remove(Config.ProjectDir+NameDir+'/WebTigerDownloads.pdf')	

	if request.json['PDFdownload']: 
		if download.PDF(NameDir,fileRows, callswithPhoto) == False:
			return jsonify('Erro ao criar o documento PDF')

	if download.copyPDFWord(NameDir, fileRows, callswithPhoto)== False:
		return jsonify(u'Erro de cópia ou remoção de arquivo')

	return jsonify('ok')

@app.route("/copyImageAudio", methods=['POST']) 
def copyImageAudio():
	NameDir= request.json['NameDir']
	file= request.json['file']
	download.copyImageAudio(NameDir, file)
	return jsonify('ok')

@app.route("/zip", methods=['GET']) 
def zip():
	NameDir= request.args.get('NameDir')
	downloadToken= request.args.get('downloadToken')

	download.zip(NameDir)
	#print 'COOKIE:',downloadToken
	response = make_response(send_file(Config.ProjectDir+NameDir+'/'+NameDir+'.zip', as_attachment=True))
	response.set_cookie ('downloadToken', downloadToken) #seta o cookie da pagina, para ser comparado no javascript pelo token gerado
	return response
	    
if __name__ == "__main__":

    print "*************************"
    print "* Wytron JSONP Service  *" 
    print "*************************"
    print "Running..."
    
    app.run(host=Config.HostIP, port=Config.Port, threaded=True)
