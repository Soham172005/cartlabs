from cartlabs_common.settings import build_settings

globals().update(build_settings("gateway", apps=["core.apps.CoreConfig"]))
