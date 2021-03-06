import React, { useContext, useEffect } from 'react';
import { SubmitHandler, useForm } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';

import { Checkbox } from 'components/Form';
import { Button } from 'components/Button';

import { useHttp } from 'hooks/useHttp';
import { Auth } from 'api/auth';
import { IUser } from 'types/user';
import { AuthContext } from 'context/auth.context';

import formStyles from 'styles/form.module.scss';
import styles from 'layouts/auth/auth.module.scss';

interface ILoginForm {
  username: string,
  password: string,
  remember: boolean
}

export const Login = () => {
	const {
		register,
		handleSubmit,
		setValue,
		formState: { errors }
	} = useForm<ILoginForm>();
	const { loading, request, error } = useHttp<IUser>();
	const { setUser } = useContext(AuthContext);
	const navigate = useNavigate();

	useEffect(() => {
		setValue('remember', false);
	}, [setValue]);

	const onSubmit: SubmitHandler<ILoginForm> = async (data) => {
		const user = await request(Auth.login.bind(null, data));
		setUser(user);
		localStorage.setItem('user', JSON.stringify(user));
		navigate('/');
	};

	const onRememberClick = (e: React.FormEvent<HTMLInputElement>) => {
		setValue('remember', e.currentTarget.value !== 'true');
	};

	return (
		<form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
			<div className={formStyles.formControl}>
				<div className={formStyles.formControl}>
					<label htmlFor="username">Username:</label>
					<input type="text" {...register('username', {
						required: {
							value: true,
							message: 'Username is required',
						},
						minLength: {
							value: 4,
							message: 'Username is too short (min 4)'
						},
						maxLength: {
							value: 30,
							message: 'Username is too long (max 30)'
						}
					})} />
					<span className={formStyles.formControlError}>
						{errors.username?.message}
					</span>
				</div>

				<div className={formStyles.formControl}>
					<label htmlFor="password">Password:</label>
					<input type="password" {...register('password', {
						required: {
							value: true,
							message: 'Password is required',
						},
						minLength: {
							value: 4,
							message: 'Password is too short (min 4)'
						},
						maxLength: {
							value: 30,
							message: 'Password is too long (max 30)'
						}
					})} />
					<span className={formStyles.formControlError}>
						{errors.password?.message}
					</span>
				</div>

				<div className={formStyles.formControl}>
					<Checkbox label={'Remember?'} name={'remember'} onChange={onRememberClick}/>
				</div>

				<span className={formStyles.formControlError}>{error.message}</span>
			</div>

			<Button value="Login" disabled={!!Object.keys(errors).length || loading}/>
		</form>
	);
};


interface IRegisterForm {
  username: string,
  password: string,
}


export const Register = () => {
	const {
		register,
		handleSubmit,
		formState: { errors }
	} = useForm<IRegisterForm>();
	const { loading, request, error } = useHttp();
	const navigate = useNavigate();

	const onSubmit: SubmitHandler<IRegisterForm> = async (data) => {
		await request(Auth.register.bind(null, data));
		navigate('/auth/login');
	};

	return (
		<form onSubmit={handleSubmit(onSubmit)} className={styles.form}>
			<div className={formStyles.formControl}>
				<div className={formStyles.formControl}>
					<label htmlFor="username">Username:</label>
					<input type="text" {...register('username', {
						required: {
							value: true,
							message: 'Username is required',
						},
						minLength: {
							value: 4,
							message: 'Username is too short (min 4)'
						},
						maxLength: {
							value: 30,
							message: 'Username is too long (max 30)'
						}
					})} />
					<span className={formStyles.formControlError}>
						{errors.username?.message}
					</span>
				</div>

				<div className={formStyles.formControl}>
					<label htmlFor="password">Password:</label>
					<input type="password" {...register('password', {
						required: {
							value: true,
							message: 'Password is required',
						},
						minLength: {
							value: 4,
							message: 'Password is too short (min 4)'
						},
						maxLength: {
							value: 30,
							message: 'Password is too long (max 30)'
						}
					})} />
					<span className={formStyles.formControlError}>
						{errors.password?.message}
					</span>
				</div>

				<span className={formStyles.formControlError}>{error.message}</span>
			</div>

			<Button value="register" disabled={!!Object.keys(errors).length || loading}/>
		</form>
	);
};

const exports = {
	Login,
	Register,
};

export default exports;
