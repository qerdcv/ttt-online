import { useContext, useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLock } from "@fortawesome/free-solid-svg-icons";
import { Button } from "components/Button";
import { PopUpContext } from "context/popUp.context";
import styles from "components/QuickGame/PopUp/LoginRoom/loginRoom.module.scss";
import { connectRoom } from "components/QuickGame/constant";
// import { Room } from "api/room";

const mockedRooms = [
  {_id: "1", room_name: "Room Name 1", is_private: false},
  {_id: "2", room_name: "Room Name 2", is_private: true},
  {_id: "3", room_name: "Room Name 3", is_private: true},
  {_id: "4", room_name: "Room Name 4", is_private: false},
  {_id: "5", room_name: "Room Name 5", is_private: false},
  {_id: "6", room_name: "Room Name 6", is_private: false},
  {_id: "7", room_name: "Room Name 7", is_private: true},
  {_id: "8", room_name: "Room Name 8", is_private: true},
  {_id: "9", room_name: "Room Name 9", is_private: false},
  {_id: "10", room_name: "Room Name 10 very very very very very long name", is_private: true},
]

export const LoginRoom = () => {
  const { onPushPopUpStack } = useContext(PopUpContext)
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    // TODO: add http request
    // Room.get()
    setRooms(mockedRooms);

  }, [])

  return (
    <div className={styles.rooms}>
        {rooms.map(room => (
          <Button classNames={[styles.roomsItem]} key={room._id} onClick={onPushPopUpStack.bind(null, connectRoom, {
            ...room
          })}>
            <span className={styles.roomsItemName}>{room.room_name}</span>
            { room.is_private && (
              <FontAwesomeIcon icon={faLock}/>
            )}
          </Button>
        ))}
    </div>
  )
}
