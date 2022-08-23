# -*- coding: utf-8 -*-

from gluon import DAL,Field
import Config
import hashlib

def get_hash_password(password):
	try:
		return hashlib.md5(password).hexdigest()
	except:
		pass
	return ''		

def check_user(username,password):	
	try:
		db=DAL(Config.DBInfoOperacaoWeb,pool_size=Config.DBPoolSize)
		db.define_table('user',Field('lgn'),Field('snh'), Field('permi'), rname='dbo.usr', migrate = False)	
		userinfo=db(db.user.lgn==username).select(db.user.snh, db.user.permi)
		db.close()
		
		if len(userinfo)>0:
			hash_pw=get_hash_password(password)

			if hash_pw == userinfo[0]['snh']:
				if (userinfo[0]['permi'])[6]=='1':
					ret ={}
					ret['user']= username
					ret['hash']= hash_pw
					return ret
		return True
	except:
		return False

def Re_check_user(login, hashSenha):
	try:
		db=DAL(Config.DBInfoOperacaoWeb,pool_size=Config.DBPoolSize)
		db.define_table('user',Field('lgn'),Field('snh'), Field('permi'), rname='dbo.usr', migrate = False)
		userinfo=db(db.user.lgn==login).select(db.user.snh, db.user.permi)
		db.close()
		if userinfo[0]['snh'] == hashSenha:
			if (userinfo[0]['permi'])[6]=='1':
				return True
		return False
	except:
		return False

def run(username,password):  
	print '[username]= ',username
	print '[password]= ',password
	
	if len(username)==0 or len(password)==0:
		return False
	
	return check_user(username,password)
