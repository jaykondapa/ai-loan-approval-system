import { useState } from "react";

import Header from "./components/Header";
import Footer from "./components/Footer";
import LoanForm, { initialFormData } from "./components/LoanForm";
import PredictionCard from "./components/PredictionCard";
import LoadingSpinner from "./components/LoadingSpinner";
import { predictLoan } from "./services/api";

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
    setPrediction(null);

    try {
      const result = await predictLoan(formData);
      setPrediction(result);
    } catch (requestError) {
      console.error(requestError);
      setPrediction(null);

      setError(
        requestError.message ||
          "Unable to complete the prediction. Please try again."
      );
    } finally {
      setLoading(false);
    }
  };

  const handleReset = () => {
    setPrediction(null);
    setError("");
  };

  return (
    <div className="app-shell">
      <Header />

      <main className="page-content">
        <div className="intro-panel">
          <div>
            <p className="section-label">Credit Risk Decision Support</p>
            <h2>Evaluate an applicant using machine learning</h2>
          </div>

          <p>
            Enter the applicant&apos;s financial and personal information to
            receive a credit-risk prediction from the tuned Gradient Boosting
            model.
          </p>
        </div>

        <div className="application-layout">
          <LoanForm
            formData={formData}
            setFormData={setFormData}
            onSubmit={handleSubmit}
            onReset={handleReset}
            loading={loading}
          />

          <aside className="results-column">
            {loading ? (
              <LoadingSpinner />
            ) : (
              <PredictionCard result={prediction} />
            )}

            {error && <div className="error-message">{error}</div>}
          </aside>
        </div>
      </main>

      <Footer />
    </div>
  );
}

export default App;