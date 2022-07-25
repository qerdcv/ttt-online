import { useEffect, useState } from 'react';
import { useParams } from 'react-router-dom';
import styles from 'layouts/game/game.module.scss';
import { Field } from 'layouts/game/field';
import { IGame } from 'types/game';
import { useHttp } from 'hooks/useHttp';


export const GameLayout = () => {
    const [game, setGame] = useState<IGame>();
    const { gameID } = useParams();
    const { loading, request } = useHttp();

    useEffect(() => {

    }, [request]);

    return (
        <div >
            <Field />
        </div>
    )
}