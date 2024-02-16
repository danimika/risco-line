import os as os
import requests
import time
from typing import List, Optional, Dict, Union
from dotenv import dotenv_values


class Line():
    def __init__(self):
        self.broker_code = None
        self.category_code = None
        self.url = 'https://api.line.bvmfnet.com.br/api/v1.0/'
        self.url_token = 'https://api.line.bvmfnet.com.br/api/oauth/token'
        self.token = None
        self.accId = None
        self.prflId = None
        self.id_documento = None
        self.conta = None

    def auth(self) -> None:
        config = dotenv_values(".env")
        username = config['LINE_USER']
        password = config['LINE_PW']
        self.broker_code = config['LINE_BROKER']
        self.category_code = config['LINE_CATEGORY']
        r = requests.get(self.url + 'token/authorization')
        authheader = r.json()['header']

        header = {'Authorization' : "Basic "+authheader,
                'content-type': 'application/x-www-form-urlencoded'
                }
        
        params = {'grant_type': 'password',
                'username': username, 
                'password' : password, 
                'brokerCode': self.broker_code,
                'categoryCode': self.category_code
                }
        
        t = requests.post(self.url_token,headers=header,data=params)
        
        if t.status_code == 200:
            token = t.json()
            self.token = token['access_token']
            return self.token
        else:
            print(f'Erro na solicitação: {t.status_code} - {t.text}')

    def consulta(self, endpoint: str, parametros)-> List[Union[int, str]]:
        time.sleep(0.1)
        url = self.url + endpoint
        headers = { 'Authorization': 'Bearer '+ self.token }
        response = requests.get(url, params=parametros, headers=headers)

        if response.status_code == 200:
            return response.json()
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}')
            return None

    def altera(self, endpoint: str, parametros) -> Union[requests.Response, None]:
        time.sleep(0.1)
        url = self.url + endpoint
        headers = { 'Authorization': 'Bearer '+ self.token, 'Content-Type': 'application/json' }
        response = requests.post(url, json=parametros, headers=headers)
        return response

    def consultaParticipante(self, code: Optional[int] = None, categories: Optional[List] = None):
        endpoint = 'participant/'
        params = { 'code': code , 'categories': categories}        
        return self.consulta(endpoint=endpoint, parametros=params)


    def setIdConta(self, accId: int) -> None:
        self.accId = accId

    def setIdDocumento(self, id_documento: int) -> None:
        self.id_documento = id_documento

    def setIdPerfil(self, prflId: int) -> None:
        self.prflId = prflId

    def consultaConta(self, pageSize: Optional[int] = None,
                angularItensPerPage: Optional[int] = None,
                pageNumber: Optional[int] = None,
                sortBy: Optional[str] = None,
                id: Optional[int] = None,
                participantCode: Optional[int] = None,
                pnpCode: Optional[int] = None,
                carryingCode: Optional[int] = None,
                isCarrying: Optional[bool] = None,
                participantCategory: Optional[str] = None,
                pnpCategory: Optional[str] = None,
                accountCode: Optional[int] = None,
                accountName: Optional[str] = None,
                accountActiveType: Optional[str] = None,
                accountProtected: Optional[bool] = None,
                accountBlocked: Optional[bool] = None,
                accountTypeLineDomain: Optional[str] = None,
                documentId: Optional[int] = None,
                documentCode: Optional[str] = None,
                ownerDocumentCode: Optional[str] = None,
                ownerName: Optional[str] = None):

        if documentCode is not None:
            documentCode = str(documentCode).zfill(14)

        params = {
                    'pageSize': pageSize,
                    'angularItensPerPage': angularItensPerPage,
                    'pageNumber': pageNumber,
                    'sortBy': sortBy,
                    'id': id,
                    'participantCode': participantCode,
                    'pnpCode': pnpCode,
                    'carryingCode': carryingCode,
                    'isCarrying': isCarrying,
                    'participantCategory': participantCategory,
                    'pnpCategory': pnpCategory,
                    'accountCode': accountCode,
                    'accountName': accountName,
                    'accountActiveType': accountActiveType,
                    'accountProtected': accountProtected,
                    'accountBlocked': accountBlocked,
                    'accountTypeLineDomain': accountTypeLineDomain,
                    'documentId': documentId,
                    'documentCode': documentCode,
                    'ownerDocumentCode': ownerDocumentCode,
                    'ownerName': ownerName,
                }
        self.conta = self.consulta(endpoint='account', parametros=params)
        return self.conta

    def consultaLimitesGlobaisConta(self):
        params = { 'accId': self.accId } 
        endpoint = 'account/' + str(self.accId) + '/lmt'

        return self.consulta(endpoint=endpoint, parametros=params)

    def consultaLimitesMercadosConta(self):
        params = { 'accId': self.accId } 
        endpoint = 'account/' + str(self.accId) + '/lmt/mkta'

        return self.consulta(endpoint=endpoint, parametros=params)
        
    def consultaLimitesSpciSpviConta(self):
        params = { 'accId': self.accId } 
        endpoint = 'account/' + str(self.accId) + '/lmt/spxi'

        return self.consulta(endpoint=endpoint, parametros=params)




    def alteraConta(self,
                isBlocked: Optional[bool] = None,
                isProtected: Optional[bool] = None,
                profileId: Optional[int] = None):
        
        if isBlocked is None and isProtected is None and profileId is None:
            raise ValueError("Pelo menos um dos parâmetros opcionais deve ser fornecido.")

        data: Dict[str, Union[bool, int]] = {}
        if isBlocked is not None:
            data['isBlocked'] = isBlocked
        if isProtected is not None:
            data['isProtected'] = isProtected
        if profileId is not None:
            data['profileId'] = profileId


        endpoint = 'account/' + str(self.accId)
        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Conta id: {self.accId} atualizada com sucesso.')
        elif response.status_code == 201:
            print("Conta criada com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}') 

    def alteraLimitesGlobaisConta(self,
                sfd: Optional[int] = None,
                sdp: Optional[int] = None,
                spvd: Optional[int] = None,
                rmkt: Optional[int] = None,
                irmkt: Optional[int] = None):
        
        if sfd is None and sdp is None and spvd is None and rmkt is None and irmkt is None:
            raise ValueError("Pelo menos um dos parâmetros opcionais deve ser fornecido.")

        data: Dict[str, Union[bool, int]] = {}
        if sfd is not None:
            data['sfd'] = sfd
        if sdp is not None:
            data['sdp'] = sdp
        if spvd is not None:
            data['spvd'] = spvd
        if rmkt is not None:
            data['rmkt'] = rmkt
        if irmkt is not None:
            data['irmkt'] = irmkt
    
        endpoint = 'account/' + str(self.accId) + '/lmt'

        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Conta id: {self.accId} atualizada com sucesso.')
        elif response.status_code == 201:
            print("Conta criada com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}') 

    def alteraLimitesMercadosConta(self,
                groupId: int,
                authorized: Optional[str] = None,
                spci: Optional[int] = None,
                spvi: Optional[int] = None,
                tmoc: Optional[int] = None,
                tmov: Optional[int] = None):
        
        if authorized is None and spci is None and spvi is None and tmoc is None and tmov is None:
            raise ValueError("Pelo menos um dos parâmetros opcionais deve ser fornecido.")

        data: Dict[str, Union[bool, int]] = {}
        data['groupId'] = groupId
        if authorized is not None:
            if authorized == 'N':
                data['authorized'] = 0
            elif authorized == 'C':
                data['authorized'] = 1
            elif authorized == 'V':
                data['authorized'] = 2
            elif authorized == 'CV':
                data['authorized'] = 3
            elif authorized == '-':
                data['authorized'] = None
        if spci is not None:
            data['spci'] = spci
        if tmoc is not None:
            data['tmoc'] = tmoc
        if tmov is not None:
            data['tmov'] = tmov
    
        endpoint = 'account/' + str(self.accId) + '/lmt/mkta'

        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Conta id: {self.accId} atualizada com sucesso.')
        elif response.status_code == 201:
            print("Conta criada com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}') 

    def alteraLimitesSpciSpviConta(self,  
                symbol: Optional[str] = None,
                spci: Optional[int] = None,
                spvi: Optional[int] = None):
        
        endpoint = 'account/' + str(self.accId) + '/lmt/spxi'

        data =[{"symbol": symbol,
            "spci": spci,
            "spvi": spvi
        }]

        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Conta id: {self.accId} atualizada com sucesso.')
        elif response.status_code == 201:
            print("Conta criada com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}') 

    def removeLimiteSpciSpviConta(self, symbol: str):
        endpoint = 'account/' + str(self.accId) + '/lmt/spxi'

        data =[{"symbol": symbol,
            "isRemoved": True
        }]

        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Conta id: {self.accId} atualizada com sucesso.')
        elif response.status_code == 201:
            print("Conta criada com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}')  





    def consultaPerfisEntidade(self, 
                entityType: int, 
                pnpCode: Optional[int] = None,
                profileType: Optional[str] = None,
                participantCode: Optional[int] = None,
                profileName: Optional[str] = None):
        
        endpoint = 'riskProfile'
        
        data: Dict[str, Union[bool, int]] = {}

        data['entityType'] = entityType
        if pnpCode is not None:
            data['pnpCode'] = pnpCode
        if profileType is not None:
            data['profileType'] = profileType
        if participantCode is not None:
            data['participantCode'] = participantCode
        if profileName is not None:
            data['profileName'] = profileName

        return self.consulta(endpoint=endpoint, parametros=data)



    def consultaLimitesGlobaisPerfil(self):
        params = { 'prflId': self.prflId } 
        endpoint = 'riskProfile/' + str(self.prflId) + '/lmt'

        return self.consulta(endpoint=endpoint, parametros=params)     
    
    def consultaLimitesMercadosPerfil(self):
        params = { 'prflId': self.prflId } 
        endpoint = 'riskProfile/' + str(self.prflId) + '/lmt/mkta'

        return self.consulta(endpoint=endpoint, parametros=params)    
    
    def consultaLimitesSpciSpviPerfil(self):
        params = { 'prflId': self.prflId } 
        endpoint = 'riskProfile/' + str(self.prflId) + '/lmt/spxi'

        return self.consulta(endpoint=endpoint, parametros=params)   




    def profileDomainRequest(entityType: Optional[int] = None
                             ):
        return  [{
                    "entityType": 0,
                    "name": "",
                    "participant": {
                        "category": 0,
                        "code": 0,
                        "name": "",
                        "segment": 0
                    },
                    "pnp": {
                        "category": 0,
                        "code": 0,
                        "name": "",
                        "segment": 0
                    },
                    "type": 0
                }]


    def criaPerfil(self,
                entityType: int,
                name: str,):

        data = {
                    'entityType': entityType, # 2-Conta 3-Documento 4-Profissional
                    'name': name,
                    'type': 1, #Completo
                    'participant': {'code':self.broker_code } ,
                    'pnp': {'code':self.broker_code }
                }

   
        endpoint = 'riskProfile/'

        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Perfil id: {self.prflId} atualizada com sucesso.')
        elif response.status_code == 201:
            print("Perfil criado com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}')


    def alteraLimitesGlobaisPerfil(self,
                sfd: Optional[int] = None,
                sdp: Optional[int] = None,
                spvd: Optional[int] = None,
                rmkt: Optional[int] = None,
                irmkt: Optional[int] = None):
        
        if sfd is None and sdp is None and spvd is None and rmkt is None and irmkt is None:
            raise ValueError("Pelo menos um dos parâmetros opcionais deve ser fornecido.")

        data: Dict[str, Union[bool, int]] = {}
        if sfd is not None:
            data['sfd'] = sfd
        if sdp is not None:
            data['sdp'] = sdp
        if spvd is not None:
            data['spvd'] = spvd
        if rmkt is not None:
            data['rmkt'] = rmkt
        if irmkt is not None:
            data['irmkt'] = irmkt
    
        endpoint = 'riskProfile/' + str(self.prflId) + '/lmt'


        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Perfil id: {self.prflId} atualizada com sucesso.')
        elif response.status_code == 201:
            print("Perfil criado com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}') 

    def alteraLimitesMercadosPerfil(self,
                groupId: int,
                authorized: Optional[str] = None,
                spci: Optional[int] = None,
                spvi: Optional[int] = None,
                tmoc: Optional[int] = None,
                tmov: Optional[int] = None):
        
        if authorized is None and spci is None and spvi is None and tmoc is None and tmov is None:
            raise ValueError("Pelo menos um dos parâmetros opcionais deve ser fornecido.")
        data_list = []
        data: Dict[str, Union[bool, int]] = {}
        data['groupId'] = groupId

        if authorized is not None:
            if authorized == 'N':
                data['authorized'] = 0
            elif authorized == 'C':
                data['authorized'] = 1
            elif authorized == 'V':
                data['authorized'] = 2
            elif authorized == 'CV':
                data['authorized'] = 3
            elif authorized == '-':
                data['authorized'] = None
        if spci is not None:
            data['spci'] = spci
        if spvi is not None:
            data['spvi'] = spvi
        if tmoc is not None:
            data['tmoc'] = tmoc
        if tmov is not None:
            data['tmov'] = tmov
    
        endpoint = 'riskProfile/' + str(self.prflId) + '/lmt/mkta'
        data_list.append(data)
        print(endpoint)
        print(data_list)


        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Perfil id: {self.prflId} atualizado com sucesso.')
        elif response.status_code == 201:
            print("Perfil criado com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}') 

    def alteraLimitesSpciSpviPerfil(self,       
                symbol: Optional[str] = None,
                spci: Optional[int] = None,
                spvi: Optional[int] = None):
        
        endpoint = 'riskProfile/' + str(self.prflId) + '/lmt/spxi'

        data =[{"symbol": symbol,
            "spci": spci,
            "spvi": spvi
        }]

        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Perfil id: {self.prflId} atualizado com sucesso.')
        elif response.status_code == 201:
            print("Perfil criado com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}') 

    def removeLimiteSpciSpviPerfil(self, symbol: str):
        endpoint = 'riskProfile/' + str(self.prflId) + '/lmt/spxi'

        data =[{"symbol": symbol,
            "isRemoved": True
        }]

        response = self.altera(endpoint=endpoint, parametros=data)
        
        if response.status_code == 200:
            print(f'Perfil id: {self.prflId} atualizado com sucesso.')
        elif response.status_code == 201:
            print("Perfil criado com sucesso.")
        else:
            print(f'Erro na solicitação: {response.status_code} - {response.text}') 




    def consultaDocumento(self, documento: int):
        endpoint = 'document'
        documento = str(documento).zfill(14)

        params = { 'documentCode': documento }

        return self.consulta(endpoint=endpoint, parametros=params)





    
    def profileTypes(self):
        params = { 'type': None } 
        endpoint = 'profileType'
        return self.consulta(endpoint=endpoint, parametros=params) 

    def profileEntityType(self):
        params = { 'type': None } 
        endpoint = 'profileEntityType'
        return self.consulta(endpoint=endpoint, parametros=params)
    
    def symbolGroup(self):
        params = { 'type': None } 
        endpoint = 'symbolGroup'
        return self.consulta(endpoint=endpoint, parametros=params) 

    def lineEntityType(self):
        params = { 'type': None } 
        endpoint = 'lineEntityType'
        return self.consulta(endpoint=endpoint, parametros=params)
    
    def symbol(self):
        params = { 'type': None } 
        endpoint = 'symbol'
        return self.consulta(endpoint=endpoint, parametros=params) 

    def consultaInstrumento(self, searchByKey: str):
        endpoint = 'symbol/' + searchByKey
        params = { 'searchByKey': searchByKey }        
        return self.consulta(endpoint=endpoint, parametros=params)



