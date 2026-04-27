from services.gambler_profile_service import GamblerProfileService
from services.stake_management_service import StakeManagementService
from services.betting_service import BettingService
from services.game_session_manager import GameSessionManager
from services.win_loss_calculator import WinLossCalculator
from strategies.random_outcome_strategy import RandomOutcomeStrategy
from models.gambler_profile import GamblerProfile
from models.betting_preferences import BettingPreferences
from models.session_parameters import SessionParameters
from strategies.martingale_strategy import MartingaleStrategy

profile_service = GamblerProfileService()
stake_service = StakeManagementService()
bet_service = BettingService()
session_manager = GameSessionManager()

GAMBLER_ID = 1
SESSION_ID = 1


def menu():
    while True:
        print("\nGAMBLING APP MENU ")
        print("1. Create Gambler (UC1)")
        print("2. View Gambler (UC1)")
        print("3. Validate Gambler (UC1)")
        print("4. Update Gambler (UC1)")
        print("5. Reset Gambler (UC1)")

        print("6. Stake Operation (UC2)")

        print("7. Place Bet (UC3)")
        print("8. Start Session (UC4)")
        print("9. Continue Session (UC4)")
        print("10. Pause Session (UC4)")
        print("11. Resume Session (UC4)")
        print("12. Run Win/Loss Calculator (UC5)")
        print("\n0. Exit")

        choice = input("Enter choice: ")

        try:
            
            if choice == "1":
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

                profile_service.create_gambler(profile, prefs)
                print("Gambler created!")

            elif choice == "2":
                print(profile_service.get_gambler("star"))

            elif choice == "3":
                print(profile_service.validate_eligibility("star"))

            elif choice == "4":
                profile_service.update_gambler(
                    "star",
                    profile_data={"full_name": "Updated Name"}
                )
                print("Updated")

            elif choice == "5":
                profile_service.reset_profile("star")
                print("Reset done")

            elif choice == "6":
                print("\nRunning Stake Operations...")

                stake_service.initialize_stake(SESSION_ID, GAMBLER_ID, 1000)

                stake_service.process_bet(GAMBLER_ID, SESSION_ID, 100, True)
                stake_service.process_bet(GAMBLER_ID, SESSION_ID, 200, False)

                history = stake_service.get_history(GAMBLER_ID)
                print("Stake History:", history)

            elif choice == "7":
                bet = bet_service.place_bet(
                    session_id=SESSION_ID,
                    gambler_id=GAMBLER_ID,
                    strategy_id=None,
                    game_index=1,
                    bet_amount=100,
                    win_probability=0.5
                )
                print("Bet placed:", bet.outcome, bet.stake_after)
            elif choice == "8":
                params = SessionParameters(
                    upper_limit=1500,
                    lower_limit=500,
                    min_bet=10,
                    max_bet=200,
                    max_games=5
                )

                session_manager.start_new_session(
                    SESSION_ID,
                    GAMBLER_ID,
                    1000,
                    params
                )
                print("Session started!")

            elif choice == "9":
                strategy = MartingaleStrategy(50)

                summary = session_manager.continue_session(
                    gambler_id=GAMBLER_ID,
                    betting_service=bet_service,
                    strategy=strategy
                )

                print("Session finished:", summary)

            elif choice == "10":
                session_manager.pause_session(GAMBLER_ID, "User break")
                print("Session paused")

            elif choice == "11":
                session_manager.resume_session(GAMBLER_ID)
                print("Session resumed")
            elif choice == "12":
                print("\nRunning UC5..")

                calc = WinLossCalculator(
                        initial_balance=1000,
                        outcome_strategy=RandomOutcomeStrategy()
                        )

                for i in range(5):
                    result = calc.process_game(
                        bet_amount=100,
                        probability=0.5  
                    )

                    print(f"Game {i+1}: {result.outcome}, Balance: {result.stake_after}")

                print("\nSummary:", calc.summary())
            elif choice == "0":
                print("Exiting...")
                break

            else:
                print("Invalid choice")

        except Exception as e:
            print("Error:", e)


if __name__ == "__main__":
    menu()