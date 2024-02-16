# LINE
Script básico para utilização das APIs do line

Projeto em construção, só feito o básico ainda, para facilitar algumas consultas e alterações em lote

>Devem ser preenchidos os dados no arquivo .env conforme arquivo de exemplo<br>
>O usuário deve ser um **usuário de serviço do CAU**

## Exemplos de uso
```
line = Line()
line.auth()
```

### Interação com contas:

#### Consulta uma conta (e pega o ID dela)
** para alterações na conta, deve ser setado o ID

```
cd_cliente = 12345
cliente = line.consultaConta(accountCode=cd_cliente)
line.setIdConta(cliente[0]['id'])
```

#### Bloqueia a conta
```
line.alteraConta(isBlocked=False)
```


#### Insere limite por instrumento na conta
```
instrumento = 'WING24'
line.alteraLimitesSpciSpviConta(symbol=instrumento, spci=2,spvi=3)
```


#### Remove o limite por instrumento de um determinado cliente/instrumento
```
instrumento = 'WING24'
line.removeLimiteSpciSpvi(instrumento)
```

#### consulta limite spci/spvi de um cliente
```
limites = line.consultaLimitesSpciSpviConta()
print(limites)
```



### Alterações nos perfis:

#### Criar um perfil novo
```
novo_perfil = 'Clientes Varejo'
resposta = line.criaPerfil(entityType=2,name=novo_perfil)
```

#### Consulta um perfil pelo nome e seta o id do perfil na classe
```
nome_perfil = 'Clientes Varejo'
resposta = line.consultaPerfisEntidade(entityType=2,profileName=nome_perfil)
line.setIdPerfil(resposta[0]['id'])
```

#### Com o id setado, faz alterações nos limites
```
sfd = 5000000
sdp = 100000000
spvd = 100000000
rmkt = 20000000
line.alteraLimitesGlobaisPerfil(sfd=sfd,sdp=sdp,spvd=spvd,rmkt=rmkt)
```

#### Cadastra limite spcispci para um perfil
```
line.alteraLimitesSpciSpviPerfil(symbol='WING24',spci=500,spvi=500)
limites = line.consultaLimitesSpciSpviPerfil()
```

#### Importa limites spci/spvi do perfil, para o excel (usando pandas)
```
line.setIdPerfil(557)
limites = line.consultaLimitesSpciSpviPerfil()
df = pd.DataFrame(limites)
nome_arquivo = 'limites.xlsx'  # Nome do arquivo de saída
df.to_excel(nome_arquivo, index=False)

print(f"Arquivo '{nome_arquivo}' salvo com sucesso!")
```


##### Dependências
python-dotenv<br>
requests