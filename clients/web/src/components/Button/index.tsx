import style from 'components/Button/button.module.scss';
import React from 'react';

interface IButton {
  classNames?: string[];
  disabled?: boolean;
  value?: string;
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
      {value || children}
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
      {value || children}
    </button>
  );
};
