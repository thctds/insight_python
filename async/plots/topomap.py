from asyncio.windows_events import NULL
from eeg_positions import get_elec_coords, plot_coords
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import CloughTocher2DInterpolator

#plot do escalpo e dos eletrodos em suas posições

RADIUS_INNER_CONTOUR = 0.72658518
RADIUS_OUTER_CONTOUR = 1.0

coords = get_elec_coords(
    elec_names=["AF3", "AF4", "T7", "T8", "Pz"],
    drop_landmarks=False,
    dim="2d",
)

fig, ax = plot_coords(
    coords, scatter_kwargs=dict(color="black"), text_kwargs=dict(fontsize=10)
)
#END plot do escalpo e dos eletrodos em suas posições



posX = [0, 0, 0, 0, 0]
posY = [0, 0, 0, 0, 0]

for idx, row in coords.iterrows():
    posX[idx] = row["x"]#array que guarda a coordenada x dos eletrodos
    posY[idx] = row["y"]#array que guara a coordenada y dos eletrodos

pointDensity = 500 #quantidade de pontos do linspace tanto no eixo x quanto no y
lastEpochDatapack = 1200 #Último datapack considerado no epoch
firstEpochDatapack = 1 #Primeiro datapack considerado no epoch

#############################
# Eu ainda não sei mexer muito bem no pandas, então só consegui pegar a média da sessão inteira, 
# mas a ideia é pegar pequenas partes para analisar a resposta do cérebro aos estímulos proporcionados
# pelo filme/trailer.
#############################

# Separei os dados do CSV de acordo com a faixa de frequência que eles representam, de forma com que é fácil trocar entre as faixas analisadas, bastando 
# descomentar o 'z' referente à faixa desejada ao passo que comenta o 'z' da faixa que estava sendo analisada.
data = pd.read_csv('../../data.csv')
zAlpha = [data['itr'][lastEpochDatapack - firstEpochDatapack]/8, data['af3a'].mean(), data['af4a'].mean(), data['pxa'].mean(), data['t8a'].mean(), data['pza'].mean()]
zLowBeta = [data['itr'][lastEpochDatapack - firstEpochDatapack]/8, data['af3lb'].mean(), data['af4lb'].mean(), data['pxlb'].mean(), data['t8lb'].mean(), data['pzlb'].mean()]
zHighBeta = [data['itr'][lastEpochDatapack - firstEpochDatapack]/8, data['af3hb'].mean(), data['af4hb'].mean(), data['pxhb'].mean(), data['t8hb'].mean(), data['pzhb'].mean()]
zGamma = [data['itr'][lastEpochDatapack - firstEpochDatapack]/8, data['af3g'].mean(), data['af4g'].mean(), data['pxg'].mean(), data['t8g'].mean(), data['pzg'].mean()]
zTheta = [data['itr'][lastEpochDatapack - firstEpochDatapack]/8, data['af3t'].mean(), data['af4t'].mean(), data['pxt'].mean(), data['t8t'].mean(), data['pzt'].mean()]

z = [zAlpha[1], zAlpha[2], zAlpha[3], zAlpha[4], zAlpha[5]]
#z = [zLowBeta[1], zLowBeta[2], zLowBeta[3], zLowBeta[4], zLowBeta[5]]
#z = [zHighBeta[1], zHighBeta[2], zHighBeta[3], zHighBeta[4], zHighBeta[5]]
#z = [zGamma[1], zGamma[2], zGamma[3], zGamma[4], zGamma[5]]
#z = [zTheta[1], zTheta[2], zTheta[3], zTheta[4], zTheta[5]]

# linspaces com as coordenadas dos pontos que preencherão o gráfico
xi = np.linspace(-1, 1, pointDensity)
yi = np.linspace(-1, 1, pointDensity)


# Para que a figura do escalpo seja completamente preenchida pelo heatmap,
# é necessário adicionar alguns outros pontos, em especial nas bordas da
# figura. Desta forma, foram adicionados 36 pontos igualmente espaçados 
# nas bordas do círculo do topomap.
newX = np.array(np.zeros((36, 1), float))
newY = np.array(np.zeros((36, 1), float))
newZ = np.array(np.zeros((36, 1), float))
distance = np.array(np.zeros((5, 1), float))
aux1 = 0
aux2 = 1

# Para calular o valor da potência nestes pontos adicionados, foi feita uma lógica de 
# interpolação baseada na distância entre os pontos adicionados e os eletrodos, sendo
# selecionados para a interpolação os dois eletrodos mais próximos.
for i in range(36):
    angle = (np.pi/18)*i
    newX[i] = np.cos(angle)
    newY[i] = np.sin(angle)
    distance[0]= np.sqrt((posX[0] - newX[i])**2 + (posY[0] - newY[i])**2)
    distance[1]= np.sqrt((posX[1] - newX[i])**2 + (posY[1] - newY[i])**2)
    distance[2] = np.sqrt((posX[2] - newX[i])**2 + (posY[2] - newY[i])**2)
    distance[3] = np.sqrt((posX[3] - newX[i])**2 + (posY[3] - newY[i])**2)
    distance[4] = np.sqrt((posX[4] - newX[i])**2 + (posY[4] - newY[i])**2)
    
    minDistance = distance[0]
    minDistance2 = distance[1]
    for j in range(3):
        if distance[j+2] < minDistance:
            minDistance, minDistance2 = distance[j+2], minDistance
            aux1, aux2 = j+2, aux1
        elif distance[j+2] < minDistance2:
            minDistance2 = distance[j+2]
            aux2 = j+2

    newZ[i] = ((1 - (distance[aux1] / 2)) * z[aux1])*0.75 + (((1 - (distance[aux2] / 2)) * z[aux2])*0.25)#lógica de interpolação

# FIM da adição de pontos para interpolação

#adição dos novos pontos gerados e interpolados nas estruturas que armazenam os dados que serão interpolados no topomap
posX  = np.append(posX, newX)
posY = np.append(posY, newY)
z = np.append(z, newZ)

X, Y = np.meshgrid(xi,yi) # "suaviza" as curvas no heatmap
interp = CloughTocher2DInterpolator(list(zip(posX, posY)), z) #interpolador
Z = interp(X, Y)

#lógica de plotagem
plt.pcolormesh(X, Y, Z, cmap = 'jet' , shading='auto')
plt.legend()
cbar = plt.colorbar()
cbar.set_label('uV²/Hz', rotation=90)

plt.axis("equal")
ax.axis("off")
plt.show()