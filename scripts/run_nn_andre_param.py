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


    #######################################################################
    # Oppgave 4.4: Start
    #######################################################################
# Plott hvordan tapene utvikler seg i løpet av treningen, og visualiser prediksjonene
# fra det ferdig trente nettverket

# genererer treningsdata, 
    cfg_values = [cfg, cfg_0stoy, cfg_1stoy, cfg_01learningRate, cfg_16nevroner, 
                  cfg_64nevroner, cfg_5sensor, cfg_15sensor, cfg_2layers, cfg_8layers]
    
    print("Generating training data...")
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6,8))
    plt.subplots_adjust(hspace=0.4)

    for cfg in cfg_values:

        x, y, t, T_fdm, sensor_data = generate_training_data(cfg) 
    
        nn_params, losses_dict = train_nn(sensor_data, cfg)

        print("Preating prediction grid...")
        T_pred = predict_grid(nn_params, x, y, t, cfg)

    
 #losses figurer   
        ax1.plot("total", data=losses_dict, label=str(cfg))
        ax2.plot("data", data=losses_dict, label=str(cfg))
        ax3.plot("ic", data=losses_dict, label=str(cfg))

    ax1.set_title("Total losses")
    ax2.set_title("Data losses")
    ax3.set_title("Initial condition (IC) losses")
    plt.xlabel("Epochs")
    plt.ylabel("Losses")
    fig.savefig("output/sammenlining_av_alle.png")
    plt.show()
    
    #######################################################################
    # Oppgave 4.4: Slutt
    #######################################################################


if __name__ == "__main__":
    main()
