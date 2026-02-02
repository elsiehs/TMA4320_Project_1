"""Training routines for NN and PINN models."""

import jax
import jax.numpy as jnp
from jax import jit
from tqdm import tqdm

from .config import Config
from .loss import bc_loss, data_loss, ic_loss, physics_loss
from .model import init_nn_params, init_pinn_params
from .optim import adam_step, init_adam
from .sampling import sample_bc, sample_ic, sample_interior


def train_nn(
    sensor_data: jnp.ndarray, cfg: Config
) -> tuple[list[tuple[jnp.ndarray, jnp.ndarray]], dict]:
    """Train a standard neural network on sensor data only.

    Args:
        sensor_data: Sensor measurements [x, y, t, T]
        cfg: Configuration

    Returns:
        params: Trained network parameters
        losses: Dictionary of loss histories
    """
    key = jax.random.key(cfg.seed)
    nn_params = init_nn_params(cfg)
    adam_state = init_adam(nn_params)

    losses = {"total": [], "data": [], "ic": []}  # Fill with loss histories

    #######################################################################
    # Oppgave 4.3: Start
    #######################################################################

    vekt_data = cfg.lambda_data
    vekt_ic = cfg.lambda_ic

    def objektive_fn(nn_params): # dårlig praksis å definere funskjon inne en funskjon
        loss = vekt_data * data_loss(nn_params, sensor_data, cfg) + vekt_ic * ic_loss(nn_params, ic_epoch, cfg)
        return loss
    
    #jit-ifiserer funskjonen slik at dn går raskere i for-loopen
    value_grad_jit = jax.jit(jax.value_and_grad(objektive_fn))

    for epoch in tqdm(range(cfg.num_epochs), desc="Training NN"):
        ic_epoch, key = sample_ic(key, cfg)
        
        # beregner verdien og gradienten til data_loss, og IC_loss funksjonen, bruke JIT?
        value_total, gradient_total =  value_grad_jit(nn_params)  
        value_data =  data_loss(nn_params, sensor_data, cfg)
        value_IC = ic_loss(nn_params, ic_epoch, cfg)
        
        # adam_state: vekter som oppdateres for hvert steg
        # grads: gradienten av loss_fn med respekt til nn_params
        nn_params, adam_state = adam_step(nn_params, gradient_total, adam_state, lr=cfg.learning_rate)
        
        
        # Update the nn_params and losses dictionary
        losses["total"].append(value_total)
        losses["data"].append(value_data)
        losses["ic"].append(value_IC)

    #######################################################################
    # Oppgave 4.3: Slutt
    #######################################################################

    return nn_params, {k: jnp.array(v) for k, v in losses.items()}


def train_pinn(sensor_data: jnp.ndarray, cfg: Config) -> tuple[dict, dict]:
    """Train a physics-informed neural network.

    Args:
        sensor_data: Sensor measurements [x, y, t, T]
        cfg: Configuration

    Returns:
        pinn_params: Trained parameters (nn weights + alpha)
        losses: Dictionary of loss histories
    """
    key = jax.random.key(cfg.seed)
    pinn_params = init_pinn_params(cfg)
    opt_state = init_adam(pinn_params)

    losses = {"total": [], "data": [], "physics": [], "ic": [], "bc": []}

    #######################################################################
    # Oppgave 5.3: Start
    #######################################################################

    # Update the nn_params and losses dictionary

    vekt_ph = cfg.lambda_physics
    vekt_bc = cfg.lambda_bc


    def objective_fn(pinn_params, interior, ic, bc):

        loss_data = data_loss(pinn_params["nn"], sensor_data, cfg)
        loss_ic   = ic_loss(pinn_params["nn"], ic, cfg)
        loss_ph   = physics_loss(pinn_params, interior, cfg)
        loss_bc   = bc_loss(pinn_params, bc, cfg)

        loss_total = (cfg.lambda_data * loss_data+ cfg.lambda_ic * loss_ic + vekt_ph * loss_ph+ vekt_bc * loss_bc)

        return loss_total, (loss_data, loss_ic, loss_ph, loss_bc)


    
    #jit-ifiserer funskjonen slik at dn går raskere i for-loopen
    value_grad_fn = jax.jit(jax.value_and_grad(objective_fn, has_aux=True),static_argnums=())  

    

    for epoch in tqdm(range(cfg.num_epochs), desc="Training PINN"):

        interior_epoch, key = sample_interior(key, cfg)
        ic_epoch, key       = sample_ic(key, cfg)
        bc_epoch, key       = sample_bc(key, cfg)

        (loss_total, (loss_data, loss_ic, loss_ph, loss_bc)), grads = (value_grad_fn(pinn_params, interior_epoch, ic_epoch, bc_epoch))

        pinn_params, opt_state = adam_step(pinn_params, grads, opt_state, lr=cfg.learning_rate)



        # logg
        losses["total"].append(loss_total)
        losses["data"].append(loss_data)
        losses["ic"].append(loss_ic)
        losses["physics"].append(loss_ph)
        losses["bc"].append(loss_bc)


    



    #######################################################################
    # Oppgave 5.3: Slutt
    #######################################################################

    return pinn_params, {k: jnp.array(v) for k, v in losses.items()}
