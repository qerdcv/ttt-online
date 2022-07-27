import { useEffect } from 'react';
import { useHttp } from 'hooks/useHttp';
import { Game } from 'api/game';
import { IGame } from 'types/game';
import { useNavigate } from 'react-router-dom';

export const CreateGame = () => {
  const { request } = useHttp<IGame>();
  const navigate = useNavigate();

  useEffect(() => {
    request(Game.create).then(
        game => navigate(`/games/${game.id}`)
    );
  }, [request, navigate]);

  return <h1>Loading...</h1>;
};
