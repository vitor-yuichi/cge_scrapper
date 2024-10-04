def extract_floods_cge(inicio, final):
    from selenium import webdriver
    from selenium.webdriver.common.keys import Keys
    from selenium.webdriver.common.by import By
    import time 
    import pandas as pd 
    from datetime import datetime, timedelta
    
    def gerar_lista_datas(inicio, fim):
        # Converter as datas de início e fim para objetos datetime
        data_inicio = datetime.strptime(inicio, '%d/%m/%Y')
        data_fim = datetime.strptime(fim, '%d/%m/%Y')
        
        # Lista para armazenar as datas em formato de string
        lista_datas = []
        
        # Loop para gerar as datas entre a data de início e a data de fim
        while data_inicio <= data_fim:
            # Adicionar a data formatada à lista de datas
            lista_datas.append(data_inicio.strftime('%d/%m/%Y'))
            
            # Incrementar a data de início para o próximo dia
            data_inicio += timedelta(days=1)
    
    datas = gerar_lista_datas(inicio, final)


    dataframes= []
    driver = webdriver.Chrome()
    driver.get('https://www.cgesp.org/v3/alagamentos.jsp')
    time.sleep(0.5)
    for data in datas:
        info_esquerda = []
        info_direita = []
        info_data = []
        bairros = []
        campo_busca = driver.find_element(By.NAME, 'dataBusca')
        campo_busca.send_keys(Keys.CONTROL, 'a')
        campo_busca.send_keys(Keys.BACKSPACE)
        campo_busca.send_keys(data)
        campo_busca.send_keys(Keys.RETURN)
        time.sleep(0.5)

        zonas_alagamentos = driver.find_elements(By.CLASS_NAME, 'tb-pontos-de-alagamentos')
        if len(zonas_alagamentos)>0:
            for alagamentos in zonas_alagamentos:
                info_1 = alagamentos.find_elements(By.CLASS_NAME, 'arial-descr-alag.col-local')
                info_2 = alagamentos.find_elements(By.CLASS_NAME, 'arial-descr-alag')
                bairro = alagamentos.find_elements(By.CLASS_NAME, 'bairro.arial-bairros-alag.linha-pontilhada')
                for info1 in info_1:
                    info_esquerda.append(info1.text)
                    bairros.append(bairro[0].text)
                    info_data.append(data)
                for info2 in info_2:
                    info_direita.append(info2.text)
                time.sleep(0.5)

            df = pd.DataFrame({
                'data_ocorrencia': info_data,
                'Bairro': bairros,
                'Local': info_esquerda,
                'Ref': [item for item in info_direita if "Sentido:" in item]
            })
            df[['Horário', 'Local']] = df['Local'].str.split('\n', expand = True)
            df[["Sentido", "Referencia"]] = df['Ref'].str.split('\n', expand = True)
            df.drop(columns = ['Ref'], inplace = True)
            df.Sentido = df.Sentido.str.replace('Sentido:', '')
            df.Referencia = df.Referencia.str.replace('Referência:', '')
            
            dataframes.append(df)
            print(f'Alagamentos do dia {data} coletados. Total de {len(df)} alagamentos')
        else:
            print(f'Não já registros de alagamento para a data {data}')

    if len(dataframes)!=0:
        return pd.concat(dataframes)
    else:
        return 'Não há alagamentos na série temporal'
    
if __name__ == '__main__':
    extract_floods_cge(inicio, final)