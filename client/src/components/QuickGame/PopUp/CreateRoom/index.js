import { Button } from "components/Button";
import { useState } from "react";
import { Checkbox } from "components/Form";
import styles from "components/QuickGame/PopUp/CreateRoom/createRoom.module.scss";
import "styles/common.scss";
import { Room } from "../../../../api/room";

export const CreateRoom = () => {
  const [isPrivate, setIsPrivate] = useState(false);

  const onCheck = (e) => {
    setIsPrivate(!isPrivate)
  }

  const onSubmit = async (e) => {
    e.preventDefault();
    const elements = e.target.elements;

    try {
      await Room.create(JSON.stringify({
        name: elements["room_name"].value,
        is_private: elements.is_private.value === "true",
        password: elements["room_password"].value,
      }))
    } catch (e) {
      console.log(e)
    }

  }

  return (
    <form
      name="createRoomForm"
      className={styles.createForm}
      onSubmit={onSubmit}
    >
      <div>
        <input autoComplete="off" type="text" placeholder="Room Name" name="room_name" required/>
        <Checkbox label="Is Private?" name="is_private" onChange={onCheck}/>
        <input
          type="password"
          placeholder="Room Password"
          name="room_password"
          className={!isPrivate ? "hidden" : null}
        />
      </div>

      <Button value="submit"/>
    </form>
  );
};
