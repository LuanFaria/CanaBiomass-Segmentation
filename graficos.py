import geopandas as gpd
import matplotlib.pyplot as plt
import os
import pandas as pd 


def pizza(ax):
    # Caminho da pasta que contém os arquivos shapefiles
    caminho_pasta = 'C:/CLASSIFICACAO/'
    # Obtendo a lista de arquivos shapefile (.shp) na pasta especificada
    arquivos_shapefiles = [f for f in os.listdir(caminho_pasta) if f.endswith('.shp')]

    # Verifica se existem arquivos shapefiles na pasta
    if not arquivos_shapefiles:
        print("Nenhum arquivo shapefile (.shp) foi encontrado na pasta especificada.")
    else:
        # Iterando sobre cada shapefile encontrado
        for arquivo in arquivos_shapefiles:
            caminho_shapefile = os.path.join(caminho_pasta, arquivo)

            # Obtendo o nome do arquivo sem extensão para usar como título do gráfico
            nome_arquivo = os.path.splitext(arquivo)[0]

            # Leitura do shapefile usando o GeoPandas
            shapefile = gpd.read_file(caminho_shapefile)

            # Verificação se as colunas 'GRIDCODE' e 'AREA_NDVI' existem
            if 'GRIDCODE' in shapefile.columns and 'AREA_NDVI' in shapefile.columns:
                # Calculando a soma de AREA_NDVI por classe de GRIDCODE
                area_ndvi_soma = shapefile.groupby('GRIDCODE')['AREA_NDVI'].sum()

                # Calculando a proporção (porcentagem) de cada classe
                proporcoes = (area_ndvi_soma / area_ndvi_soma.sum()) * 100

                # Mapeamento de cores personalizadas para as classes
                cores = {
                    1: '#d7191c',          # Solo exposto
                    2: '#f59053',       # Biomassa baixa
                    3: '#feef99',       # Biomassa média baixa
                    4: '#a2c238',      # Verde marca-texto - Biomassa média alta
                    5: '#2e5316'      # Biomassa alta
                }

                # Criando uma lista de cores com base nos índices das classes
                lista_cores = [cores.get(classe, 'gray') for classe in proporcoes.index]

                # Criar a legenda correspondente
                legend_labels = [
                    "Solo Exposto",
                    "Baixa",
                    "Média Baixa",
                    "Média Alta",
                    "Alta"
                ]

                # Mantendo a ordem correta para a legenda
                legend_colors = [cores[i] for i in sorted(cores.keys())]

                # Plotagem do gráfico de pizza em 2D com base nas proporções de AREA_NDVI
                # Usando o eixo fornecido
                wedges, texts, autotexts = ax.pie(
                    proporcoes, 
                    #labels=proporcoes.index, 
                    colors=lista_cores, 
                    autopct='%1.1f%%', 
                    startangle=90
                )

                # Adiciona contorno preto às fatias
                for wedge in wedges:
                    wedge.set_edgecolor('black')  # Define a cor do contorno

                # Adiciona título ao gráfico
                ax.set_title(f'BIOMASSA - {nome_arquivo}')
                ax.axis('equal')  # Para garantir que o gráfico fique como um círculo

                # Adiciona legenda abaixo do gráfico
                handles = [plt.Line2D([0], [0], color=color, lw=4) for color in legend_colors]
                ax.legend(handles, legend_labels, title="BIOMASSA", bbox_to_anchor=(0.15, 0.25), ncol=1)

                # Criando a tabela com os valores de AREA_NDVI somados
                area_ndvi_tabela = area_ndvi_soma.reset_index(drop=True).to_frame()
                area_ndvi_tabela.columns = ['ÁREA']
                area_ndvi_tabela = area_ndvi_tabela.round(2)

                # Adicionando uma coluna de cores à tabela
                area_ndvi_tabela['Cor'] = lista_cores

                # Reordenando as colunas para que a cor apareça antes do valor de NDVI
                area_ndvi_tabela = area_ndvi_tabela[['Cor', 'ÁREA']]

                # Calculando o valor total de AREA_NDVI
                total_ndvi = area_ndvi_tabela['ÁREA'].sum()

                # Adicionando uma linha ao final com o valor total
                total_linha = pd.DataFrame([['Total', total_ndvi]], columns=['Cor', 'ÁREA'])
                area_ndvi_tabela = pd.concat([area_ndvi_tabela, total_linha])



                # Adiciona tabela ao gráfico (ajuste a posição conforme necessário)
                tabela = ax.table(cellText=area_ndvi_tabela.values,
                         colLabels=['Biomassa', 'ÁREA (ha)'],
                         cellLoc='right', 
                         loc='right', 
                         #bbox=[1.05, 0.1, 0.3, 0.6])  # Ajuste da posição da tabela
                         bbox=[0.845, -0.12, 0.28, 0.6])  # Ajuste da posição da tabela
            
                # Colorindo as células da tabela e a letra da coluna "Biomassa" - GAMBIARRA COM CORES 
                for i in range(len(area_ndvi_tabela) - 1):  # Excluindo a última linha que é "Total"
                        tabela[(i + 1, 0)].set_facecolor(area_ndvi_tabela['Cor'].iloc[i])  # Colorindo a coluna de cores
                        tabela[(i + 1, 0)].set_text_props(color=area_ndvi_tabela['Cor'].iloc[i])  # Definindo a cor do texto igual ao fundo
                tabela[(len(area_ndvi_tabela), 0)].set_facecolor('lightgrey')  # Cor do fundo da linha total
                tabela[(len(area_ndvi_tabela), 0)].set_text_props(color='black')  # Cor do texto da linha total
                tabela[(len(area_ndvi_tabela), 1)].set_facecolor('lightgrey')  # Cor do fundo da coluna de valores
                tabela[(len(area_ndvi_tabela), 1)].set_text_props(color='black')  # Cor do texto da coluna de valores

                
                plt.tight_layout()
                
                
            else:
                print(f"As colunas 'GRIDCODE' e/ou 'AREA_NDVI' não foram encontradas no shapefile: {arquivo}")
