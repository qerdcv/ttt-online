import React from 'react';
import { useTranslation } from 'react-i18next';
import style from 'components/Button/button.module.scss';

interface IButton {
  classNames?: string[];
  disabled?: boolean;
  value: string;
  children?: React.ReactNode;

  onClick?: React.MouseEventHandler<HTMLButtonElement>;
}

export const Button = ({
  value,
  onClick,
  children,
  classNames = [],
  disabled = false,
}: IButton) => {
  const { t } = useTranslation();
  console.log(value);
  return (
    <button
      className={[
        style.btn,
        style.fuzzy,
        !disabled ? style.btnActive : null,
        ...classNames,
      ].join(' ')}
      onClick={onClick}
      disabled={disabled}
    >
      {t(value) || children}
    </button>
  );
};

export const RoundedButton = ({
  value,
  onClick,
  classNames = [],
  disabled = false,
  children,
}: IButton) => {
  const { t } = useTranslation();
  return (
    <button
      className={[
        style.btn,
        style.round,
        !disabled ? style.btnActive : null,
        ...classNames,
      ].join(' ')}
      onClick={onClick}
      disabled={disabled}
    >
      {t(value) || children}
    </button>
  );
};
