"""Script for training and plotting the NN model."""

import os

import matplotlib.pyplot as plt
import numpy as np
from viz import create_animation, plot_snapshots

from project import (
    generate_training_data,
    load_config,
    predict_grid,
    train_nn,
)


def main():
    cfg = load_config("config.yaml")
    cfg_5sensor = load_config("config_5sensor.yaml")
    cfg_15sensor = load_config("config_15sensor.yaml")
    cfg_2layers = load_config("config_2layers.yaml")
    cfg_8layers = load_config("config_8layers.yaml")
    cfg_0stoy = load_config("config_0stoy.yaml")
    cfg_1stoy = load_config("config_1stoy.yaml")
    cfg_01learningRate = load_config("config_01learningrate.yaml")
    cfg_16nevroner = load_config("config_16nevroner.yaml")
    cfg_64nevroner = load_config("config_64nevroner.yaml")
    #cfg_10000epoker = load_config("config_10000epoker.yaml")
    #cfg_1000epoker = load_config("config_1000epoker.yaml")

    #######################################################################
    # Oppgave 4.4: Start
    #######################################################################
# Plott hvordan tapene utvikler seg i løpet av treningen, og visualiser prediksjonene
# fra det ferdig trente nettverket

# genererer treningsdata, 
    cfg_values = [cfg, cfg_0stoy, cfg_1stoy, cfg_16nevroner, cfg_64nevroner, cfg_5sensor, 
                  cfg_15sensor, cfg_8layers, cfg_01learningRate, cfg_01learningRate, cfg_2layers]
    cfg_navn = ["Original", "Støy = 0.0", "Støy = 1.0", "Nevroner = 16", "Nevroner = 64", "Sensorer = 5",
                "Sensorer = 15", "Lag = 8", "Learning Rate = 0.1", "Learning Rate = 0.01", "Lag = 2"]
    
    print("Generating training data...")
    fig_total, axtot = plt.subplots(1, 1, figsize=(6,8))
    fig_data, axdata = plt.subplots(1, 1, figsize=(6,8))
    fig_IC, axIC = plt.subplots(1, 1, figsize=(6,8))

    fig_total2, axtot2 = plt.subplots(1, 1, figsize=(6,8))
    fig_data2, axdata2 = plt.subplots(1, 1, figsize=(6,8))
    fig_IC2, axIC2 = plt.subplots(1, 1, figsize=(6,8))

    for i in range(len(cfg_values)-3):

        x, y, t, T_fdm, sensor_data = generate_training_data(cfg_values[i]) 
    
        nn_params, losses_dict = train_nn(sensor_data, cfg_values[i])

        print("Preating prediction grid...")
        T_pred = predict_grid(nn_params, x, y, t, cfg_values[i])
    
 #losses figurer   
        axtot.plot("total", data=losses_dict, label=(cfg_navn[i]))
        axdata.plot("data", data=losses_dict, label=(cfg_navn[i]))
        axIC.plot("ic", data=losses_dict, label=(cfg_navn[i]))
    
    """for i in range(len(cfg_values)-3, len(cfg_values)):

        x, y, t, T_fdm, sensor_data = generate_training_data(cfg_values[i]) 
    
        nn_params, losses_dict = train_nn(sensor_data, cfg_values[i])

        print("Preating prediction grid...")
        T_pred = predict_grid(nn_params, x, y, t, cfg_values[i])
    
 #losses figurer   
        axtot2.plot("total", data=losses_dict, label=(cfg_navn[i]))
        axdata2.plot("data", data=losses_dict, label=(cfg_navn[i]))
        axIC2.plot("ic", data=losses_dict, label=(cfg_navn[i]))"""

    axtot.set_xlabel("Epoker")
    axtot.set_ylabel("Losses (MSE)")
    axtot.set_title("Total losses")
    axtot.set_xlim(0, 2000)
    axtot.legend()
    
    axdata.set_xlabel("Epoker")
    axdata.set_ylabel("Losses (MSE)") 
    axdata.set_title("Data losses")
    axdata.set_xlim(0, 2000)
    axdata.legend()

    axIC.set_xlabel("Epoker")
    axIC.set_ylabel("Losses (MSE)")
    axIC.set_title("Initial condition (IC) losses")
    axIC.set_xlim(0, 2000)
    axIC.legend()

    """axtot2.set_xlabel("Epoker")
    axtot2.set_ylabel("Losses (MSE)")
    axtot2.set_title("Total losses")
    axtot2.set_xlim(0, 5000)
    axtot2.legend()
    
    axdata2.set_xlabel("Epoker")
    axdata2.set_ylabel("Losses (MSE)") 
    axdata2.set_title("Data losses")
    axdata2.set_xlim(0, 5000)
    axdata2.legend()

    axIC2.set_xlabel("Epoker")
    axIC2.set_ylabel("Losses (MSE)")
    axIC2.set_title("Initial condition (IC) losses")
    axIC2.set_xlim(0, 5000)
    axIC2.legend()"""

    fig_total.savefig("output/sammenligning/sammenlining_av_alle_total_plt1_xlim.png")
    fig_data.savefig("output/sammenligning/sammenlining_av_alle_data_plt1_xlim.png")
    fig_IC.savefig("output/sammenligning/sammenlining_av_alle_IC_plt1_xlim.png")
    #fig_total2.savefig("output/sammenligning/sammenlining_av_alle_total_plt2.png")
    #fig_data2.savefig("output/sammenligning/sammenlining_av_alle_data_plt2.png")
    #fig_IC2.savefig("output/sammenligning/sammenlining_av_alle_IC_plt2.png")
    
    plt.show()
    
    #######################################################################
    # Oppgave 4.4: Slutt
    #######################################################################


if __name__ == "__main__":
    main()
