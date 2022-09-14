import React, { useContext } from 'react';
import { useTranslation } from 'react-i18next';
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
  const { t } = useTranslation();
  const { user } = useContext<IAuthContext>(AuthContext);
  const getOpponentTitle = (): string => {
    const opponentTitle = t`Opponent`;
    const title = opponent?.username || opponentTitle;

    if (opponent === null) {
      return title + ' ('+t`not joined`+')';
    }

    if (user?.id === opponent?.id) {
      return title + ' ('+t`you`+')';
    }

    return title;
  };

  return (
    <div className={styles.players}>
      <Player isActive={isInGame && currentPlayer?.id === owner.id}
        title={`${owner.username || t`Owner`} ${owner.id === user?.id ? '('+t`you`+')' : ''}`}/>
      <Player isActive={isInGame && currentPlayer?.id === opponent?.id}
        title={getOpponentTitle()}/>
    </div>
  );
};
