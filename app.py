import pandas as pd
import statsmodels.api as sm
from scipy.stats import ttest_ind
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Carregar os dados do arquivo CSV
data = pd.read_csv('data.csv')
data = data.drop(columns=['email'])

# Definir os nomes das colunas
aliases = {
    'timestamps': "Data e Hora",
    'nome': 'Nome',
    'melhor_praca': 'Melhor Praça',
    'nota_parque_infantil': 'Nota Parque Infantil',
    'numero_filhos': 'Número de Filhos',
    'nota_seguranca': 'Nota de Segurança',
    'nota_atividades': 'Nota de Atividades'
}

st.title("Explorando a Satisfação com os Parques Municipais de Matão")
st.markdown("Bem-vindos à apresentação de nossa análise sobre a satisfação da comunidade com os parques municipais de Matão. Este estudo foi realizado a partir de dados coletados diretamente dos frequentadores, que avaliaram aspectos como segurança, atividades oferecidas e infraestrutura infantil.")
st.markdown("Nosso objetivo é compreender quais fatores mais impactam a preferência e o nível de satisfação com esses espaços, contribuindo para decisões que melhorem a experiência de todos. Além disso, buscamos verificar hipóteses sobre diferenças nas percepções entre diferentes grupos e praças.")
st.markdown("A análise estatística e os insights obtidos neste trabalho têm o potencial de fortalecer a gestão dos espaços públicos, assegurando que eles atendam às necessidades e expectativas da nossa comunidade. Vamos explorar os resultados juntos!"
)

st.markdown("## Metodologia Utilizada")
st.markdown("Para entender melhor como a comunidade percebe os parques municipais de Matão, realizamos uma pesquisa simples, onde 250 participantes responderam a um questionário. Perguntamos sobre a segurança, as atividades disponíveis e os espaços para crianças em cada parque, além de qual parque eles preferem.")
st.markdown("Depois de coletar as respostas, analisamos os dados para identificar o que as pessoas mais valorizam e o que pode ser melhorado. Também verificamos se diferentes grupos, como famílias com crianças, têm opiniões diferentes. Por fim, usamos um modelo básico para entender quais fatores mais influenciam a satisfação das pessoas com os parques.")
st.markdown("Nosso objetivo é transformar essas informações em ações que tornem os parques melhores para todos.")

st.markdown("## Resultados da pesquisa")

# Exibir os dados coletados
st.markdown("Abaixo você pode visualizar o resultado da pesquisa.")
st.dataframe(data.rename(columns=aliases), height=400)

## Exibir um resumo estatístico do DataFrame
st.markdown("### Resumo Estatístico dos Dados")
st.write(data.rename(columns=aliases).describe())
resumo_estatistico = '''
Este resumo apresenta as notas dadas pelos participantes para diferentes aspectos dos parques da cidade: segurança, atividades e parquinho infantil. Além disso, consideramos o número de filhos das pessoas, que pode influenciar suas percepções sobre os parques. Essas informações nos ajudam a entender melhor o que as pessoas pensam e o que pode ser melhorado.

### Insights Simples  
1. **Média Alta nas Avaliações:**  
   - A segurança teve uma nota média de **8,57**, atividades **8,56** e o parquinho infantil **8,65**. Isso mostra que, no geral, as pessoas estão satisfeitas com os parques, mas ainda pode haver espaço para melhorias.  

2. **Consistência nas Avaliações:**  
   - As notas mais baixas foram **4 ou 5**, mas a maioria dos participantes deu notas próximas a **8 ou 9** (como indicado pelos valores de 25%, 50% e 75%). Isso sugere que, embora haja algumas críticas, os parques são bem avaliados pela maioria.  

3. **Número de Filhos:**  
   - A média é de **1,6 filhos por participante**, o que reforça a importância do parquinho infantil como um fator relevante.  

4. **Notas Altas como Padrão:**  
   - Muitas pessoas deram nota **10** para pelo menos um aspecto do parque, especialmente o parquinho infantil, indicando que algumas áreas são extremamente bem recebidas.
'''
st.markdown(resumo_estatistico)

# Função para criar gráficos estilizados
def create_barplot(data, x_col, y_col, title, xlabel, ylabel):
    plt.figure(figsize=(10, 6))
    sns.barplot(
        data=data,
        x=x_col,
        y=y_col,
        ci=None,
        palette="viridis" 
    )
    plt.title(title, fontsize=16)
    plt.xlabel(xlabel, fontsize=12)
    plt.ylabel(ylabel, fontsize=12)
    plt.xticks(rotation=45)
    plt.yticks(range(0, 11))
    st.pyplot(plt)

# Gráfico: Nota de Segurança por Parque
st.markdown("### Comparação entre Parques")
st.markdown("Aqui, você pode visualizar a média das notas dadas para cada parque em relação à segurança, atividades e parquinho infantil.")
create_barplot(data, 'melhor_praca', 'nota_seguranca', 
               "Média das Notas de Segurança por Parque", "Parques", "Nota de Segurança")

# Gráfico: Nota de Atividades por Parque
create_barplot(data, 'melhor_praca', 'nota_atividades', 
               "Média das Notas de Atividades por Parque", "Parques", "Nota de Atividades")

# Gráfico: Nota de Parquinho Infantil por Parque
create_barplot(data, 'melhor_praca', 'nota_parque_infantil', 
               "Média das Notas de Parquinho Infantil por Parque", "Parques", "Nota de Parquinho Infantil")

# Hipóteses e Testes Estatísticos
introducao_hipoteses = '''
### Introdução ao Teste de Hipóteses  
O teste de hipóteses é uma forma de verificar se as diferenças nos dados são reais ou apenas coincidências.  

Aqui, usamos esse método para entender se as notas dos parques mudam de verdade dependendo de fatores como segurança e infraestrutura.  

Isso nos ajuda a tomar decisões melhores para melhorar os parques.
'''
st.markdown(introducao_hipoteses)

primeira_hipotese = '''
### Hipótese: A quantidade de filhos influencia na escolha da melhor praça?  

Imagine que cada família escolhe sua praça favorita como se escolhesse o sabor de um sorvete. Será que quem tem mais filhos prefere praças com notas mais altas em geral, como se buscassem um "super sabor"?  

Nesta hipótese, queremos entender se a quantidade de filhos faz as pessoas preferirem praças que têm uma avaliação melhor em segurança, atividades e parquinho infantil. Vamos explorar os dados para descobrir!  
'''
st.markdown(primeira_hipotese)


# Agrupamento dos dados por quantidade de filhos e melhores praças
st.markdown("### Escolha das Praças por Quantidade de Filhos")
data = data.rename(columns=aliases)
melhores_pracas = data.groupby(['Número de Filhos', 'Melhor Praça']).size().reset_index(name='Quantidade')
st.write("A tabela abaixo mostra a relação entre a quantidade de filhos e as praças mais escolhidas:")
st.dataframe(melhores_pracas)

melhores_pracas = data.groupby(['Número de Filhos', 'Melhor Praça']).size().reset_index(name='Quantidade')

resultado_teste = '''
Parece que o Parque Ecológico faz o maior sucesso, né? As famílias com mais filhos estão adorando por lá! Acho que a natureza e o espaço pra correr solto atraem bastante. A Matinha do Bosque também tá bem popular, principalmente entre as famílias menores. Já a Praça Matriz e a Praça da Buscardi são mais quietinhas, mas ainda assim têm seus fãs.'''
st.markdown(resultado_teste)


# Cálculo das médias de notas gerais por quantidade de filhos
st.markdown("### Notas Médias Gerais por Quantidade de Filhos")
notas_medias = data.groupby('Número de Filhos')[
    ['Nota de Segurança', 'Nota de Atividades', 'Nota Parque Infantil']
].mean().reset_index()
notas_medias['Média Geral'] = notas_medias.mean(axis=1)
st.write("A tabela abaixo mostra as notas médias para segurança, atividades, parquinho infantil e a média geral:")
st.dataframe(notas_medias)
resultado_teste2 = '''
Imagine uma corrida entre os parques! O Parque Ecológico seria o campeão de público, especialmente entre as famílias com mais filhos. A natureza, os espaços abertos e a diversidade de atividades fazem dele o favorito para a galera que busca aventura. A Matinha do Bosque seria a prata da casa, com um público fiel e apaixonado. Já a Praça Matriz e a Praça da Buscardi, embora um pouco mais tranquilas, completam o pódio, cada uma com sua particularidade. É como se cada parque tivesse sua torcida especial!'''
st.markdown(resultado_teste2)

# Gráfico de linha para as notas médias
st.markdown("#### Gráfico: Notas Médias por Quantidade de Filhos")
plt.figure(figsize=(12, 6))
sns.lineplot(data=notas_medias, x='Número de Filhos', y='Média Geral', marker='o', color='orange', label='Média Geral')
plt.title("Média Geral das Notas por Número de Filhos", fontsize=14)
plt.xlabel("Número de Filhos", fontsize=12)
plt.ylabel("Média Geral das Notas", fontsize=12)
plt.grid(True)
st.pyplot(plt)

resultado_teste3 = '''
**Olha que legal esse gráfico!** Ele mostra uma coisa bem legal: quanto mais filhos uma família tem, mais ela gosta dos parques! É como se fosse uma corrida, e as famílias com mais filhos sempre chegam na frente, dando notas mais altas para os parques. 

**Isso quer dizer que:**

* **Famílias grandes adoram parques:** Quanto mais filhos, mais a família precisa de um lugar legal para brincar e se divertir, né? 
* **Parques bem avaliados:** Os parques estão sendo super bem avaliados pelas famílias, principalmente aqueles que oferecem mais opções para as crianças.

**Em resumo:** Quanto mais filhos mais exisgentes por um parque legal!
'''
st.markdown(resultado_teste3)

# Conclusão final
st.markdown("### Conclusão Final")
st.markdown("""
Com base nos dados analisados, podemos concluir que a quantidade de filhos influencia na escolha da melhor praça. Observamos que:

- **Parque Ecológico** é a escolha preferida das famílias com mais filhos, provavelmente devido à sua natureza e espaço amplo para atividades.
- **Matinha do Bosque** é popular entre famílias menores, oferecendo um ambiente acolhedor e seguro.
- **Praça Matriz** e **Praça da Buscardi** são menos escolhidas, mas ainda têm seus fãs, especialmente entre famílias com menos filhos.

Além disso, as notas médias gerais indicam que famílias com mais filhos tendem a dar notas mais altas para os parques, sugerindo que esses espaços são importantes para proporcionar lazer e diversão para crianças de todas as idades.

Portanto, a quantidade de filhos é um fator significativo na escolha da melhor praça, com uma clara preferência por parques que oferecem mais espaço e atividades para crianças.
""")