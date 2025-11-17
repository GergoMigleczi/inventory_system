class UrlBuilder:
    def __init__(self, url_name, params=None, query=None):
        """
        url_name -> name of the URL pattern
        params   -> list of positional args (existing behaviour)
        query    -> dict of querystring params (new, optional)
        """
        self.url_name = url_name
        self.params = params or []
        self.query = query or {}

    def resolve(self, row, context):
        """
        Returns (args, query_params)
        Maintaining old behaviour:
        - Previously returned only args
        - Now returns (args, query_dict)
        """

        resolved_args = []

        # resolve positional args (existing logic preserved)
        for p in self.params:
            if callable(p):
                resolved_args.append(p(row, context))
            elif isinstance(p, str):
                if hasattr(row, p):
                    resolved_args.append(getattr(row, p))
                else:
                    resolved_args.append(context.get(p))
            else:
                resolved_args.append(p)

        # resolve NEW query params
        resolved_query = {}
        for key, p in self.query.items():
            if callable(p):
                resolved_query[key] = p(row, context)
            elif isinstance(p, str):
                if hasattr(row, p):
                    resolved_query[key] = getattr(row, p)
                else:
                    resolved_query[key] = context.get(p)
            else:
                resolved_query[key] = p

        return resolved_args, resolved_query

    def __bool__(self):
        return self.url_name is not None
