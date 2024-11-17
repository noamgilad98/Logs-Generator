from utils.distribution_settings_frame import DistributionSettingsFrame

class CategoriesSettingsFrame(DistributionSettingsFrame):
    def __init__(self, parent, config_manager, app):
        super().__init__(parent, config_manager, app, "Categories", 'distinct_categories_default', 8)
