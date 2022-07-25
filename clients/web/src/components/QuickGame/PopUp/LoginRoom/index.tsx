import { useContext, useState } from 'react';
import { Button } from 'components/Button';
import { PopUpContext, Stack } from 'context/popUp.context';
import styles from 'components/QuickGame/PopUp/LoginRoom/loginRoom.module.scss';
import { useHttp } from 'hooks/useHttp';
import { IGame } from 'types/game';

export const LoginRoom = () => {
  const { request, loading } = useHttp();
  const { onPushPopUpStack } = useContext(PopUpContext);
  const [rooms, setRooms] = useState([]);

  if (loading) {
    return <div className={styles.rooms}>Loading...</div>;
  }

  return (
    <div className={styles.rooms}>
      {rooms.length > 0 ? (
        rooms.map((game: IGame) => (
          <Button
            classNames={[styles.roomsItem]}
            key={game.id}
            onClick={onPushPopUpStack.bind(null, Stack.ConnectRoom, {
              ...game,
            })}
            />
        ))
      ) : (
        <h1>No rooms yet</h1>
      )}
    </div>
  );
};
