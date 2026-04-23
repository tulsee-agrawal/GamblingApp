
# USE CASE 1

# from models.gambler_profile import GamblerProfile
# from models.betting_preferences import BettingPreferences
# from services.gambler_profile_service import GamblerProfileService

# service = GamblerProfileService()

# profile = GamblerProfile(
#     username="star",
#     full_name="Tulsee",
#     email="tulsee@gmail.com",
#     initial_stake=1000,
#     win_threshold=1500,
#     loss_threshold=500,
#     min_required_stake=200
# )

# prefs = BettingPreferences(
#     min_bet=10,
#     max_bet=200,
#     game_type="roulette",
#     auto_play=True,
#     auto_games=50,
#     session_loss_limit=500,
#     session_win_target=1000
# )

# service.create_gambler(profile, prefs)

# print(service.get_gambler("star"))

# print(service.validate_eligibility("star"))

# service.update_gambler(
#     "star",
#     profile_data={"full_name": "Updated"},
#     pref_data={"max_bet": 300}
# )

# service.reset_profile("star")





## UC2 
# from services.stake_management_service import StakeManagementService


# stake_service = StakeManagementService()

# monitor = stake_service.initialize_stake(session_id=1, gambler_id=3, initial_amount=1000)

# print(stake_service.process_bet(3, 1, 100, True))   # win
# print(stake_service.process_bet(3, 1, 200, False))  # loss

# print(stake_service.get_history(3))
from models.stake_monitor import StakeMonitor

monitor = StakeMonitor(1000)

monitor.update(1200)
monitor.update(800)
monitor.update(1500)
monitor.update(700)

print("Current:", monitor.current_stake)
print("Peak:", monitor.peak)
print("Lowest:", monitor.lowest)
print("Volatility:", monitor.volatility())
print("History:", monitor.history)