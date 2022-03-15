import inspect
import logging

from biliup import common
from biliup import engine
from .engine.decorators import Plugin

logger = logging.getLogger('biliup')


def upload(platform, data):
    """
    上传入口
    :param platform:
    :param index:
    :param data: 现在需包含内容{url,date} 完整包含内容{url,date,format_title}
    :return:
    """
    index = data['name']
    try:
        cls = Plugin.upload_plugins.get(platform)
        if cls is None:
            return logger.error(f"No such uploader: {platform}")
        sig = inspect.signature(cls)
        context = {**engine.config, **engine.config['streamers'][index]}
        kwargs = {}
        for k in sig.parameters:
            v = context.get(k)
            if v:
                kwargs[k] = v
        date = data.get("date") if data.get("date") else common.time_now()
        threshold = engine.config.get('filtering_threshold')
        if threshold:
            data['threshold'] = threshold
        if data.get("format_title") is None:
            data["format_title"] = f"{date}{index}"
        return cls(index, data, **kwargs).start()
    except:
        logger.exception("Uncaught exception:")