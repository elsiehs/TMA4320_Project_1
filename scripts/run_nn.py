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

    #######################################################################
    # Oppgave 4.4: Start
    #######################################################################
# Plott hvordan tapene utvikler seg i løpet av treningen, og visualiser prediksjonene
# fra det ferdig trente nettverket

# genererer treningsdata
    print("Generating training data...")
    x, y, t, T_fdm, sensor_data = generate_training_data(cfg) 
    
    nn_params, losses_dict = train_nn(sensor_data, cfg)

    print("Preating prediction grid...")
    T_pred = predict_grid(nn_params, x, y, t, cfg)
    
# genererer visualisering av NN
    print("Generating NN visualizations...")
    plot_snapshots(
        x,
        y,
        t,
        T_pred,
        save_path="output/nn/nn_snapshots.png",
    )
    create_animation(
        x, y, t, T_pred, title="Neural Network", save_path="output/nn/nn_animation.gif"
    )
    
#genererer visualisering av differeanden mellom FDM og NN
    print("Generating FDM - NN visualizations...")
    plot_snapshots(
        x,
        y,
        t,
        (T_fdm _ T_pred),
        save_path="output/fdm_vs_nn/fdm_vs_nn_snapshots.png",
    )
    create_animation(
        x, y, t, T_pred, title="FDM - NN", save_path="output/fdm_vs_nn/fdm_vs_nn_animation.gif"
    )
    
 #losses figurer   
    fig, (ax1, ax2, ax3) = plt.subplots(3, 1, figsize=(6,8))
    plt.subplots_adjust(hspace=0.4)
    
    ax1.plot("total", data=losses_dict)
    ax1.set_title("Total losses")
    #ax1.set_xlabel("Epoker")
    #ax1.set_ylabel("Tap")

    ax2.plot("data", data=losses_dict)
    ax2.set_title("Data losses")
    #ax2.set_xlabel("Epoker")
    #ax2.set_ylabel("Tap")

    ax3.plot("ic", data=losses_dict)
    ax3.set_title("Initial condition (IC) losses")
    #ax3.set_xlabel("Epoker")
    #ax3.set_ylabel("Losses")
    plt.xlabel("Epochs")
    plt.ylabel("Losses")
    fig.savefig("output/figures_nn/Losses_nn_orginal.png")
    plt.show()
    
    #######################################################################
    # Oppgave 4.4: Slutt
    #######################################################################


if __name__ == "__main__":
    main()
