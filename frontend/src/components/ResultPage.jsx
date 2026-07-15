import { useState } from "react";

function SummaryRow({ label, value }) {
  return (
    <div className="details-row">
      <span>{label}</span>
      <strong>{value}</strong>
    </div>
  );
}

function ResultPage({ result, onStartNew }) {
  const [showDetails, setShowDetails] = useState(false);

  const approved = result.decision === "Approved";
  const summary = result.ai_explanation?.loan_officer_summary;
  const customerMessage = result.ai_explanation?.customer_message;

  return (
    <section className="result-page">
      <div className="result-message-card">
        <span
          className={`status-badge ${
            approved ? "approved-badge" : "rejected-badge"
          }`}
        >
          {approved ? "Favorable Preliminary Assessment" : "Preliminary Assessment"}
        </span>

        <p className="section-label">Application Update</p>

        <h1>
          {approved
            ? "Your application received a favorable preliminary assessment"
            : "Your application did not receive a favorable preliminary assessment"}
        </h1>

        <p className="customer-result-message">
          {customerMessage}
        </p>

        <div className="result-actions">
          <button
            className="primary-button result-button"
            type="button"
            onClick={() => setShowDetails((current) => !current)}
          >
            {showDetails ? "Hide Internal Details" : "View Internal Details"}
          </button>

          <button
            className="secondary-button result-button"
            type="button"
            onClick={onStartNew}
          >
            Start New Assessment
          </button>
        </div>
      </div>

      {showDetails && summary && (
        <div className="internal-details-panel">
          <div className="details-header">
            <div>
              <p className="section-label">Internal Use Only</p>
              <h2>Loan Officer Assessment Details</h2>
            </div>

            <span className="internal-badge">Internal Use Only</span>
          </div>

          <div className="details-section">
            <h3>Model Assessment</h3>

            <div className="details-grid">
              <SummaryRow
                label="Model Decision"
                value={summary.model_decision}
              />

              <SummaryRow
                label="Approval Probability"
                value={`${(summary.approval_probability * 100).toFixed(2)}%`}
              />

              <SummaryRow
                label="Risk Probability"
                value={`${(summary.risk_probability * 100).toFixed(2)}%`}
              />

              <SummaryRow
                label="Risk Level"
                value={summary.risk_level}
              />

              <SummaryRow
                label="Confidence"
                value={summary.confidence}
              />

              <SummaryRow
                label="Prediction Time"
                value={`${result.prediction_time_ms} ms`}
              />

              <SummaryRow
                label="Model"
                value={result.model_name}
              />
            </div>
          </div>

          <div className="details-section">
            <h3>Loan Request</h3>

            <div className="details-grid">
              <SummaryRow
                label="Requested Amount"
                value={`${summary.requested_loan_amount.toLocaleString()} DM`}
              />

              <SummaryRow
                label="Requested Duration"
                value={`${summary.requested_duration_months} months`}
              />

              <SummaryRow
                label="Purpose"
                value={summary.loan_purpose}
              />
            </div>
          </div>

          <div className="details-section">
            <h3>Applicant Profile</h3>

            <div className="details-table">
              <SummaryRow
                label="Checking Account"
                value={summary.checking_account}
              />

              <SummaryRow
                label="Savings Account"
                value={summary.savings_account}
              />

              <SummaryRow
                label="Credit History"
                value={summary.credit_history}
              />

              <SummaryRow
                label="Employment Duration"
                value={summary.employment_duration}
              />

              <SummaryRow
                label="Existing Credits"
                value={summary.existing_credits}
              />

              <SummaryRow
                label="Housing"
                value={summary.housing}
              />

              <SummaryRow
                label="Property"
                value={summary.property}
              />

              <SummaryRow
                label="Job"
                value={summary.job}
              />
            </div>
          </div>
        </div>
      )}
    </section>
  );
}

export default ResultPage;