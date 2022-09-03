import React, { useContext } from 'react';
import { IUser } from 'types/user';
import { AuthContext, IAuthContext } from 'context/auth.context';
import styles from 'components/Game/Players/players.module.scss';

interface IPlayerProps {
  title: string,
  isActive: boolean,
  child?: React.ReactNode,
}

const Player = ({ title, isActive }: IPlayerProps) => {
  return (
    <div className={isActive ? styles.playersActive : ''}>
      {title}
    </div>
  );
};


interface IPlayersProps {
  isInGame: boolean
  owner: IUser
  opponent?: IUser
  currentPlayer?: IUser
  child?: React.ReactNode
}
export const Players = ({ isInGame, owner, opponent, currentPlayer }: IPlayersProps) => {
  const { user } = useContext<IAuthContext>(AuthContext);
  const getOpponentTitle = (): string => {
    const title = opponent?.username || 'Opponent';

    if (opponent === null) {
      return title + ' (not joined)';
    }

    if (user?.id === opponent?.id) {
      return title + ' (you)';
    }

    return title;
  };

  return (
    <div className={styles.players}>
      <Player isActive={isInGame && currentPlayer?.id === owner.id}
        title={`${owner.username || 'Owner'} ${owner.id === user?.id ? '(you)' : ''}`}/>
      <Player isActive={isInGame && currentPlayer?.id === opponent?.id}
        title={getOpponentTitle()}/>
    </div>
  );
};
