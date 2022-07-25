import { useContext } from 'react';
import { useForm } from 'react-hook-form';
import { PopUpContext } from 'context/popUp.context';
import { Button } from 'components/Button';
import { useHttp } from 'hooks/useHttp';

import style from 'components/QuickGame/PopUp/ConnectRoom/connectRoom.module.scss';
import formStyle from 'styles/form.module.scss';

export const ConnectRoom = () => {
  const {
    formState: { errors },
    register,
    handleSubmit,
  } = useForm();
  const { loading } = useHttp();
  const { popUpCtx } = useContext(PopUpContext);

  const onSubmit = () => {
    console.log();
  };

  return (
    <form className={style.connectForm} onSubmit={handleSubmit(onSubmit)}>
      <div>
        <h3 className={style.connectFormRoomName}>{popUpCtx.room_name}</h3>
        {popUpCtx?.is_private && (
          <div className={formStyle.formControl}>
            <input
              {...register('room_password', {
                required: true,
              })}
              type="password"
              placeholder="Game password"
            />
            {errors?.room_password && (
              <p className={formStyle.formControlError}>
                Password is required for private room
              </p>
            )}
          </div>
        )}
      </div>
      <Button
        value={'Connect'}
        disabled={loading || !!Object.keys(errors).length}
      />
    </form>
  );
};
