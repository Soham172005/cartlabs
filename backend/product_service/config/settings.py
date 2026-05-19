from cartlabs_common.settings import build_settings

globals().update(build_settings("product_service", apps=["core.apps.CoreConfig"]))
