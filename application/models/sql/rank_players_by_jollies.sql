-- Rank the players participating in game {{ game_id }} from most to least amount of jollies gained
-- Template variables:
--      game_id: int, game ID
SELECT
    exchanges.receiving_player AS receiver_id,
    players.name AS receiver_name,
    SUM(favors.jollies) AS n_jollies
FROM exchanges
    JOIN favors on favors.id = exchanges.favor_id
    JOIN players ON exchanges.receiving_player = players.id
WHERE
    exchanges.game_id = {{ game_id}}
GROUP BY receiver_id, receiver_name
ORDER BY n_jollies DESC