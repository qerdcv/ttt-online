import React from 'react';
import { Coords, Marks, TField } from 'types/game';

import styles from 'layouts/game/field.module.scss';
import { Game } from 'api/game';
import { useHttp } from 'hooks/useHttp';

interface IFieldProps {
    child?: React.ReactNode,
    gameID: number,
    field: TField,
}

export const Field = ({ field, gameID }: IFieldProps) => {
  const { request } = useHttp();
  const handleCellClick = (coords: Coords) => {
    request(Game.step.bind(null, { coords }, gameID))
      .catch(console.error);
  };

  return (
    <div className={styles.field}>
      {field.map((row, rowIdx) => (
        <div className={styles.fieldRow} key={`row-${rowIdx}`}>
          {row.map((mark, colIdx) => {
            const classNames = [styles.fieldCell];
            switch (mark) {
            case Marks.ownerMark:
              classNames.unshift(styles.fieldCellOwner);
              break;
            case Marks.opponentMark:
              classNames.unshift(styles.fieldCellOpponent);
              break;
            }
            return (
              <span
                key={`cell-${rowIdx}-${colIdx}`}
                className={classNames.join(' ')}
                onClick={handleCellClick.bind(null, [rowIdx, colIdx])
                }>{mark}</span>
            );
          })}
        </div>
      ))}
    </div>
  );
};
