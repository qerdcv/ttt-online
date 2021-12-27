import style from 'components/Button/button.module.scss';

export const Button = ({value, classNames=[], type, onClick=()=>{}}) => {
  return (
    <button className={[style.btn, style.fuzzy, ...classNames].join(" ")} onClick={onClick}>
      {value}
    </button>
  )
};

export const RoundedButton = ({value, onClick, classNames=[]}) => {
  return (
    <button className={[...classNames, style.btn, style.round].join(" ")} onClick={onClick}>
      {value}
    </button>
  )
}
