from abc import ABC, abstractmethod

from src.config import *


class PowerPlant(ABC):
    """
    Abstract base class representing a power plant.
    All power plant types should inherit from this class.
    """

    def __init__(self, plant_data: dict, price_per_raw_mw: float) -> None:
        """
        Initialize a power plant with the given data and price per raw MW.

        Args:
            plant_data (dict): Dictionary containing power plant data.
            price_per_raw_mw (float): Price per raw MW of production.
        """
        self.name = plant_data[KEY_NAME]
        self.efficiency = plant_data[KEY_EFFICIENCY]
        self.pmin = plant_data[KEY_PRODUCTION_MIN]
        self.pmax = plant_data[KEY_PRODUCTION_MAX]
        self.price_per_raw_mw = price_per_raw_mw

    @abstractmethod
    def get_cost_per_mw(self) -> float:
        """
        Calculate and return the cost per MW of production.

        Returns:
            float: Cost per MW of production.
        """
        pass

    @abstractmethod
    def calculate_production(self, missing_load: int) -> float:
        """
        Calculate the production capacity of the power plant based on the missing load.

        Args:
            missing_load (int): Amount of load yet to be fulfilled.

        Returns:
            float: Production capacity of the power plant.
        """
        pass

    def get_maximum_production(self):
        """
        Get the maximum production capacity of the power plant.

        Returns:
            float: Maximum production capacity.
        """
        output = self.pmax
        # Ensure output is multiple of 0.1 (round down)
        output = int(output * 10) / 10
        return output

    def get_minimum_production(self) -> float:
        """
        Get the minimum production capacity of the power plant.

        Returns:
            float: Minimum production capacity.
        """
        output = self.pmin
        # Ensure output is multiple of 0.1
        output = round(output, 1)
        return output

    def generate_metrics(self) -> dict:
        """
        Generate a dictionary of metrics for the power plant.

        Returns:
            dict: Metrics including cost, maximum production, minimum production, and name ID.
        """
        return {
            "cost": self.get_cost_per_mw(),
            "maximum_production": self.get_maximum_production(),
            "minimum_production": self.get_minimum_production(),
            "name_id": self.name,
        }


class WindMill(PowerPlant):
    """
    Represents a windmill power plant.
    """

    def __init__(self, plant_data: dict, percentage_wind: float) -> None:
        """
        Initialize a windmill power plant with the given data and wind percentage.

        Args:
            plant_data (dict): Dictionary containing windmill power plant data.
            percentage_wind (float): Percentage of wind availability.
        """
        self.percentage_wind = percentage_wind
        super().__init__(plant_data, price_per_raw_mw=0)

    def get_cost_per_mw(self):
        return 0

    def calculate_production(self, missing_load: int):
        maximum_production = self.pmax * self.percentage_wind
        final_production = min(maximum_production, missing_load)
        # Ensure output is multiple of 0.1
        final_production = (
            round(final_production, 1)
            if final_production <= maximum_production
            else int(final_production * 10) / 10
        )
        return final_production

    def get_maximum_production(self):
        output = self.pmax * self.percentage_wind
        # Ensure output is multiple of 0.1 (round down)
        output = round(output, 1)
        return output


class GasPowerPlant(PowerPlant):
    """
    Represents a gas fired power plant.
    """

    def __init__(self, plant_data: dict, price_gas_per_mw: float) -> None:
        """
        Initialize a gas fired power plant with the given data and gas price per MW.

        Args:
            plant_data (dict): Dictionary containing gas power plant data.
            price_gas_per_mw (float): Price of gas per MW.
        """
        super().__init__(plant_data, price_per_raw_mw=price_gas_per_mw)

    def get_cost_per_mw(self):
        return self.price_per_raw_mw + (1 / self.efficiency)

    def calculate_production(self, missing_load: int):
        if missing_load > 0:
            baseline_production = max(missing_load, self.pmin)
            final_production = min(baseline_production, self.pmax)
            # Ensure output is multiple of 0.1
            final_production = round(final_production, 1)
            return final_production
        else:
            return 0


class JetPowerPlant(PowerPlant):
    """
    Represents a Turbo Jet power plant.
    """

    def __init__(self, plant_data: dict, price_kerosine_per_mw: float) -> None:
        """
        Initialize a Turbo Jet power plant with the given data and kerosine price per MW.

        Args:
            plant_data (dict): Dictionary containing jet power plant data.
            price_kerosine_per_mw (float): Price of kerosine per MW.
        """
        super().__init__(plant_data, price_per_raw_mw=price_kerosine_per_mw)

    def get_cost_per_mw(self):
        return self.price_per_raw_mw + (1 / self.efficiency)

    def calculate_production(self, missing_load: int):
        if missing_load > 0:
            baseline_production = max(missing_load, self.pmin)
            final_production = min(baseline_production, self.pmax)
            # Ensure output is multiple of 0.1
            final_production = round(final_production, 1)
            return final_production
        else:
            return 0
