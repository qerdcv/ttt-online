import axios from 'axios';
import React, { useCallback, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import { useHttp } from 'hooks/useHttp';
import { Game } from 'api/game';

import { Field } from 'components/Game/Field';
import { defaultGame, GameState, IGame } from 'types/game';

import { IUser } from 'types/user';
import { Players } from 'components/Game/Players';

import styles from 'layouts/history/history.module.scss';

enum KeyupEvents {
  ARROW_LEFT = 'ArrowLeft',
  ARROW_RIGHT = 'ArrowRight',
}

interface IWinnerProps {
  child?: React.ReactNode,
  winner?: IUser,
}

const Winner = ({ winner }: IWinnerProps) => {
  const { t } = useTranslation();
  let title: string;

  const winnerName = winner?.username;

  if (!winnerName) {
    title = t`DRAW!`;
  } else {
    title = `${winnerName} ` + t`WON!`;
  }

  return (
    <h1 className={styles.gameWinner}>{title}</h1>
  );
};

export const GameHistory = () => {
  const navigate = useNavigate();
  const [game, setGame] = useState<IGame>(defaultGame);
  const [games, setGames] = useState<Array<IGame>>();
  const [currentGameCnt, setCurrentGameCnt] = useState(0);
  const { t } = useTranslation();
  const { gameID = '' } = useParams();
  const { loading, request } = useHttp<Array<IGame>>();

  const loadGames = useCallback(async () => {
    try {
      const gms = await request(Game.history.bind(null, +gameID));
      setGame(gms[0]);
      setGames(gms);
    } catch (e) {
      if (axios.isAxiosError(e) && e.response?.status === 404) {
        navigate('/404.html');
      }
    }
  }, [request, gameID, navigate]);

  const handleKeyDownEvent = useCallback((e: KeyboardEvent) => {
    switch (e.code) {
    case KeyupEvents.ARROW_LEFT:
      if (currentGameCnt > 0) {
        setCurrentGameCnt((prevGameCnt) => --prevGameCnt);
      }
      break;
    case KeyupEvents.ARROW_RIGHT:
      if (currentGameCnt < (games?.length || 0) - 1) {
        setCurrentGameCnt((prevGameCnt) => ++prevGameCnt);
      }
      break;
    }
  }, [setCurrentGameCnt, games?.length, currentGameCnt]);

  useEffect(() => {
    loadGames().then().catch(console.error);
  }, [loadGames]);

  useEffect(() => {
    window.addEventListener('keydown', handleKeyDownEvent);
    return () => {
      window.removeEventListener('keydown', handleKeyDownEvent);
    };
  }, [handleKeyDownEvent]);

  useEffect(() => {
    if (games) {
      setGame(games[currentGameCnt]);
    }
  }, [currentGameCnt, games, setGame]);

  if (loading) {
    return <h1>LOADING....</h1>;
  }

  const handleRangeChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setCurrentGameCnt(+e.currentTarget.value);
  };

  return (
    <>
      <div className={styles.history}>
        <h1>{t`Game ID`}: {game.id}</h1>
        <Players
          isInGame={game.current_state === GameState.inGame}
          owner={game.owner}
          opponent={game.opponent}
          currentPlayer={game.current_player}
        />
        <div>
          <h3>{game.current_state}</h3>
          <Field field={game?.field} gameID={game.id} />
        </div>
        {game.current_state === GameState.done && (
          <Winner winner={game.winner} />
        )}
        <input
          className={styles.historyRange}
          type="range"
          min="0"
          max={(games?.length || 0) - 1}
          value={currentGameCnt}
          onChange={handleRangeChange}
          onKeyDown={() => false}
        />
      </div>
    </>
  );
};
