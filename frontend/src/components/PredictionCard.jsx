function PredictionCard({ result }) {
  if (!result) {
    return (
      <section className="prediction-card prediction-placeholder">
        <h2>Prediction Result</h2>
        <p>Complete the loan application to view the assessment.</p>
      </section>
    );
  }

  const approved = result.decision === "Approved";

  return (
    <section className={`prediction-card ${approved ? "approved" : "rejected"}`}>
      <div className="result-heading">
        <div>
          <p className="section-label">Prediction Result</p>
          <h2>{approved ? "Loan Approved" : "Loan Rejected"}</h2>
        </div>

        <span className={`status-badge ${approved ? "approved-badge" : "rejected-badge"}`}>
          {result.decision}
        </span>
      </div>

      <div className="probability-block">
        <span>Approval Probability</span>
        <strong>{(result.approval_probability * 100).toFixed(2)}%</strong>

        <div className="progress-track">
          <div
            className="progress-value"
            style={{ width: `${result.approval_probability * 100}%` }}
          />
        </div>
      </div>

      <div className="result-grid">
        <div className="metric-card">
          <span>Risk Probability</span>
          <strong>{(result.risk_probability * 100).toFixed(2)}%</strong>
        </div>

        <div className="metric-card">
          <span>Risk Level</span>
          <strong>{result.risk_level}</strong>
        </div>

        <div className="metric-card">
          <span>Confidence</span>
          <strong>{result.confidence}</strong>
        </div>

        <div className="metric-card">
          <span>Prediction Time</span>
          <strong>{result.prediction_time_ms} ms</strong>
        </div>
      </div>

      <div className="model-details">
        Model used: <strong>{result.model_name}</strong>
      </div>

      <p className="disclaimer">
        This result is generated for demonstration purposes and should not be
        treated as a real lending decision.
      </p>
    </section>
  );
}

export default PredictionCard;