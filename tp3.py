#------- TP : ANEMOMETRIE LASER A EFFET DOPPLER --------

# Packages utilisés
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import re
import os
from scipy.signal import find_peaks
from scipy import stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import math


### PARTIE 1 : Détermination de la vitesse selon le débit ###

# Constantes liées à l'équation de vitesse
lambda0 = 6328*10**-10      
tethasur2 = 0.075                               # en degrés

v_sum = pd.DataFrame()                          # Futur df de vitesse et débit
debit = []                                      # Liste des débits mesurés

for i in range(1000):                           # Appels des X fichiers
    name = 'D{}.csv'.format(i)                  # On définit le format
    if os.path.exists(name): 
        data = pd.read_csv(name, decimal=',',delimiter=';',names=['number'])    
        dt=1/len(data)                          # Temps entre deux points

        voltage=np.array(data['number'])        # Voltage des 200k points
        time=np.arange(len(data))*dt            # Temps des 200k points     
        t0=time[np.argmax(voltage)]             # On défini le temps où volt est au maximum
        indexes = np.array(np.where(np.abs(time-t0)<0.001)).ravel() # Array autour du volt max
        peaks = find_peaks(voltage[indexes],    # Fct pour trouver les maxima
                           height = 5.45,       # Hauteur minimum des pics
                           distance = 12)       # Distance minimum entre les pics
        height = peaks[1]["peak_heights"]       # Hauteur des pics identifiés
        peak_pos = indexes[peaks[0]]*dt         # Position des pics identifiés
        
# Plot des pics associés à la fréquence maximale du signal :   
        sns.set_style('ticks')
        sns.set_context("talk")
        sns.set_style('ticks', {"grid.color":"0.9", 
                                "grid.linestyle":":", 
                                "axes.grid": True})
        fig, ax = plt.subplots(figsize=(10,7))
        ax.plot(time[indexes], voltage[indexes])
        ax.plot(peak_pos, height, "o", markersize = 7, color = 'red')
        ax.set_xlabel('Temps [s]')
        ax.set_ylabel('Voltage [V]')
       # plt.title('Figure de la fréquence du signal de la veine à débit de {}cL/min'.format(i),
                    # y = -0.25, fontsize = 25, fontweight = 'bold')
        plt.show()
    
# Détermination de la vitesse :
        peak_df = pd.DataFrame(peak_pos)
        periode = (peak_df.iloc[-1]-peak_df.iloc[0])/len(peak_df)   # On défini la période
        freq = 1/periode                                            # Puis la fréquence
        vitesse = freq*(6328*10**-10)/(2*math.sin(0.075))           # Enfin la vitesse
        
        v_sum = v_sum.append(vitesse, ignore_index = True)          # On rempli v_sum
        debit.append(i)                                             # On rempli debit
        
v_sum['debit'] = debit                          # On crée le df complet
v_sum.columns = ['vitesse', 'debit']            # On rename les colonnes

# Plot de la régression linéaire du débit en fct de la vitesse


slope, intercept, r_value, p_value, std_err = stats.linregress(v_sum['debit'],v_sum['vitesse'])

fig, ax = plt.subplots(figsize=(10,7))
sns.regplot(v_sum.debit, v_sum.vitesse, 
            line_kws={'color': 'darkred',
                      'label':"y = {0:.6f}x + {1:.5f} \n\nR² = {2:.3f}".format(slope, intercept, r_value)},
            scatter_kws={'lw': 4})
ax.set_xlabel('Débit [cL/min]')
ax.set_ylabel('Vitesse [m/s]')
ax.legend()
#plt.title("Figure de l'évolution de la vitesse du fluide en fonction du débit",
         # y = -0.25, fontsize = 25, fontweight = 'bold')
plt.show()
      

### PARTIE 2 : Détermination du profil de vitesse à  ###

  
v_sum2 = pd.DataFrame()
position = []

for j in range(100):
    # On définit le fichier
    name_2 = 'x{}.csv'.format(j)
    if os.path.exists(name_2): 
        df_2 = pd.read_csv(name_2, decimal=',',delimiter=';',names=['number'])    
        dt_2=1/len(df_2)

        volt=np.array(df_2['number'])
        time2=np.arange(len(df_2))*dt_2
        t0_2=time2[np.argmax(volt)]
        index = np.array(np.where(np.abs(time2-t0_2)<0.001)).ravel()
        peaks2 = find_peaks(volt[index], 
                           height = 5.55, 
                           distance = 19)
        height2 = peaks2[1]["peak_heights"]
        peak_pos2 = index[peaks2[0]]*dt_2
        
        sns.set_style('ticks')
        sns.set_context("talk")
        sns.set_style('ticks', {"grid.color":"0.9", 
                                "grid.linestyle":":", 
                                "axes.grid": True})
        fig, ax = plt.subplots(figsize=(10,7))
        ax.plot(time2[index], volt[index])
        ax.plot(peak_pos2, height2, "o", markersize = 7, color = 'red')
        ax.set_xlabel('Temps [s]')
        ax.set_ylabel('Voltage [V]')
       # plt.title('Figure de la fréquence du signal de la veine à débit de {}cL/min'.format(j),
               #   y = -0.25, fontsize = 25, fontweight = 'bold')
        plt.show()
    
        peak_df2 = pd.DataFrame(peak_pos2)
        periode2 = (peak_df2.iloc[-1]-peak_df2.iloc[0])/len(peak_df2)
        freq2 = 1/periode2
        vitesse2 = freq2*(6328*10**-10)/(2*math.sin(0.075))
        
        v_sum2 = v_sum2.append(vitesse2, ignore_index = True)   
        position.append(j)    

v_sum2['position'] = position               
v_sum2.columns = ['vitesse', 'position']

fig, ax = plt.subplots(figsize=(10,7))
plt.plot(v_sum2.position, v_sum2.vitesse)
ax.set_xlabel('Distance [mm]')
ax.set_ylabel('Vitesse [m/s]')
#plt.title("Figure de la vitesse de l'écoulement selon sa position \n dans la veine à débit constant de ??",
         # y = -0.3, fontsize = 25, fontweight = 'bold')
plt.show()
