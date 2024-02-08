from abc import ABC, abstractmethod

import pandas as pd

from src.powerplants import WindMill, GasPowerPlant, JetPowerPlant
from src.config import *


def generate_production_plan(payload: dict) -> list:
    """
    Generate the production plan for power plants based on the given payload.

    Args:
        payload (dict): The payload containing load, fuels, and power plant data.

    Returns:
        list: The production plan specifying how much power each power plant should deliver.
    """
    # Validate input:
    assert all(key in payload.keys() for key in (KEY_LOAD, KEY_FUELS, KEY_POWER_PLANTS))

    # Load the payload.
    load = payload[KEY_LOAD]
    fuels = payload[KEY_FUELS]
    powerplants = payload[KEY_POWER_PLANTS]

    # Prices
    gas_cost = fuels[KEY_PRICE_GAS]
    kerosine_cost = fuels[KEY_PRICE_KEROSINE]
    # Wind Speed percentage. Convert to float:
    wind_percentage = fuels[KEY_WIND_PRCT] / 100

    # Iterate over power plants
    power_plants_inst_dict = {}
    power_plants_dict_list = []

    for power_plant_dict in powerplants:
        if power_plant_dict[KEY_TYPE] == TYPE_WINDMILL:
            power_plant = WindMill(
                plant_data=power_plant_dict, percentage_wind=wind_percentage
            )

        elif power_plant_dict[KEY_TYPE] == TYPE_GAS_PPLANT:
            power_plant = GasPowerPlant(
                plant_data=power_plant_dict, price_gas_per_mw=gas_cost
            )
        elif power_plant_dict[KEY_TYPE] == TYPE_JET_PPLANT:
            power_plant = JetPowerPlant(
                plant_data=power_plant_dict, price_kerosine_per_mw=kerosine_cost
            )

        # Save instance and metrics
        power_plants_inst_dict[power_plant.name] = power_plant
        power_plants_dict_list.append(power_plant.generate_metrics())

    # Create a DataFrame to represent the merit order of power plants
    merit_order_df = (
        pd.DataFrame(power_plants_dict_list)
        .sort_values(["cost", "maximum_production"], ascending=[True, False])
        .reset_index(drop=True)
    )
    merit_order_df["total_load"] = merit_order_df.maximum_production.cumsum()

    # Find the last power plants needed to meet the load
    last_power_plants_needed = merit_order_df[merit_order_df.total_load >= load].iloc[0]
    missing_load = load - (
        last_power_plants_needed.total_load
        - last_power_plants_needed.maximum_production
    )

    # Calculate the production of the last power plant to meet the missing load
    last_power_plant_production = power_plants_inst_dict[
        last_power_plants_needed.name_id
    ].calculate_production(missing_load=missing_load)

    # Set the production for each power plant in the merit order
    merit_order_df["p"] = 0.0
    merit_order_df.loc[merit_order_df.index < last_power_plants_needed.name, "p"] = (
        merit_order_df.loc[
            merit_order_df.index < last_power_plants_needed.name
        ].maximum_production
    )
    merit_order_df.loc[merit_order_df.index == last_power_plants_needed.name, "p"] = (
        last_power_plant_production
    )
    merit_order_df = merit_order_df.rename(columns={"name_id": "name"})
    return merit_order_df[["name", "p"]].to_dict(orient="records")
