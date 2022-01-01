import style from 'components/Button/button.module.scss';

export const Button = ({value, classNames=[], type, onClick=()=>{}, disabled=false}) => {
  return (
    <button className={[
      style.btn,
      style.fuzzy,
      !disabled
      ? style.btnActive
      : null,
      ...classNames
    ].join(" ")} onClick={onClick} disabled={disabled}>
      {value}
    </button>
  )
};

export const RoundedButton = ({value, onClick, classNames=[], disabled=false}) => {
  return (
    <button className={[...classNames, style.btn, style.round].join(" ")} onClick={onClick} disabled={disabled}>
      {value}
    </button>
  )
}
