import { useContext, useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLock } from "@fortawesome/free-solid-svg-icons";
import { Button } from "components/Button";
import { PopUpContext } from "context/popUp.context";
import styles from "components/QuickGame/PopUp/LoginRoom/loginRoom.module.scss";
import { connectRoom } from "components/QuickGame/constant";
import { useHttp } from "hooks/useHttp";
import { Room } from "api/room";

export const LoginRoom = () => {
  const {request, loading} = useHttp();
  const { onPushPopUpStack } = useContext(PopUpContext)
  const [rooms, setRooms] = useState([]);

  useEffect(async () => {
    const data = await request(Room.get)
    setRooms(data['rooms']);
  }, [])

  if (loading) {
    return (
      <div className={styles.rooms}>
        Loading...
      </div>
    )
  }

  return (
    <div className={styles.rooms}>
      {rooms.length > 0
        ? rooms.map(room => (
          <Button classNames={[styles.roomsItem]} key={room._id} onClick={onPushPopUpStack.bind(null, connectRoom, {
            ...room
          })}>
            <span className={styles.roomsItemName}>{room.room_name}</span>
            {room.is_private && (
              <FontAwesomeIcon icon={faLock}/>
            )}
          </Button>
        ))
        : (
          <h1>No rooms yet</h1>
        )
      }
    </div>
  )
}
