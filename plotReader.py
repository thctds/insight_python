import matplotlib.pyplot as plt
import pandas as pd

plt.style.use('fivethirtyeight')

x = []
y = []
  
data = pd.read_csv('data.csv')
x = data['itr']
y1 = data['af3a']
y2 = data['af3hb']
y3 = data['af3t']
y4 = data['af4a']
y5 = data['af4hb']
y6 = data['af4t']
  
plt.tight_layout()
plt.plot(x, y1, label='AF3Alpha')
plt.plot(x, y2, label='AF3Hbeta')
plt.plot(x, y3, label='AF3Theta')
plt.plot(x, y4, label='Af4Alpha')
plt.plot(x, y5, label='Af4HBeta')
plt.plot(x, y6, label='Af4Theta')
plt.legend(loc='upper left')
plt.plot()
plt.show()