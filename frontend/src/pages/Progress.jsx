import HeaderHome from "../components/HeaderHome";
import HomeSidebar from "../components/HomeSidebar";
import { useState, useEffect } from "react";
import Loading from "../components/Loading";
import { fetchAPI_JSON } from "../utils/api";
import './Progress.css';

function Progress() {
  // Types of data to show
  // 1. # learning, # reviewing, # mastered words
  // 2. bar chart of % of hsk words mastered per level
  // 3. # of practice questions answered
  // 4. # hrs spent practicing
  const [learningCount, setLearningCount] = useState(0);
  const [reviewingCount, setReviewingCount] = useState(0);
  const [masteredCount, setMasteredCount] = useState(0);
  const [practiceQuestionsAnswered, setPracticeQuestionsAnswered] = useState(0);
  const [hoursSpentPracticing, setHoursSpentPracticing] = useState(0);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Fetch all vocab word for the counts
    const fetchData = async () => {
      try {
        const data = await fetchAPI_JSON('/api/progress/', { method: 'GET' });
        setLearningCount(data.learning_count || 0);
        setReviewingCount(data.reviewing_count || 0);
        setMasteredCount(data.mastered_count || 0);
        setHoursSpentPracticing(Math.ceil(data.time_spent / 3600)); // Convert seconds to hours and ceil
        setPracticeQuestionsAnswered(data.practice_completed);
        setLoading(false);
      } catch (error) {
        console.error('Error fetching vocabulary:', error);
        setLoading(false);
      }
    };
    fetchData();
  }, []);

  if (loading) {
    return <Loading />;
  }
  return (
    <div className="progress">
      <HeaderHome />

      <div className="home-container">
        <HomeSidebar activePage="progress" />

        <main className="content">
          <h1>Progress</h1>

          <div className="progress-container">
            <div className="progress-circle">
              <h2>Total Words</h2>
              <p>{learningCount + reviewingCount + masteredCount}</p>
            </div>

            <div className="progress-circle">
              <h2>Hours Spent Practicing</h2>
              <p>{hoursSpentPracticing}</p>
            </div>

            <div className="progress-circle">
              <h2>Words Learning</h2>
              <p>{learningCount}</p>
            </div>

            <div className="progress-circle">
              <h2>Words Reviewing</h2>
              <p>{reviewingCount}</p>
            </div>

            <div className="progress-circle">
              <h2>Words Mastered</h2>
              <p>{masteredCount}</p>
            </div>

            <div className="progress-circle">
              <h2>Practice Questions Answered</h2>
              <p>{practiceQuestionsAnswered}</p>
            </div>
          </div>
        </main>
      </div>
    </div>
  );
}

export default Progress;
