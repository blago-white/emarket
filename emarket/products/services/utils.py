from emarket import config


def get_product_prices_bounds(request_get_args: dict, max_price_bound: float) -> list[int, int]:
    return sorted(
        [
            max(int(request_get_args.get("min", 0)), 0),
            min(int(request_get_args.get("max", max_price_bound)), config.MAX_PRODUCT_PRICE_USD)
         ]
    )


def filters_window_requested(request_get_args: dict) -> int:
    return int(request_get_args.get("filters", 0))
