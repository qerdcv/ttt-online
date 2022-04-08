import { useForm } from 'react-hook-form';
import { Button } from 'components/Button';
import { useEffect, useState } from 'react';
import { Checkbox } from 'components/Form';
import styles from 'components/QuickGame/PopUp/CreateRoom/createRoom.module.scss';
import 'styles/common.scss';
import formStyles from 'styles/form.module.scss';
import { Room } from 'api/room';
import { useHttp } from 'hooks/useHttp';

export const CreateRoom = () => {
  const {
    register,
    handleSubmit,
    formState: { errors },
    setValue,
    resetField,
  } = useForm();
  const { loading, error, request } = useHttp();
  const [isPrivate, setIsPrivate] = useState(false);

  useEffect(() => {
    setValue('is_private', isPrivate);
  }, [setValue, isPrivate]);

  const onCheck = () => {
    setIsPrivate(!isPrivate);
    resetField('password');
  };

  const onSubmit = async () => {
    await request(Room.create);
  };

  return (
    <form
      name="createRoomForm"
      className={styles.createForm}
      onSubmit={handleSubmit(onSubmit)}
    >
      <div>
        <div className={formStyles.formControl}>
          <input
            {...register('room_name', {
              required: 'Room name is required',
              maxLength: {
                value: 20,
                message: 'Room name is too long',
              },
              minLength: {
                value: 3,
                message: 'Room name is too short',
              },
            })}
            autoComplete="off"
            type="text"
            placeholder="Room Name"
          />
          {errors.room_name && (
            <p className={formStyles.formControlError}>
              {errors.room_name?.message}
            </p>
          )}
        </div>
        <Checkbox label="Is Private?" name="is_private" onChange={onCheck} />
        <div className={formStyles.formControl}>
          <input
            {...register('password', {
              required: {
                value: isPrivate,
                message: 'Required if is private flag is ON',
              },
            })}
            type="password"
            placeholder="Room Password"
            name="password"
            className={!isPrivate ? 'hidden' : undefined}
          />
          {errors.room_password && (
            <p className={formStyles.formControlError}>
              {errors.room_password?.message}
            </p>
          )}
        </div>
      </div>

      <Button value="submit" disabled={loading} />

      {Object.keys(error) && <p className="error">{error.message}</p>}
    </form>
  );
};
