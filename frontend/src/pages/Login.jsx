import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import './LoginRegister.css'

function Login() {
    const [formData, setFormData] = useState({
        email: '',
        password: ''
    })

    const [error, setError] = useState('')
    const [fieldErrors, setFieldErrors] = useState({
        email: '',
        password: ''
    })

    const validateForm = () => {
        const newErrors = {
            email: '',
            password: ''
        }

        if (!formData.email.trim()) {
            newErrors.email = 'Email is required'
        }
        if (!formData.password.trim()) {
            newErrors.password = 'Password is required'
        }

        setFieldErrors(newErrors)
        return !newErrors.email && !newErrors.password
    }

    const navigate = useNavigate()

    const handleChange = (e) => {
        const { name, value } = e.target
        setFormData({
            ...formData,
            [name]: value
        })

        if (fieldErrors[name]) {
            setFieldErrors({
                ...fieldErrors,
                [name]: ''
            })
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setFieldErrors({ email: '', password: '' })
        setError('')

        // Validate form fields
        if (!validateForm()) {
            return;
        }
        
        try {
            const response = await fetch('http://localhost:4000/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(formData)
            })

            const data = await response.json()

            if (response.ok) {
                // Store token in localStorage
                localStorage.setItem('token', data.access_token)
                localStorage.setItem('user', JSON.stringify(data.user))

                // Redirect to dashboard
                navigate('/home')
            } else {
                setError(data.error || 'Login failed')
            }
        } catch (err) {
            setError('Network error. Please try again.')
        }
    }

    return (
        <div className="login-page">
            <Header />

            <main>
                <div className="page-center">
                    <section className="login-register-section">
                        <h1>Sign In</h1>

                        <form onSubmit={handleSubmit}>
                            <input
                                name="email"
                                placeholder="Email"
                                value={formData.email}
                                onChange={handleChange}
                                className={`input${fieldErrors.email ? ' error' : ''}`}
                            />
                            {fieldErrors.email && (
                                <p className="form-error">{fieldErrors.email}</p>
                            )}

                            <input
                                type="password"
                                name="password"
                                placeholder="Password"
                                value={formData.password}
                                onChange={handleChange}
                                className={`input${fieldErrors.password ? ' error' : ''}`}
                            />
                            {fieldErrors.password && (
                                <p className="form-error">{fieldErrors.password}</p>
                            )}

                            {error && <p className="form-error">{error}</p>}

                            <button type="submit">Sign In</button>
                        </form>

                        <p>
                            Don't have an account? <Link to="/register">Sign up now.</Link>
                        </p>
                    </section>
                </div>
            </main>
        </div>
    )
}

export default Login
