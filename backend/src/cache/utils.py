from fastapi import Request, Response


def request_key_builder(
    func,
    namespace: str = "",
    *,
    request: Request = None,
    response: Response = None,
    **kwargs,
):
    info = [namespace]
    if request.path_params:
        resource_id = list(request.path_params.keys())[0]
        resource_id = request.path_params[resource_id]

        info.append(resource_id)

    key = ":".join(
        info
        + [
            request.method.lower(),
            request.url.path,
            repr(sorted(request.query_params.items())),
        ]
    )
    return key
