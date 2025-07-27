import { useState } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import Header from '../components/Header'
import './LoginRegister.css'
import { fetchAPI_JSON } from '../utils/api'

function Register() {
    const [formData, setFormData] = useState({
        name: '',
        email: '',
        password: ''
    })

    const [error, setError] = useState('')
    const [fieldErrors, setFieldErrors] = useState({
        name: '',
        email: '',
        password: ''
    })

    const validateForm = () => {
        const newErrors = {
            name: '',
            email: '',
            password: ''
        }

        if (!formData.name.trim()) {
            newErrors.name = 'Name is required'
        }

        if (!formData.email.trim()) {
            newErrors.email = 'Email is required'
        }
        if (!formData.password.trim()) {
            newErrors.password = 'Password is required'
        }

        setFieldErrors(newErrors)
        return !newErrors.name && !newErrors.email && !newErrors.password
    };

    const [passwordRules, setPasswordRules] = useState({
        length: false,
        uppercase: false,
        number: false,
    });

    const [showPasswordRules, setShowPasswordRules] = useState(false);

    const validatePassword = (password) => {
        const rules = {
            length: password.length >= 8,
            uppercase: /[A-Z]/.test(password),
            number: /\d/.test(password),
        };
        setPasswordRules(rules);
        return rules;
    };

    const navigate = useNavigate()

    const handleChange = (e) => {
        const { name, value } = e.target
        // Clear field error if it exists
        if (fieldErrors[name]) {
            setFieldErrors({
                ...fieldErrors,
                [name]: ''
            })
        }

        setFormData({
            ...formData,
            [e.target.name]: e.target.value
        })
        
        // Real-time password validation
        if (name === 'password') {
            setShowPasswordRules(true);
            validatePassword(value);
        }
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setFieldErrors({ name: '', email: '', password: '' })
        setError('')
        setShowPasswordRules(false)


        // Validate form fields
        if (!validateForm()) {
            return;
        }

        // Validate password rules
        const rules = validatePassword(formData.password);
        if (!rules.length || !rules.uppercase || !rules.number) {
            setShowPasswordRules(true);
            return;
        }

        try {
            const data = await fetchAPI_JSON('/api/auth/register', {
                method: 'POST',
                body: JSON.stringify(formData),
            })

            if (data.user) {
                // Store token in localStorage
                localStorage.setItem('token', data.access_token)
                localStorage.setItem('user', JSON.stringify(data.user))

                // Redirect to dashboard
                navigate('/home')
            } else {
                setError(data.error || 'Registration failed')
            }
        } catch (err) {
            setError('Network error. Please try again.')
        }
    }

    return (
        <div className="register-page">
            <Header />

            <main>
                <div className="page-center">
                    <section className="login-register-section">
                        <h1>Sign Up</h1>
                        <form onSubmit={handleSubmit}>
                            <div className="input-group">
                            <input
                                name="name"
                                placeholder="Full Name"
                                value={formData.name}
                                onChange={handleChange}
                                className={`input${fieldErrors.name ? ' error' : ''}`}
                            />
                            {fieldErrors.name && (
                                <p className="form-error">{fieldErrors.name}</p>
                            )}
                            </div>

                            <div className="input-group">
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
                            </div>

                            <div className="input-group">
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
                            </div>

                            {showPasswordRules && (
                                <div className="password-rules">
                                    <h2>Password must contain:</h2>
                                    <ul>
                                        <li className={passwordRules.length ? 'valid' : ''}>At least 8 characters</li>
                                        <li className={passwordRules.uppercase ? 'valid' : ''}>At least 1 uppercase letter</li>
                                        <li className={passwordRules.number ? 'valid' : ''}>At least 1 number</li>
                                    </ul>
                                </div>
                            )}

                            <button type="submit">Sign Up</button>
                        </form>

                        <p>
                            Already have an account? <Link to="/login">Sign in now.</Link>
                        </p>
                    </section>
                </div>
            </main>
        </div>
    )
}

export default Register
