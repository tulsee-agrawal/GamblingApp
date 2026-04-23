import mysql.connector
from settings import settings
def get_connection():
    return mysql.connector.connect(
        host=settings.DB_HOST,
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        database=settings.DB_NAME
    )


conn = get_connection()
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS gamblers (
    gambler_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(100) UNIQUE,
    full_name VARCHAR(150),
    email VARCHAR(150) UNIQUE,
    is_active BOOLEAN DEFAULT TRUE,
    initial_stake DECIMAL(12,2),
    current_stake DECIMAL(12,2),
    win_threshold DECIMAL(12,2),
    loss_threshold DECIMAL(12,2),
    min_required_stake DECIMAL(12,2),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
)
""")


cursor.execute("""
CREATE TABLE IF NOT EXISTS betting_preferences (
    preference_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    gambler_id BIGINT UNIQUE,

    min_bet DECIMAL(12,2),
    max_bet DECIMAL(12,2),
    preferred_game_type VARCHAR(100),

    auto_play_enabled BOOLEAN,
    auto_play_max_games INT,

    session_loss_limit DECIMAL(12,2),
    session_win_target DECIMAL(12,2),

    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,

    FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS betting_strategies (
    strategy_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    strategy_code VARCHAR(100) UNIQUE,
    strategy_name VARCHAR(100),
    strategy_type VARCHAR(100),
    is_progressive BOOLEAN,
    is_active BOOLEAN,
    created_at DATETIME
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS sessions (
    session_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    gambler_id BIGINT,

    status VARCHAR(100),
    end_reason VARCHAR(100),

    starting_stake DECIMAL(12,2),
    ending_stake DECIMAL(12,2),
    peak_stake DECIMAL(12,2),
    lowest_stake DECIMAL(12,2),

    max_games INT,
    games_played INT,
    total_pause_seconds INT,

    started_at DATETIME,
    ended_at DATETIME,
    created_at DATETIME,

    FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS session_parameters (
    parameter_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT UNIQUE,

    lower_limit DECIMAL(12,2),
    upper_limit DECIMAL(12,2),

    min_bet DECIMAL(12,2),
    max_bet DECIMAL(12,2),

    default_win_probability DECIMAL(10,2),
    max_session_minutes INT,
    strict_mode BOOLEAN,

    created_at DATETIME,

    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS pause_records (
    pause_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    session_id BIGINT,

    pause_reason VARCHAR(100),
    paused_at DATETIME,
    resumed_at DATETIME,
    pause_seconds INT,

    FOREIGN KEY (session_id) REFERENCES sessions(session_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS odds_config (
    odds_config_id BIGINT AUTO_INCREMENT PRIMARY KEY,
    odds_type VARCHAR(100),
    fixed_multiplier DECIMAL(10,2),
    american_odds INT,
    decimal_odds DECIMAL(10,2),
    prob_payout_factor DECIMAL(10,2),
    house_edge DECIMAL(10,2),
    is_default BOOLEAN,
    created_at DATETIME
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS bets (
    bet_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_id BIGINT,
    gambler_id BIGINT,
    strategy_id BIGINT,

    game_index INT,
    bet_amount DECIMAL(10,2),
    win_probability DECIMAL(10,2),

    odds_type VARCHAR(100),
    odds_value DECIMAL(10,2),
    potential_win DECIMAL(10,2),

    stake_before DECIMAL(12,2),
    stake_after DECIMAL(12,2),

    is_settled BOOLEAN,
    placed_at DATETIME,

    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id),
    FOREIGN KEY (strategy_id) REFERENCES betting_strategies(strategy_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS game_records (
    game_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_id BIGINT,
    bet_id BIGINT,
    odds_config_id BIGINT,

    outcome VARCHAR(100),
    payout_amount DECIMAL(10,2),
    loss_amount DECIMAL(10,2),
    net_change DECIMAL(10,2),

    stake_before DECIMAL(10,2),
    stake_after DECIMAL(10,2),

    consecutive_win_streak INT,
    consecutive_loss_streak INT,

    game_duration_ms INT,
    resolved_at DATETIME,

    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (bet_id) REFERENCES bets(bet_id),
    FOREIGN KEY (odds_config_id) REFERENCES odds_config(odds_config_id)
)
""")
cursor.execute("""
CREATE TABLE IF NOT EXISTS running_total_snapshots (
    snapshot_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_id BIGINT,
    game_id BIGINT,

    total_games INT,
    total_wins INT,
    total_losses INT,
    total_pushes INT,

    total_winnings DECIMAL(10,2),
    total_losses_amount DECIMAL(10,2),
    net_profit DECIMAL(10,2),

    win_rate DECIMAL(10,2),
    profit_factor DECIMAL(10,2),
    roi DECIMAL(10,2),

    longest_win_streak INT,
    longest_loss_streak INT,

    created_at DATETIME,

    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (game_id) REFERENCES game_records(game_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS validation_events (
    validation_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_id BIGINT,
    gambler_id BIGINT,

    error_type VARCHAR(100),
    severity VARCHAR(100),
    field_name VARCHAR(100),
    attempted_value VARCHAR(100),
    message VARCHAR(200),

    created_at DATETIME,

    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id)
)
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS stake_transactions (
    transaction_id BIGINT AUTO_INCREMENT PRIMARY KEY,

    session_id BIGINT,
    gambler_id BIGINT,
    bet_id BIGINT,
    game_id BIGINT,

    transaction_type VARCHAR(100),
    amount DECIMAL(10,2),

    balance_before DECIMAL(10,2),
    balance_after DECIMAL(10,2),

    transaction_ref VARCHAR(100),
    created_at DATETIME,

    FOREIGN KEY (session_id) REFERENCES sessions(session_id),
    FOREIGN KEY (gambler_id) REFERENCES gamblers(gambler_id),
    FOREIGN KEY (bet_id) REFERENCES bets(bet_id),
    FOREIGN KEY (game_id) REFERENCES game_records(game_id)
)
""")

conn.commit()
conn.close()

print("All tables created successfully!")