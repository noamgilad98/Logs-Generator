from logs_generator.utils.distribution_settings_frame import DistributionSettingsFrame

class UsersSettingsFrame(DistributionSettingsFrame):
    def __init__(self, parent, config_manager, app):
        super().__init__(parent, config_manager, app, "Users", 'distinct_users_default', 6)
