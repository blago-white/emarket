def convert_category_filters_to_product_filters(query_filters: dict) -> None:
    for query_filter_column, query_filter_value in tuple(zip(query_filters.keys(), query_filters.values())):
        if not ("phones__" in query_filter_column):
            continue

        query_filters[query_filter_column.replace("phones__", "")] = query_filters[query_filter_column]
        del query_filters[query_filter_column]
