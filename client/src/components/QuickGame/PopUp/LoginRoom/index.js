import { useEffect, useState } from "react";
import { FontAwesomeIcon } from "@fortawesome/react-fontawesome";
import { faLock } from "@fortawesome/free-solid-svg-icons";
import styles from "components/QuickGame/PopUp/LoginRoom/loginRoom.module.scss";
// import { Room } from "api/room";

const mockedRooms = [
  {_id: "1", name: "Room Name 1", is_private: false},
  {_id: "2", name: "Room Name 2", is_private: true},
  {_id: "3", name: "Room Name 3", is_private: true},
  {_id: "4", name: "Room Name 4", is_private: false},
  {_id: "5", name: "Room Name 5", is_private: false},
  {_id: "6", name: "Room Name 6", is_private: false},
  {_id: "7", name: "Room Name 7", is_private: true},
  {_id: "8", name: "Room Name 8", is_private: true},
  {_id: "9", name: "Room Name 9", is_private: false},
  {_id: "10", name: "Room Name 10 very very very very very long name", is_private: true},
]

export const LoginRoom = () => {
  const [rooms, setRooms] = useState([]);

  useEffect(() => {
    // TODO: add http request
    // Room.get()
    setRooms(mockedRooms);

  }, [])

  return (
    <div className={styles.rooms}>
      <ul>
        {rooms.map(room => (
          <li className={styles.roomsItem} key={room._id}>
            <span className={styles.roomsItemName}>{room.name}</span>
            { room.is_private && (
              <FontAwesomeIcon icon={faLock}/>
            )}
          </li>
        ))}
        {/*<li className={styles.roomsItem}>name</li>*/}
      </ul>
    </div>
  )
}