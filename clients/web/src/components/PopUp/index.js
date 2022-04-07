import style from "components/PopUp/PopUp.module.scss";
import { RoundedButton } from "components/Button";
import { useContext, useState } from "react";
import { PopUpContext } from "context/popUp.context";

export const PopUp = ({closeEvent, children}) => {
  const { popUpStack, onPopPopUpStack } = useContext(PopUpContext);

  const [className, setClassName] = useState(style.content.toString());

  const onClose = () => {
    setClassName((prevClassName) => `${prevClassName} ${style.hidden}`);

    if (closeEvent) {
      setTimeout(closeEvent, 300);
    }
  };

  return (
    <div className={style.overlay}>
      <div className={style.overlay} onClick={onClose} />
      <div className={className}>
        <div className={style.contentNav}>
          {popUpStack.length > 1 && (
            <RoundedButton onClick={onPopPopUpStack} value={"ᐊ"}/>
          )}
          <RoundedButton onClick={onClose} value={"⨉"}/>
        </div>
        {children}
      </div>
    </div>
  );
};
