from utils.distribution_settings_frame import DistributionSettingsFrame

class DestinationsSettingsFrame(DistributionSettingsFrame):
    def __init__(self, parent, config_manager, app):
        super().__init__(parent, config_manager, app, "Destinations", 'distinct_destinations_default', 5)
