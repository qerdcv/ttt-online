import { useState } from 'react';
import styles from 'components/Form/Checkbox/checkbox.module.scss';
// import { useForm } from "react-hook-form";

interface ICheckbox {
  label: string;
  name: string;
  onChange(e: React.FormEvent<HTMLInputElement>): void;
}

export const Checkbox: React.FC<ICheckbox> = ({ label, name, onChange }) => {
  const [isChecked, setIsChecked] = useState(false);

  const onCheck = (e: React.FormEvent<HTMLInputElement>) => {
    setIsChecked(!isChecked);

    if (onChange) {
      onChange(e);
    }
  };

  return (
    <label htmlFor={name} className={styles.checkboxLabel}>
      <div
        className={[styles.checkbox, isChecked ? styles.checked : null].join(
          ' '
        )}
      />
      {label}
      <input
        value={isChecked.toString()}
        type="checkbox"
        name={name}
        id={name}
        onChange={onCheck}
      />
    </label>
  );
};
