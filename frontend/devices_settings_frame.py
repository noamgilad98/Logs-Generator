from logs_generator.utils.distribution_settings_frame import DistributionSettingsFrame

class DevicesSettingsFrame(DistributionSettingsFrame):
    def __init__(self, parent, config_manager, app):
        super().__init__(parent, config_manager, app, "Devices", 'distinct_devices_default', 7)
