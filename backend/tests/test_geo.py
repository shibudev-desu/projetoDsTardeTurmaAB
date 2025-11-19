import pytest
from unittest.mock import MagicMock, patch
from backend.utils.geo import _haversine_km
from backend.services.geo import recommend_geo


# -----------------------------
#   UNIT TESTS – HAVERSINE
# -----------------------------

def test_haversine_km_same_location():
    assert _haversine_km(0.0, 0.0, 0.0, 0.0) == 0.0


def test_haversine_km_known_distance():
    d = _haversine_km(0.0, 0.0, 0.0, 1.0)
    assert abs(d - 111.319) < 0.2


def test_haversine_km_antipodal_points():
    half_circle = 6371 * 3.14159
    d = _haversine_km(0.0, 0.0, 0.0, 180.0)
    assert abs(d - half_circle) < 0.1


# -----------------------------
#       FIXTURES MOCKADAS
# -----------------------------

@pytest.fixture
def mock_models():
    User = MagicMock()
    Music = MagicMock()
    UserMusicRating = MagicMock()
    return User, Music, UserMusicRating


@pytest.fixture
def mock_user(mock_models):
    User, _, _ = mock_models
    u = MagicMock(id=1, latitude=34.052235, longitude=-118.243683)
    User.get_or_none.return_value = u
    return u


@pytest.fixture
def mock_music_query(mock_models):
    User, Music, _ = mock_models

    near = MagicMock(
        id=101, title="Test Song", artist_id=2,
        posted_at="2023-01-01",
        latitude=34.052235, longitude=-118.243683
    )

    far = MagicMock(
        id=102, title="Far Song", artist_id=3,
        posted_at="2023-01-02",
        latitude=35.0, longitude=-119.0
    )

    near.artist.latitude = near.latitude
    near.artist.longitude = near.longitude

    far.artist.latitude = far.latitude
    far.artist.longitude = far.longitude

    mock_result = MagicMock()
    mock_result.__iter__.return_value = [near, far]

    Music.select.return_value.join.return_value.where.return_value.order_by.return_value.limit.return_value = mock_result
    return Music


# -----------------------------
#   INTEGRATION TESTS – GEO
# -----------------------------

@patch("backend.services.geo.recommend_popular")
def test_recommend_geo_user_not_found(mock_pop, mock_models):
    User, Music, UserMusicRating = mock_models
    User.get_or_none.return_value = None

    mock_pop.return_value = [{"id": 1}]
    result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=999)

    mock_pop.assert_called_once_with(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=999, limit=10)
    assert result == [{"id": 1}]


@patch("backend.services.geo.recommend_popular")
def test_recommend_geo_user_no_location(mock_pop, mock_models):
    User, Music, UserMusicRating = mock_models
    User.get_or_none.return_value = MagicMock(id=1, latitude=None, longitude=None)

    mock_pop.return_value = [{"id": 1}]
    result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating, user_id=1)

    mock_pop.assert_called_once()
    assert result == [{"id": 1}]


def test_recommend_geo_within_radius(mock_models, mock_user, mock_music_query, monkeypatch):
    User, Music, UserMusicRating = mock_models
    UserMusicRating.select.return_value.where.return_value = []

    mock_hav = MagicMock(return_value=5.0)
    monkeypatch.setattr("backend.utils.geo._haversine_km", mock_hav)

    result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating,
                           user_id=1, radius_km=10, limit=1, method="haversine")

    assert len(result) == 1
    assert result[0]["id"] == 101
    assert result[0]["distance_km"] == 5.0
    mock_hav.assert_called()


def test_recommend_geo_outside_radius(mock_models, mock_user, mock_music_query, monkeypatch):
    User, Music, UserMusicRating = mock_models
    UserMusicRating.select.return_value.where.return_value = []

    monkeypatch.setattr("backend.utils.geo._haversine_km", MagicMock(return_value=15.0))

    with patch("backend.services.geo.recommend_popular", return_value=[{"id": 200}]) as mock_pop:
        result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating,
                               user_id=1, radius_km=10, limit=1)

    mock_pop.assert_called_once()
    assert result == [{"id": 200}]


@patch("backend.services.geo.recommend_popular")
def test_recommend_geo_fill_limit(mock_pop, mock_models, mock_user):
    User, Music, UserMusicRating = mock_models
    UserMusicRating.select.return_value.where.return_value = []

    near = MagicMock(id=101, title="Close Song", latitude=34.052235, longitude=-118.243683)
    Music.select.return_value.join.return_value.where.return_value.order_by.return_value.limit.return_value = MagicMock(
        __iter__=lambda *a: iter([near])
    )

    mock_pop.return_value = [{"id": 200}, {"id": 201}]

    with patch("backend.utils.geo._haversine_km", return_value=5.0):
        result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating,
                               user_id=1, radius_km=10, limit=3)

    assert [x["id"] for x in result] == [101, 200, 201]
    mock_pop.assert_called_once_with(user_id=1, limit=2)


@patch("backend.services.geo.recommend_popular")
def test_recommend_geo_no_duplicates(mock_pop, mock_models, mock_user):
    User, Music, UserMusicRating = mock_models
    UserMusicRating.select.return_value.where.return_value = []

    near = MagicMock(id=101, title="Close Song")
    Music.select.return_value.join.return_value.where.return_value.order_by.return_value.limit.return_value = MagicMock(
        __iter__=lambda *a: iter([near])
    )

    mock_pop.return_value = [{"id": 101}, {"id": 201}]

    with patch("backend.utils.geo._haversine_km", return_value=5.0):
        result = recommend_geo(User=User, Music=Music, UserMusicRating=UserMusicRating,
                               user_id=1, radius_km=10, limit=2)

    assert [x["id"] for x in result] == [101, 201]
    mock_pop.assert_called_once_with(user_id=1, limit=1)
