import style from 'components/Button/button.module.scss';

export const Button = ({value, classNames=[], type}) => {
  return (
    <button className={[style.btn, ...classNames].join(" ")}>
      {value}
    </button>
  )
};