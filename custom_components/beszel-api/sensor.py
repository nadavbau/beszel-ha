from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    entities = []
    for system in coordinator.data:
        entities.append(BeszelCPUSensor(coordinator, system))
        entities.append(BeszelRAMSensor(coordinator, system))
        entities.append(BeszelDiskSensor(coordinator, system))
        entities.append(BeszelBandwidthSensor(coordinator, system))
        entities.append(BeszelTemperatureSensor(coordinator, system))
        entities.append(BeszelUptimeSensor(coordinator, system))
    async_add_entities(entities)

class BeszelBaseSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, system):
        super().__init__(coordinator)
        self._system_id = system.id

    @property
    def system(self):
        for s in self.coordinator.data:
            if s.id == self._system_id:
                return s
        return None

    @property
    def device_info(self):
        sys = self.system
        if sys is None:
            return None
        info = getattr(sys, "info", {})
        return {
            "identifiers": {(DOMAIN, sys.id)},
            "name": sys.name,
            "manufacturer": "Beszel",
            "model": info.get("m"),
            "sw_version": info.get("v"),
            "hw_version": info.get("k"),
        }

class BeszelCPUSensor(BeszelBaseSensor):
    @property
    def unique_id(self):
        return f"beszel_{self._system_id}_cpu"

    @property
    def name(self):
        return f"{self.system.name} CPU" if self.system else None

    @property
    def icon(self):
        return "mdi:memory"

    @property
    def native_value(self):
        return self.system.info.get("cpu") if self.system else None

    @property
    def native_unit_of_measurement(self):
        return "%"

class BeszelRAMSensor(BeszelBaseSensor):
    @property
    def unique_id(self):
        return f"beszel_{self._system_id}_ram"

    @property
    def name(self):
        return f"{self.system.name} RAM" if self.system else None

    @property
    def icon(self):
        return "mdi:chip"

    @property
    def native_value(self):
        return self.system.info.get("mp") if self.system else None

    @property
    def native_unit_of_measurement(self):
        return "%"

class BeszelDiskSensor(BeszelBaseSensor):

    @property
    def unique_id(self):
        return f"beszel_{self._system_id}_disk"

    @property
    def name(self):
        return f"{self.system.name} Disk" if self.system else None

    @property
    def icon(self):
        return "mdi:harddisk"

    @property
    def native_value(self):
        return self.system.info.get("dp") if self.system else None

    @property
    def native_unit_of_measurement(self):
        return "%"

class BeszelBandwidthSensor(BeszelBaseSensor):
    @property
    def unique_id(self):
        return f"beszel_{self._system_id}_bandwidth"

    @property
    def name(self):
        return f"{self.system.name} Bandwidth" if self.system else None

    @property
    def icon(self):
        return "mdi:router-network"

    @property
    def native_value(self):
        return self.system.info.get("b") if self.system else None

    @property
    def native_unit_of_measurement(self):
        return "MB/s"

class BeszelTemperatureSensor(BeszelBaseSensor):
    @property
    def unique_id(self):
        return f"beszel_{self._system_id}_temperature"

    @property
    def name(self):
        return f"{self.system.name} temperature" if self.system else None

    @property
    def native_value(self):
        return self.system.info.get("dt") if self.system else None

    @property
    def device_class(self):
        return "temperature"

    @property
    def native_unit_of_measurement(self):
        return "°C"

class BeszelUptimeSensor(BeszelBaseSensor):
    @property
    def unique_id(self):
        return f"beszel_{self._system_id}_uptime"

    @property
    def name(self):
        return f"{self.system.name} uptime" if self.system else None

    @property
    def icon(self):
        return "mdi:sort-clock-descending"

    @property
    def native_value(self):
        return self.system.info.get("u") / 60 if self.system else None

    @property
    def suggested_display_precision(self):
        return 2

    @property
    def state_class(self):
        return "total_increasing"

    @property
    def native_unit_of_measurement(self):
        return "minutes"