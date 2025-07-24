import HeaderHero from '../components/HeaderHero'
import Hero from '../components/Hero'
import Footer from '../components/Footer'
import './Home.css'

function Home() {
    return (
        <div className="home">
            <HeaderHero />

            <main>
                <Hero />

                <div className="container">
                    <section className="two-column">
                        <div className="image-column">
                            <img src="/dummy.jpg" alt="Example image" />
                        </div>
                        <div className="content-column">
                            <h2>simple & effective</h2>
                            <p>
                                Practicing with Charpete is simple and effective. No more hours of unstructured
                                and more of effective exercises powered by AI that focus on reading, writing, and speaking.
                            </p>
                        </div>
                    </section>


                    <section className="two-column">
                        <div className="content-column">
                            <h2>personalized learning</h2>
                            <p>
                                Choose what you want to learn or let Charpete automatically choose for you! With a
                                custom algorithm that adapts to your strengths and weaknesses, you will optimize
                                your learning and long-term retention.
                            </p>
                        </div>
                        <div className="image-column">
                            <img src="/hero.jpg" alt="Personalized learning" />
                        </div>
                    </section>

                    <section className="two-column">
                        <div className="image-column">
                            <img src="/dummy.jpg" alt="Example image" />
                        </div>
                        <div className="content-column">
                            <h2>unlimited dictation exercises</h2>
                            <p>
                                Transcribe what you hear using pinyin or characters. Sharpen your listening
                                comprehension whiel also memorizing words and phrases naturally.
                            </p>
                        </div>
                    </section>
       

       
                    <section className="two-column">
                        <div className="content-column">
                            <h2>unlimited writing practice</h2>
                            <p>
                                Memorize your vocabulary through sentence construction or repetition exercises.
                                These exercises are designed to reinforce stroke order, build muscle memory,
                                and improve writing fluency.
                            </p>
                        </div>
                        <div className="image-column">
                            <img src="/dummy.jpg" alt="Example image" />
                        </div>
                    </section>
     


                    <section className="two-column">
                        <div className="image-column">
                            <img src="/dummy.jpg" alt="Example image" />
                        </div>
                        <div className="content-column">
                            <h2>unlimited speaking exercises</h2>
                            <p>
                                Master your pronunciation and comprehension through speaking exercises as short
                                as a sentence to as long as a paragraph. These exercises target your reading
                                recognition and critial thinking abilities.
                            </p>
                        </div>
                    </section>
                </div>
            </main>

            <Footer />
        </div>
    )
}

export default Home
