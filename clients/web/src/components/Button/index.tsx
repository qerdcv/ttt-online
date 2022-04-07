import style from 'components/Button/button.module.scss';

export const Button = ({value, classNames=[], type, onClick=()=>{}, disabled=false, children}) => {
  return (
    <button className={[
      style.btn,
      style.fuzzy,
      !disabled
        ? style.btnActive
        : null,
      ...classNames
    ].join(" ")} onClick={onClick} disabled={disabled}>
      {value || children}
    </button>
  )
};

export const RoundedButton = ({value, onClick, classNames=[], disabled=false, children}) => {
  return (
    <button className={[
      style.btn,
      style.round,
      !disabled
        ? style.btnActive
        : null,
      ...classNames ].join(" ")} onClick={onClick} disabled={disabled}>
      {value || children}
    </button>
  )
}
