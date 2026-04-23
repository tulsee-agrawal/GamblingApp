from models.gambler_profile import GamblerProfile
from models.betting_preferences import BettingPreferences
from services.gambler_profile_service import GamblerProfileService

service = GamblerProfileService()

profile = GamblerProfile(
    username="star",
    full_name="Tulsee",
    email="tulsee@gmail.com",
    initial_stake=1000,
    win_threshold=1500,
    loss_threshold=500,
    min_required_stake=200
)

prefs = BettingPreferences(
    min_bet=10,
    max_bet=200,
    game_type="roulette",
    auto_play=True,
    auto_games=50,
    session_loss_limit=500,
    session_win_target=1000
)

# service.create_gambler(profile, prefs)

# print(service.get_gambler("star"))

# print(service.validate_eligibility("star"))

service.update_gambler(
    "star",
    profile_data={"full_name": "Updated"},
    pref_data={"max_bet": 300}
)

# service.reset_profile("star")