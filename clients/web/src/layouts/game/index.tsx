import axios from 'axios';
import React, { useCallback, useContext, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';

import { AuthContext, IAuthContext } from 'context/auth.context';
import { useHttp } from 'hooks/useHttp';
import { Game } from 'api/game';

import { Field } from 'components/Game/Field';
import { Button } from 'components/Button';

import { defaultGame, GameState, IGame } from 'types/game';

import styles from 'layouts/game/game.module.scss';
import { IUser } from 'types/user';
import { Players } from 'components/Game/Players';


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
    <Button value="JOIN!" classNames={[styles.gameJoinButton]} onClick={handleJoin} disabled={loading}/>
  );
};

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

export const GameLayout = () => {
  const navigate = useNavigate();
  const [game, setGame] = useState<IGame>(defaultGame);
  const { t } = useTranslation();
  const { user } = useContext<IAuthContext>(AuthContext);
  const { gameID = '' } = useParams();
  const { loading, request } = useHttp<IGame>();

  const handleSourceEvent = useCallback((e: MessageEvent) => {
    setGame(JSON.parse(e.data as string) as IGame);
  }, [setGame]);

  useEffect(() => {
    let es: EventSource;
    const sourceURL = !process.env.NODE_ENV || process.env.NODE_ENV !== 'development'
      ? `/api/games/${gameID}/sse`
      : `http://localhost:4444/api/games/${gameID}/sse`;

    request(Game.getByID.bind(null, gameID))
      .then(game => {
        setGame(game);

        es = new EventSource(sourceURL);
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



  if (loading) {
    return <h1>LOADING....</h1>;
  }

  return (
    <>
      <div className={styles.game}>
        <h1>{ t`Game ID` }: {game.id}</h1>
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
        {game.current_state === GameState.pending && user?.id !== game.owner.id && (
          <JoinButton gameID={game.id}/>
        )}
        {game.current_state === GameState.done && (
          <>
            <Winner winner={game.winner} />
            <Button value='Show history' onClick={() => navigate('history')}/>
          </>
        )}
      </div>
    </>
  );
};
