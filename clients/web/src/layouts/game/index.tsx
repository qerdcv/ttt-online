import axios from 'axios';
import React, { useCallback, useContext, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';

import { AuthContext } from 'context/auth.context';
import { useHttp } from 'hooks/useHttp';
import { Game } from 'api/game';

import { Field } from 'layouts/game/field';
import { Button } from 'components/Button';

import { defaultGame, GameState, IGame } from 'types/game';

import styles from 'layouts/game/game.module.scss';

interface IPlayerProps {
    title: string,
    isActive: boolean,
    child?: React.ReactNode,
}

const Player = ({ title, isActive }: IPlayerProps) => {
    return (
        <div className={isActive ? styles.gameActivePlayer : ''}>
            {title}
        </div>
    );
};

interface IJoinButton {
    gameID: number,
    child?: React.ReactNode,
}

const JoinButton = ({ gameID }: IJoinButton) => {
    const { loading, request } = useHttp();
    const handleJoin = async () => {
        await request(Game.loginGame.bind(null, gameID));
    };

    return (
        <Button value="JOIN!" onClick={handleJoin} disabled={loading}/>
    );
};

interface IWinnerProps {
    child?: React.ReactNode,
    winnerID: number,
}

const Winner = ({ winnerID }: IWinnerProps) => {
    let title: string;

    if (winnerID === null) {
        title = 'DRAW!';
    } else {
        title = `${winnerID} WON!`;
    }

    return (
        <h1>{title}</h1>
    );
};

export const GameLayout = () => {
    const navigate = useNavigate();
    const [game, setGame] = useState<IGame>(defaultGame);
    const { user } = useContext(AuthContext);
    const { gameID } = useParams();
    const { loading, request } = useHttp<IGame>();

    const handleSourceEvent = useCallback((e: MessageEvent) => {
        setGame(JSON.parse(e.data));
    }, [setGame]);

    useEffect(() => {
        let es: EventSource;
        request(Game.getByID.bind(null, gameID))
            .then(game => {
                setGame(game);

                es = new EventSource(`/api/games/${gameID}/sse`);
                es.addEventListener('message', handleSourceEvent);
            })
            .catch(e => {
                if (axios.isAxiosError(e) && e.response?.status === 404) {
                    return navigate('/404.html');
                }
            });
        return () => {
            if (es) {
                es.close();
            }
        };
    }, [setGame, handleSourceEvent, navigate, request, gameID]);

    const getOpponentTitle = (): string => {
        let title = 'Opponent';

        if (game.opponent_id === null) {
            return title + ' (not joined)';
        }

        if (user.id === game.opponent_id) {
            return title + ' (you)';
        }

        return title;
    };

    if (loading) {
        return <h1>LOADING....</h1>;
    }

    return (
        <>
            <div className={styles.game}>
                <h1>Game ID: {game.id}</h1>
                <div className={styles.gamePlayers}>
                    <Player isActive={game.current_state === GameState.inGame && game.current_player_id === game.owner_id}
                            title={`Owner ${game.owner_id === user.id ? '(you)' : ''}`}/>
                    <Player isActive={game.current_state === GameState.inGame && game.current_player_id === game.opponent_id}
                            title={getOpponentTitle()}/>
                </div>
                <div>
                    <h3>{game.current_state}</h3>
                    <Field field={game?.field} gameID={game.id} />
                </div>
                {game.current_state === GameState.pending && user.id && user.id !== game.owner_id && (
                    <JoinButton gameID={game.id}/>
                )}
                {game.current_state === GameState.done && (
                    <Winner winnerID={game.winner_id} />
                )}
            </div>
        </>

    );
};
