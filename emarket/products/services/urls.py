from .. import filters


def compile_inverted_price_url_args(**url_kwargs) -> str:
    url_kwargs["price"] = filters.invert_sorting(
        get_url_arg_from_ordering_field(field=filters.invert_sorting(url_kwargs["price"]))
    )

    return compile_url_args(**url_kwargs)


def compile_url_args(**url_kwargs) -> str:
    url_args = str()

    for arg_name in url_kwargs:
        if type(url_kwargs[arg_name]) in (list, set, frozenset, tuple):
            for value in url_kwargs[arg_name]:
                url_args += f"&{arg_name.replace('_', '')}={value}" if value is not None else ""
        else:
            url_args += f"&{arg_name.replace('_', '')}={url_kwargs[arg_name]}" if url_kwargs[arg_name] is not None else ""

    return url_args


def get_ordering_field_from_url_arg(url_arg: str, field: str) -> str:
    try:
        return ("" if not int(url_arg) else "-") + field
    except:
        return field


def get_url_arg_from_ordering_field(field: str) -> int:
    return int(field.startswith("-"))
