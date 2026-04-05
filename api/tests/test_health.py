from main import app, health


def test_health_returns_ok() -> None:
    assert health() == {"status": "ok"}


def test_health_route_is_registered() -> None:
    assert str(app.url_path_for("health")) == "/health"
