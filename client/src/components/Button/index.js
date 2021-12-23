import style from 'components/Button/button.module.scss';

export const Button = ({value, type}) => {
  return (
    <button className={style.btn}>
      {value}
    </button>
  )
};