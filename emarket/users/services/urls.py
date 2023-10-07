def get_url_with_args(url: str, **url_args) -> str:
    return url + "?" + "&".join([f"{key}={value}" for key, value in zip(url_args.keys(), url_args.values())])
