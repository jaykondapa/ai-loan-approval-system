import { useState } from "react";

import Header from "./components/Header";
import Footer from "./components/Footer";
import LoanForm, { initialFormData } from "./components/LoanForm";
import LoadingSpinner from "./components/LoadingSpinner";
import ResultPage from "./components/ResultPage";
import { predictLoanWithExplanation } from "./services/api";

import "./App.css";

function App() {
  const [formData, setFormData] = useState(initialFormData);
  const [prediction, setPrediction] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  const handleSubmit = async (event) => {
    event.preventDefault();

    setLoading(true);
    setError("");

    try {
      const result = await predictLoanWithExplanation(formData);
      setPrediction(result);
    } catch (requestError) {
      console.error(requestError);

      setPrediction(null);
      setError(
        requestError.message ||
          "Unable to complete the assessment. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setFormData(initialFormData);
    setPrediction(null);
    setError("");
  };

  const handleStartNew = () => {
    setFormData(initialFormData);
    setPrediction(null);
    setError("");
    window.scrollTo({ top: 0, behavior: "smooth" });
  };

  if (loading) {
    return (
      <div className="app-shell">
        <Header />

        <main className="full-page-state">
          <LoadingSpinner />
        </main>

        <Footer />
      </div>
    );
  }

  if (prediction) {
    return (
      <div className="app-shell">
        <Header />

        <main className="page-content result-page-content">
          <ResultPage
            result={prediction}
            onStartNew={handleStartNew}
          />
        </main>

        <Footer />
      </div>
    );
  }

  return (
    <div className="app-shell">
      <Header />

      <main className="page-content landing-page-content">
        <section className="intro-panel centered-panel">
          <div className="intro-copy">
            <p className="section-label">
              Credit Risk Decision Support
            </p>

            <h2>
              Evaluate an applicant using machine learning
            </h2>

            <p>
              Enter the applicant&apos;s financial and personal information to
              receive a preliminary credit-risk assessment.
            </p>
          </div>
        </section>

        <section className="form-container">
          <LoanForm
            formData={formData}
            setFormData={setFormData}
            onSubmit={handleSubmit}
            onReset={handleReset}
            loading={loading}
          />
        </section>

        {error && (
          <div className="error-message form-error-message">
            {error}
          </div>
        )}
      </main>

      <Footer />
    </div>
  );
}

export default App;