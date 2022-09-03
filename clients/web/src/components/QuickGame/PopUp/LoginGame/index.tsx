import React from 'react';
import { useTranslation } from 'react-i18next';
import { useNavigate } from 'react-router-dom';
import { useForm } from 'react-hook-form';

import { Button } from 'components/Button';
import { Game } from 'api/game';
import { useHttp } from 'hooks/useHttp';

import formStyles from 'styles/form.module.scss';
import styles from 'components/QuickGame/PopUp/LoginGame/loginGame.module.scss';

interface ILoginGameForm {
  gameID: number;
}

export const LoginGame = () => {
  const navigate = useNavigate();
  const { t } = useTranslation();
  const { register, handleSubmit, formState: { errors } } = useForm<ILoginGameForm>();
  const { request, loading, error } = useHttp();

  const onSubmit = async ({ gameID }: ILoginGameForm) => {
    await request(Game.loginGame.bind(null, gameID));
    navigate(`/games/${gameID}`);
  };

  return (
    <form onSubmit={handleSubmit(onSubmit)} className={styles.loginGame}>
      <div className={formStyles.formControl}>
        <label htmlFor="gameID">{ t`Game ID` }:</label>
        <input type="number" min="1" pattern="\d*" autoFocus {...register('gameID', {
          required: {
            value: true,
            message: t`Game ID is required!`
          }
        })} />
        <span className={formStyles.formControlError}>{errors.gameID?.message}</span>
      </div>
      <div className={formStyles.formControl}>
        <Button value={t`Join Game!`} disabled={loading}/>
      </div>
      <span className={formStyles.formControlError}>{error.message}</span>
    </form>
  );
};
