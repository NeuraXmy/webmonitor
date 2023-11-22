from flask_sqlalchemy.query import Query
from webmonitor.utils.error import ErrorCode, abort
from flask import request


class PaginationData:
    def __init__(self, total, page, size, pages, items):
        self.total = total
        self.page = page
        self.size = size
        self.pages = pages
        self.items = items


def paginate(query: Query):
    page     = int(request.args.get('page', 1))
    per_page = int(request.args.get('size', 10))

    if page < 1:
        abort(ErrorCode.PARAMS_INVALID, "页码无效")
    if per_page < 1:
        abort(ErrorCode.PARAMS_INVALID, "每页数量无效")

    try:
        pagination = query.paginate(page=page, per_page=per_page, error_out=True)
    except Exception as e:
        abort(ErrorCode.INTERNAL_SERVER_ERROR, str(f"分页错误: {e}"))

    return PaginationData(
        total=pagination.total,
        page=pagination.page,
        size=pagination.per_page,
        pages=pagination.pages,
        items=list(pagination.items)
    )