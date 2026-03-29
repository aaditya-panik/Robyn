import logging

from robyn.robyn import HttpMethod, Request
from robyn.router import Router
from robyn.types import PathParams


def _add_route(router, endpoint, handler):
    """Register a handler with minimal required args."""
    router.add_route(
        route_type=HttpMethod.GET,
        endpoint=endpoint,
        handler=handler,
        is_const=False,
        auth_required=False,
        openapi_name="test",
        openapi_tags=[],
        exception_handler=None,
        injected_dependencies={},
    )


class TestPathParamWarning:
    """Tests for issue #1336: false-positive path params warning."""

    def test_no_warning_with_typed_request(self, caplog):
        def handler(request: Request):
            pass

        router = Router()
        with caplog.at_level(logging.WARNING, logger="robyn.router"):
            _add_route(router, "/:id", handler)
        assert "declares path params" not in caplog.text

    def test_no_warning_with_reserved_name(self, caplog):
        def handler(request):
            pass

        router = Router()
        with caplog.at_level(logging.WARNING, logger="robyn.router"):
            _add_route(router, "/:id", handler)
        assert "declares path params" not in caplog.text

    def test_warning_fires_without_request_access(self, caplog):
        def handler():
            pass

        router = Router()
        with caplog.at_level(logging.WARNING, logger="robyn.router"):
            _add_route(router, "/:id", handler)
        assert "declares path params" in caplog.text

    def test_no_warning_with_pathparams_annotation(self, caplog):
        def handler(path_params: PathParams):
            pass

        router = Router()
        with caplog.at_level(logging.WARNING, logger="robyn.router"):
            _add_route(router, "/:id", handler)
        assert "declares path params" not in caplog.text
